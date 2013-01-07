<?php
if(session_id()=='') // If the session has not been started, it is impossible to play with the parser
{
	echo '<div class="error">A session must be started to use the parser</div>';
	exit;	
}

// Loading configuration and useful classes
require_once dirname(__FILE__).'/parser.conf.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdParser.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/XsdDisplay.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';

// TODO put some data in the configuration file

// Debug and logger configuration for the file
$debug = $_SESSION['xsd_parser']['conf']['debug'];
if($debug) $logger_level = 'notice';
else $logger_level = 'info';

$logger = new Logger($logger_level, $_SESSION['xsd_parser']['conf']['dirname'].'/logs/parser.inc.log', 'parser.inc.php');

/**
 * General function to call the parser
 */

//Define a global variable to avoid to reload the parser each time
function loadSchema($schemaFilename)
{
	global $logger, $debug;
	$logger->log_debug('Function called w/ file '.$schemaFilename, 'loadSchema');
	
	$parser = new XsdParser($schemaFilename, $debug);
	$rootElementsArray = $parser->parseXsdFile();
	$parser->buildTree($rootElementsArray[0]);
	
	$_SESSION['xsd_parser']['parser'] = serialize($parser);
	
	$tree = $parser->getXmlTree();
	//$_SESSION['xsd_parser']['tree'] = serialize($tree);
	$_SESSION['xsd_parser']['xsd_tree'] = serialize($tree);
	
	/*$display = new XsdDisplay($tree, $debug);
	$_SESSION['xsd_parser']['display'] = serialize($display);*/
}

// ???
/*function computeMinOccurs()
{
	if(isset($_SESSION['xsd_parser']['parser']))
	{
		$parser = unserialize($_SESSION['xsd_parser']['parser']);
		$parser->computeMinOccurs();
		
		$tree = $parser->getXmlTree();
		$_SESSION['xsd_parser']['tree'] = serialize($tree);
		
		$_SESSION['xsd_parser']['parser'] = serialize($parser);
	}
}*/

// Displays the configuration view of the parser
function displayConfiguration()
{
	global $logger, $debug;
	$logger->log_debug('Function called', 'displayConfiguration');
	
	if(isset($_SESSION['xsd_parser']['xsd_tree']))
	{
		$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['xsd_tree']), $debug);
		echo $display->displayConfiguration();
	}
	else
	{
		echo '<i>No schema file loaded</i>';
	}
}

// Displays the form view of the parser
// TODO Pagination handling
function displayHTMLForm()
{	
	global $logger, $debug;
	$logger->log_debug('Function called', 'displayHTMLForm');
	
	if(!isset($_SESSION['xsd_parser']['xml_tree']))
	{
		if(isset($_SESSION['xsd_parser']['xsd_tree']))
		{
			// Computing MINOCCURS
			if(isset($_SESSION['xsd_parser']['parser']))
			{
				$parser = unserialize($_SESSION['xsd_parser']['parser']);
				$parser->computeMinOccurs();
				
				$tree = $parser->getXmlTree();
				$_SESSION['xsd_parser']['xml_tree'] = serialize($tree);
				
				$_SESSION['xsd_parser']['parser'] = serialize($parser);
			}
			
			$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['xml_tree']), $debug);
			echo $display->displayHTMLForm();
		}
		else 
		{
			$logger->log_debug('No schema loaded', 'displayHTMLForm');
			echo '<i>No schema file loaded</i>';
		}
	}
	else
	{
		$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['xml_tree']), $debug);
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

function getModuleList()
{
	$result = array();
	
	if(isset($_SESSION['xsd_parser']['conf']['modules_dirname']))
	{
		$module_dir = $_SESSION['xsd_parser']['conf']['modules_dirname'];
		
		if(is_dir($module_dir))
		{
			$fileList = scandir($module_dir);
			
			foreach($fileList as $file)
			{
				if(is_dir($module_dir.'/'.$file) && !startsWith($file, '.'))
					array_push($result,$file);
			}

			return $result;
		}
		else {
			return null;
		}
	}
	else {
		return null;
	}
}
 
?>