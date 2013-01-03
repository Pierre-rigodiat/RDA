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

/**
 * General function to call the parser
 */

//Define a global variable to avoid to reload the parser each time
function loadSchema($schemaFilename)
{
	$debug = $_SESSION['xsd_parser']['conf']['debug'];
	
	$parser = new XsdParser($schemaFilename, $debug);
	
	$rootElementsArray = $parser->parseXsdFile();
	
	$parser->buildTree($rootElementsArray[0]);
		
	$_SESSION['xsd_parser']['parser'] = serialize($parser);
	
	$tree = $parser->getXmlFormTree();
	$_SESSION['xsd_parser']['tree'] = serialize($tree);
	
	/*$display = new XsdDisplay($tree, $debug);
	$_SESSION['xsd_parser']['display'] = serialize($display);*/
}

// ???
function computeMinOccurs()
{
	if(isset($_SESSION['xsd_parser']['parser']))
	{
		$parser = unserialize($_SESSION['xsd_parser']['parser']);
		$parser->computeMinOccurs();
		
		$tree = $parser->getXmlFormTree();
		$_SESSION['xsd_parser']['tree'] = serialize($tree);
		
		$_SESSION['xsd_parser']['parser'] = serialize($parser);
	}
}

// Displays the configuration view of the parser
function displayConfiguration()
{
	if(isset($_SESSION['xsd_parser']['tree']))
	{
		$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['tree']), true); // todo use the variable for debug
		echo $display->displayConfiguration();
	}
}

// Displays the form view of the parser
// TODO Pagination handling
function displayHTMLForm()
{
	if(isset($_SESSION['xsd_parser']['tree']))
	{
		computeMinOccurs();
		$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['tree']), true); // todo use the variable for debug
		
		echo $display->displayHTMLForm();
	}
}

// Displays the XML tree
// TODO Implement it
function displayXmlTree()
{
	if(isset($_SESSION['xsd_parser']['tree']))
	{
		$display = new XsdDisplay(unserialize($_SESSION['xsd_parser']['tree']), true); // todo use the variable for debug
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