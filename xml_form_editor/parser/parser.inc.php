<?php
/**
 * A parser adapter to load everything from this file
 * 
 * 
 */

if(session_id()=='') // If the session has not been started, it is impossible to play with the parser
{
	// TODO Throw an exception rather than writing something
	echo '<div class="error">A session must be started to use the parser</div>';
	exit;	
}

// Loading configuration and useful classes
require_once dirname(__FILE__).'/parser.conf.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
//require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
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
	
	// Build the module handler (if necessary)
	if(!isset($_SESSION['xsd_parser']['mhandler'])) loadModuleHandler();
	$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
	
	// Parse the file
	$manager = new XsdManager($schemaFilename, $pHandler, $mHandler, $debug);
	$rootElementsArray = $manager->parseXsdFile();
	$manager->buildOrganizedTree($rootElementsArray[0]); // TODO Split at this point on 2 function (to be able to choose the root element)
	
	$_SESSION['xsd_parser']['parser'] = serialize($manager);
	
	$logger->log_debug('Schema '.$schemaFilename.' loaded', 'loadSchema');
	
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		$_SESSION['xsd_parser']['display'] = serialize($display);
	}
	else
	{
		$display = new Display($manager, $debug);
		$_SESSION['xsd_parser']['display'] = serialize($display);
	}
	
	$schemaPath = explode('/', $schemaFilename);
	$_SESSION['xsd_parser']['xsd_filename'] = end($schemaPath);
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

/**
 * Displays the configuration view of the parser
 */
function displayConfiguration()
{
	global $logger, $debug;
	
	$logger->log_debug('Displaying configuration...', 'displayConfiguration');
	
	if(isset($_SESSION['xsd_parser']['parser']))
	{
		if(isset($_SESSION['xsd_parser']['display']))
		{
			$display = unserialize($_SESSION['xsd_parser']['display']);
			$display -> update();
		}
		else // If the display has not been created
		{
			$manager = unserialize($_SESSION['xsd_parser']['parser']);
			$display = new Display($manager, $debug);
			$_SESSION['xsd_parser']['display'] = serialize($display);
		}
		
		echo $display -> displayConfiguration();
		
		$logger->log_debug('Configuration displayed', 'displayConfiguration');
		
		return;
	}
	else // If the manager do not exist
	{
		$logger->log_debug('No schema configured', 'displayConfiguration');
		echo '<i>No schema file loaded</i>';
		
		return;
	}
}

/**
 * Displays the form view of the parser
 * 
 */
function displayHTMLForm()
{
	global $logger, $debug;
	
	// If the XsdManager has not been created it is impossible to display something
	if(!isset($_SESSION['xsd_parser']['parser']))
	{
		$logger->log_debug('No schema loaded', 'displayHTMLForm');
		echo '<i>No schema file loaded</i>';
		return;
	}
	
	// Set up the module handler if needed
	// XXX If the XsdManager is set so is the ModuleHandler
	//if(!isset($_SESSION['xsd_parser']['mhandler'])) loadModuleHandler();
	
	// Set up the parser
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	
	// FIXME Condition not good
	if(get_class($manager -> getXsdCompleteTree()) != 'ClosureTable')
	{
		$logger -> log_debug('Building complete tree...', 'displayHTMLForm');
		
		
		// FIXME Change the parameter in the function
		//$rootElements = $manager -> getRootElements();
		
		$manager -> buildCompleteTree(/*$rootElements[0]*/);
		$_SESSION['xsd_parser']['parser'] = serialize($manager);
		
		$logger -> log_debug('Complete tree built', 'displayHTMLForm');
	}
	
	// Set up the display
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
	}
	else
	{
		$display = new Display($manager, $debug);
		$_SESSION['xsd_parser']['display'] = serialize($display);
	}
	
	echo $display->displayHTMLForm();
	
	//$logger->log_debug('Page '.$page.' displayed', 'displayHTMLForm');
}

/**
 * Displays the XML tree
 * TODO Implement it in the display view
 */
function displayXmlTree()
{
	global $logger, $debug;
	
	//echo '"<root><element0>value0</element0><element1>value1</element1></root>"';
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		return $display -> displayXMLTree();
	}	
	
	$logger->log_info('XmlTree displayed', 'displayXmlTree');
}

/**
 * 
 */
function displayPageNavigator()
{
	global $logger, $debug;
	
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		echo $display -> displayPageNavigator();
		
		$logger->log_debug('Page navigator displayed', 'displayPageNavigator');
		
		return;
	}
	else { // If the display is not set
		$logger->log_error('No display element built', 'displayPageNavigator');
		return;
	}
}

/**
 * 
 */
function displayModuleChooser()
{
	global $logger, $debug;
	
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		echo $display -> displayModuleChooser();
		
		$logger->log_debug('Module chooser displayed', 'displayModuleChooser');
		
		return;
	}
	else { // If the module handler is not set, it loaded it automatically
		$logger->log_debug('No display element', 'displayModuleChooser');
		
		loadModuleHandler();
		$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		
		$voidXsdManager = new XsdManager("undefined", new PageHandler(1), $mHandler, $debug);	
		
		$display = new Display($voidXsdManager, $debug);
		$_SESSION['xsd_parser']['display'] = serialize($display);
		
		return displayModuleChooser();
	}
} 

/**
 * 
 */
function displayPageChooser()
{
	global $logger, $debug;
	
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		echo $display -> displayPageChooser();
		
		$logger->log_debug('Page chooser displayed', 'displayPageChooser');
		
		return;
	}
	else { // If the display is not set
		$logger->log_debug('No display element built', 'displayPageChooser');
		
		loadModuleHandler();
		$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		
		$voidXsdManager = new XsdManager("undefined", new PageHandler(1), $mHandler, $debug);	
		
		$display = new Display($voidXsdManager, $debug);
		$_SESSION['xsd_parser']['display'] = serialize($display);
		
		return displayPageChooser();
	}
}

/**
 * Save data entered in the HTML Form
 * @param {array} $dataArray The array containing tuples (id, value)
 */
function saveData($dataArray)
{
	global $logger, $debug;
	
	$logger->log_notice('Registering new data...', 'saveData');
	
	if(is_array($dataArray) && isset($_SESSION['xsd_parser']['parser']))
	{
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		
		foreach ($dataArray as $id => $value) 
		{
			if(is_int($id))
			{
				$manager -> setDataForId($value, $id);
			}
		}
		
		$_SESSION['xsd_parser']['parser'] = serialize($manager);
		$logger->log_notice('Data registered', 'saveData');
	}
	else {
		if(!is_array($dataArray))
			$logger->log_debug('Parameter is not an array', 'saveData');
		else
			$logger->log_debug('XsdManager not initialized', 'saveData');
	}
}

/**
 * 
 */
function clearData()
{
	global $logger, $debug;
	$logger->log_notice('Clearing all data...', 'clearData');
	
	if(isset($_SESSION['xsd_parser']['parser']))
	{
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$manager -> clearData();

		$_SESSION['xsd_parser']['parser'] = serialize($manager);
		$logger->log_notice('All data cleared...', 'clearData');
	}
	else 
	{
		$logger->log_info('XsdManager not initialized', 'clearData');
	}
}

/**
 * 
 */
function getData()
{
	/* Not yet implemented */
}
?>