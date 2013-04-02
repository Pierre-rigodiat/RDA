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
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/ModuleHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/SearchHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/db/mongodb/MongoDBStream.php';

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
function loadSchemaFromDB($schemaFileName)
{
	global $logger;
	$mongoDbStream = null;
	
	// Connecting to the default port on localhost
	try
	{
		$mongoDbStream = new MongoDBStream();
		$mongoDbStream -> setDatabaseName("xsdmgr");
		$mongoDbStream -> openDB();
	}
	catch(Exception $e)
	{
		//echo '<div class="error">Impossible to connect to the server</div>';
		exit;
	}
	
	$pathElements = explode('/', $schemaFileName);
	$treeId = $pathElements[count($pathElements)-1];
	
	
	$resultCursor = $mongoDbStream -> queryData(array("_id" => $treeId), "config");
	$resultArray = iterator_to_array($resultCursor);
	
	if(count($resultArray) == 1)
	{
		$result = array_pop($resultArray);
		
		/* Original tree setup */
		$tree = $result["tree"];
		$elementList = $tree["elementList"];
		$ancestorTable = $tree["ancestorTable"];
		
		$trueElementList = array();
		foreach ($elementList as $element) {
			$trueElementList[$element["_id"]] = new XsdElement($element["element"]["type"], $element["element"]["attr"]);
		}
		
		$originalTree = new Tree("originalTree");
		$originalTree -> setTree($trueElementList, $ancestorTable);
		
		/* Page handler setup */
		$logger -> log_debug('PageHandler setup...', 'loadSchemaFromDB');
		$pageHandlerArray = $result["pageHandler"];
		$pageHandler = new PageHandler($pageHandlerArray["numberOfPage"]);
		$pageHandler -> setPageHandler($pageHandlerArray["currentPage"], $pageHandlerArray["pageArray"]);
		
		/* Module handler setup */
		$logger -> log_debug('ModuleHandler setup...', 'loadSchemaFromDB');
		$moduleHandlerArray = $result["moduleHandler"];
		$moduleHandler = new ModuleHandler($moduleHandlerArray["moduleDir"]);
		$moduleHandler -> setModuleHandler($moduleHandlerArray["moduleList"]);
		
		/* XsdManager setup */
		$logger -> log_debug('XsdManager setup...', 'loadSchemaFromDB');
		$manager = new XsdManager($schemaFileName, $pageHandler, $moduleHandler);
		$manager -> setXsdOriginalTree($originalTree);
		$manager -> setNamespaces($result["namespaces"]);
		$manager -> update();
		
		$logger -> log_debug('Element found in DB', 'loadSchemaFromDB');
		return $manager;
	}
	else {
		$logger -> log_info('Nothing in DB', 'loadSchemaFromDB');
		return null;
	}
}


/**
 * 
 */
function loadSchema($schemaFilename, $numberOfPage = 1)
{
	global $logger, $debug;
	
	// Build the page handler
	$pHandler = new PageHandler($numberOfPage, $debug);
	
	// Build the module handler (if necessary)
	// TODO Try to avoid this part
	if(!isset($_SESSION['xsd_parser']['mhandler'])) loadModuleHandler();
	$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
	
	// Parse the file
	$manager = loadSchemaFromDB($schemaFilename);
	
	if(!isset($manager))
	{
		$manager = new XsdManager($schemaFilename, $pHandler, $mHandler, $debug);
		$rootElementsArray = $manager->parseXsdFile();
		$manager->buildOrganizedTree($rootElementsArray[0]); // TODO Split at this point on 2 function (to be able to choose the root element)
	}
	
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
		$display = new Display($manager/*, $debug*/);
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
			$display = new Display($manager/*, $debug*/);
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

function registerForm()
{
	
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
	
	// Set up the parser
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	
	
	
	// Set up the display
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
	}
	else
	{
		// Set up the parser
		//$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$display = new Display($manager/*, $debug*/);
		$_SESSION['xsd_parser']['display'] = serialize($display);
	}

	/* Register the document into MongoDB */
	$manager -> saveFormData();
	$_SESSION['xsd_parser']['parser'] = serialize($manager);
	
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
		
		$display = new Display($voidXsdManager/*, $debug*/);
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
		
		$display = new Display($voidXsdManager/*, $debug*/);
		$_SESSION['xsd_parser']['display'] = serialize($display);
		
		return displayPageChooser();
	}
}

/**
 * 
 */
function displayQuery()
{
	global $logger, $debug;
	
	// If the XsdManager has not been created it is impossible to display something
	if(!isset($_SESSION['xsd_parser']['parser']))
	{
		$logger->log_debug('No schema loaded', 'displayQuery');
		echo '<i>No schema file loaded</i>';
		return;
	}
	
	// Set up the display
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
	}
	else
	{
		
		// Set up the parser
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		//$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$display = new Display($manager/*, $debug*/);
		$_SESSION['xsd_parser']['display'] = serialize($display);
	}
	
	echo $display->displayQuery();
}

/**
 *
 */
function displayAdminQueryTree()
{
	global $logger, $debug;

	// If the XsdManager has not been created it is impossible to display something
	if(!isset($_SESSION['xsd_parser']['parser']))
	{
		$logger->log_debug('No schema loaded', 'displayAdminQueryTree');
		echo '<i>No schema file loaded</i>';
		return;
	}

	/*if (!(isset($manager->getXsdQueryTree()->getElementList) && $manager->getXsdQueryTree()->getElementList != array()))
		$manager -> buildQueryTree();

	$_SESSION['xsd_parser']['parser'] = serialize($manager);*/

	// Set up the display
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
	}
	else
	{

		// Set up the parser
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		//$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$display = new Display($manager/*, $debug*/);
		$_SESSION['xsd_parser']['display'] = serialize($display);
	}

	echo $display->displayAdminQueryTree();
}

/**
 * Save data entered in the HTML Form
 * @param {array} $dataArray The array containing tuples (id, value)
 */
function saveData($dataArray, $where = 'session')
{
	global $logger, $debug;
	
	$logger->log_notice('Registering new data in '.$where.'...', 'saveData');
	
	if(!isset($_SESSION['xsd_parser']['parser']))
	{
		$logger -> log_warning('XsdManager undefined, function stops', 'saveData');
		exit;
	}
	
	if(!is_array($dataArray))
	{
		$logger -> log_warning('Input parameter $array is not an array, function stops', 'saveData');
		exit;
	}
	
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	
	switch($where)
	{
		case 'session':
			$pageHandler = $manager -> getPageHandler();
			$currentPage = $pageHandler -> getCurrentPage();
			
			
			$elementList = $manager -> getXsdCompleteTree() -> getElementList();
			
			foreach($elementList as $elementId => $referenceId)
			{
				// FIXME Element erased are not saved
				/*if(in_array($currentPage, $pageHandler -> getPageForId($referenceId)))
				{*/
					if(isset($dataArray[$elementId]))
					{
						$manager -> setDataForId($dataArray[$elementId], $elementId);
					}
					/*else 
					{
						$manager -> clearDataForId($elementId);
					}
				}*/
				
			}
			
			$logger->log_notice('Data registered in session', 'saveData');
			break;
		case 'db':
			$manager -> saveFormData();
			
			$logger->log_notice('Data registered in db', 'saveData');
			break;
		default:
			$logger -> log_error('Input parameter $where is wrong (='.$where.')', 'saveData');
			throw new Exception("Wrong input parameter", -1);
			break;
	}
	
	$_SESSION['xsd_parser']['parser'] = serialize($manager);
}

function loadData($formId)
{
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	$manager -> retrieveFormData($formId);
	$_SESSION['xsd_parser']['parser'] = serialize($manager);
	
	$display = unserialize($_SESSION['xsd_parser']['display']);
	$display -> update();
	
	return $display -> displayHTMLForm();
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