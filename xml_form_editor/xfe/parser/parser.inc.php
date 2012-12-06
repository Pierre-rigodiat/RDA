<?php
session_start();
require_once dirname(__FILE__).'/parser.conf.php';

require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdParser.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/XsdDisplay.php';

//Define a global variable to avoid to reload the parser each time
function loadSchema($schemaFilename)
{
	$debug = $_SESSION['xsd_parser']['conf']['debug'];
	
	$parser = new XsdParser($schemaFilename, $debug);
	
	$rootElementsArray = $parser->parseXsdFile();
	
	$parser->buildTree($rootElementsArray[0]);
		
	$tree = $parser->getXmlFormTree();
	$_SESSION['xsd_parser']['tree'] = serialize($tree);
	
	$display = new XsdDisplay($tree, $debug);
	$_SESSION['xsd_parser']['display'] = serialize($display);
}


function displayConfiguration()
{
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		echo $display->displayConfiguration();
	}
}

function displayHTMLForm()
{
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		echo $display->displayHTMLForm();
	}
}

function displayXmlTree()
{
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		echo $display->displayXMLTree();
	}
}

/**
 * Function to call modules
 */
// TODO automatically include a PHP script in the module
 
?>