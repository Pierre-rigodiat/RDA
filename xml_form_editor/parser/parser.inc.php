<?php
if(session_id()=='') // If the session has not been started, it is impossible to play with the parser
{
	echo '<div class="error">A session must be started to use the parser</div>';
	exit;	
}

// Loading configuration and useful classes
require_once dirname(__FILE__).'/parser.conf.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdParser.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/ModuleHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/XsdDisplay.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/ModuleDisplay.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';

// TODO put some data in the configuration file
// TODO Use the display as a configuration variable (use XsdDisplay::setTree to update the current tree after modification)

// Debug and logger configuration for the file
$debug = $_SESSION['xsd_parser']['conf']['debug'];
if($debug) $logger_level = 'notice';
else $logger_level = 'info';

$logger = new Logger($logger_level, $_SESSION['xsd_parser']['conf']['dirname'].'/logs/parser.inc.log', 'parser.inc.php');

/**
 * General function to call the parser
 */

 /**
  * 
  */
function loadSchema($schemaFilename)
{
	global $logger, $debug;
	$logger->log_debug('Function called w/ file '.$schemaFilename, 'loadSchema');
	
	$parser = new XsdParser($schemaFilename, $debug);
	$rootElementsArray = $parser->parseXsdFile();
	$parser->buildTree($rootElementsArray[0]); // TODO Split at this point on 2 function (to be able to choose the root element)
	
	$_SESSION['xsd_parser']['parser'] = serialize($parser);
	
	$tree = $parser->getXmlTree();
	$_SESSION['xsd_parser']['xsd_tree'] = serialize($tree);
	
	/*$display = new XsdDisplay($tree, $debug);
	$_SESSION['xsd_parser']['display'] = serialize($display);*/
}

/**
 * Load every module using the module handler
 */
function loadModules()
{
	global $logger, $debug;
	$logger->log_debug('Function called', 'loadModules');
	
	// Build the module handler object
	if(isset($_SESSION['xsd_parser']['conf']['modules_dirname']))
	{
		$mHandler = new ModuleHandler($_SESSION['xsd_parser']['conf']['modules_dirname'], true);
		
		// Store it into a $_SESSION variable
		$_SESSION['xsd_parser']['mhandler']	= serialize($mHandler);
	}
	else 
	{
		$logger->log_error('Configuration variable $_SESSION[\'xsd_parser\'][\'conf\'][\'modules_dirname\'] missing', 'loadSchema');
	}	
}

// Displays the configuration view of the parser
function displayConfiguration()
{
	global $logger, $debug;
	$logger->log_debug('Function called', 'displayConfiguration');
	
	if(isset($_SESSION['xsd_parser']['xsd_tree']))
	{
		if(isset($_SESSION['xsd_parser']['mhandler']))
		{
			$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
			$moduleDisplay = new ModuleDisplay($mHandler, $debug);
			
			$logger->log_debug('ModuleDisplay created', 'displayConfiguration');
		}
		else { // If the module handler is not set, it loaded it automatically
			$logger->log_debug('Need to create the module handler first', 'displayConfiguration');
			loadModules();
			return displayConfiguration();
		}		
		
		$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['xsd_tree']), $moduleDisplay, $debug);
		echo $display->displayConfiguration();
		
		return;
	}
	else
	{
		$logger->log_debug('No schema loaded', 'displayConfiguration');
		echo '<i>No schema file loaded</i>';
		
		return;
	}
}

// Displays the form view of the parser
// TODO Pagination handling
function displayHTMLForm()
{	
	global $logger, $debug;
	$logger->log_debug('Function called', 'displayHTMLForm');
	
	if(isset($_SESSION['xsd_parser']['mhandler']))
	{
		$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		$moduleDisplay = new ModuleDisplay($mHandler, $debug);
		
		$logger->log_debug('ModuleDisplay created and module chooser displayed', 'displayModuleChooser');
	}
	else { // If the module handler is not set, it loaded it automatically
		$logger->log_debug('Need to create the module handler first', 'displayConfiguration');
		loadModules();
		return displayHTMLForm();
	}
	
	if(!isset($_SESSION['xsd_parser']['xml_tree'])) // If the xml_tree is not set, it built it
	{
		if(isset($_SESSION['xsd_parser']['xsd_tree'])) // Need a basis to build the form
		{
			// Computing MINOCCURS using the parser function
			// Allows to display the right number of element
			if(isset($_SESSION['xsd_parser']['parser']))
			{
				$parser = unserialize($_SESSION['xsd_parser']['parser']);
				$parser->computeMinOccurs();
				
				$tree = $parser->getXmlTree();
				$_SESSION['xsd_parser']['xml_tree'] = serialize($tree);
				
				$_SESSION['xsd_parser']['parser'] = serialize($parser);
			}
			
			// Build the form
			$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['xml_tree']), $moduleDisplay, $debug);
			echo $display->displayHTMLForm();
		}
		else // No schema has been loaded ($_SESSION['xsd_parser']['xsd_tree'] does not exist)
		{
			$logger->log_debug('No schema loaded', 'displayHTMLForm');
			echo '<i>No schema file loaded</i>';
		}
	}
	else // An XML tree already exists
	{
		$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['xml_tree']), $moduleDisplay, $debug);
		echo $display->displayHTMLForm();
	}
}

// Displays the XML tree
// TODO Implement it in the display view
function displayXmlTree()
{
	global $logger, $debug;
	$logger->log_debug('Function called', 'displayXmlTree');
	
	if(isset($_SESSION['xsd_parser']['tree']))
	{
		$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['tree']), $debug);
		echo $display->displayXMLTree();
	}
}

/**
 * Function to call modules
 */
// TODO automatically include all module functions
// XXX try to hide to module handling from the website and from this file


/**
 * 
 */
function displayModuleChooser()
{
	global $logger, $debug;
	
	if(isset($_SESSION['xsd_parser']['mhandler']))
	{
		$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		$moduleDisplay = new ModuleDisplay($mHandler, $debug);
		echo $moduleDisplay -> displayModuleChooser();
		
		$logger->log_debug('ModuleDisplay created and module chooser displayed', 'displayModuleChooser');
		
		return;
	}
	else { // If the module handler is not set, it loaded it automatically
		$logger->log_debug('Need to create the module handler first', 'displayModuleChooser');
		loadModules();
		return displayModuleChooser();
	}
}
 
?>