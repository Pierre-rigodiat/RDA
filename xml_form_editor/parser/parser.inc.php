<?php
/**
 * A parser adapter to load everything from this file
 * 
 * 
 */

if(session_id()=='') // If the session has not been started, it is impossible to play with the parser
{
	echo '<div class="error">A session must be started to use the parser</div>';
	exit;	
}

// Loading configuration and useful classes
require_once dirname(__FILE__).'/parser.conf.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdParser.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/ModuleHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';

// TODO put some data in the configuration file
// TODO Use the display as a configuration variable (use XsdDisplay::setTree to update the current tree after modification)

// Debug and logger configuration for the file
$debug = $_SESSION['xsd_parser']['conf']['debug'];
if($debug) $logger_level = 'notice';
else $logger_level = 'info';

$logger = new Logger($logger_level, $_SESSION['xsd_parser']['conf']['logs_dirname'].'/'.$_SESSION['xsd_parser']['conf']['log_file'], 'parser.inc.php');

 /**
  * 
  */
function loadSchema($schemaFilename, $numberOfPage = 1)
{
	global $logger, $debug;
	
	// Build the page handler
	$pHandler = new PageHandler($numberOfPage, $debug);
	$_SESSION['xsd_parser']['phandler'] = serialize($pHandler);
	
	// Build the module handler (if necessary)
	if(!isset($_SESSION['xsd_parser']['mhandler'])) loadModuleHandler();
	$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
	
	// Parse the file
	$parser = new XsdParser($schemaFilename, $debug);
	$rootElementsArray = $parser->parseXsdFile();
	$parser->buildOrganizedTree($rootElementsArray[0]); // TODO Split at this point on 2 function (to be able to choose the root element)
	
	$_SESSION['xsd_parser']['parser'] = serialize($parser);
	
	$logger->log_debug('Schema '.$schemaFilename.' loaded', 'loadSchema');
	
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		$_SESSION['xsd_parser']['display'] = serialize($display);
	}
	else
	{
		$display = new Display($parser, $pHandler, $mHandler, $debug);
		$_SESSION['xsd_parser']['display'] = serialize($display);
	}
}

/**
 * Load every module using the module handler
 */
function loadModuleHandler()
{
	global $logger, $debug;
	
	// Build the module handler object
	if(isset($_SESSION['xsd_parser']['conf']['modules_dirname']))
	{
		$mHandler = new ModuleHandler($_SESSION['xsd_parser']['conf']['modules_dirname'], $debug);
		
		// Store it into a $_SESSION variable
		$_SESSION['xsd_parser']['mhandler']	= serialize($mHandler);
		
		$logger->log_debug('Module handler built and stored into a $_SESSION variable', 'loadModules');
	}
	else 
	{
		$logger->log_error('Configuration variable $_SESSION[\'xsd_parser\'][\'conf\'][\'modules_dirname\'] missing', 'loadModules');
	}	
}

// Displays the configuration view of the parser
function displayConfiguration()
{
	global $logger, $debug;
	
	if(isset($_SESSION['xsd_parser']['parser']) && isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		echo $display -> displayConfiguration();
		
		$logger->log_debug('Configuration displayed', 'displayConfiguration');
		
		return;
	}
	else
	{
		$logger->log_debug('No schema loaded/page handler configured', 'displayConfiguration');
		echo '<i>No schema file loaded</i>';
		
		return;
	}
}

// Displays the form view of the parser
// TODO Pagination handling
function displayHTMLForm($page = 1)
{
	global $logger, $debug;
	
	// TODO Modify the XML tree when you modify the configuration
	
	if(!isset($_SESSION['xsd_parser']['parser']) || !isset($_SESSION['xsd_parser']['phandler']))
	{
		$logger->log_debug('No schema/page hanlder/parser loaded', 'displayHTMLForm');
		echo '<i>No schema file loaded</i>';
		return;
	}
	
	if(!isset($_SESSION['xsd_parser']['mhandler'])) loadModuleHandler();
	
	// Set up the parser
	$parser = unserialize($_SESSION['xsd_parser']['parser']);
	$parser -> buildCompleteTree();
	$_SESSION['xsd_parser']['parser'] = serialize($parser);
	
	// Set up the display
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
	}
	else
	{
		$display = new Display(unserialize($_SESSION['xsd_parser']['parser']), unserialize($_SESSION['xsd_parser']['phandler']), unserialize($_SESSION['xsd_parser']['mhandler']), $debug);
	}
	
	echo $display->displayHTMLForm();
	
	$logger->log_debug('Page '.$page.' displayed', 'displayHTMLForm');
}

// Displays the XML tree
// TODO Implement it in the display view
function displayXmlTree()
{
	global $logger, $debug;
	$logger->log_info('Not yet implemented', 'displayXmlTree');
}

/**
 * 
 */
function displayModuleChooser()
{
	global $logger, $debug;
	
	//if(isset($_SESSION['xsd_parser']['mhandler']))
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		echo $display -> displayModuleChooser();
		
		$logger->log_debug('Module chooser displayed', 'displayModuleChooser');
		
		return;
	}
	else { // If the module handler is not set, it loaded it automatically
		$logger->log_debug('No display element built', 'displayModuleChooser');
		
		loadModuleHandler();
		$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		
		$display = new Display(/*new Tree()*/new XsdParser(""), new PageHandler(0), $mHandler, $debug);
		$_SESSION['xsd_parser']['display'] = serialize($display);
		
		return displayModuleChooser();
	}
} 
?>