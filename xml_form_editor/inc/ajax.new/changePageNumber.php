<?php
/**
 * Sets the number of page in the configuration view
 * TODO Move this script into the schema manager folder
 * 
 */
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/parser.inc.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';

if(isset($_GET['p']) && isset($_SESSION['xsd_parser']['parser']))
{
	$newPageHandler = new PageHandler(intval($_GET['p']));
	
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	$manager -> setPageHandler($newPageHandler);
	
	$_SESSION['xsd_parser']['parser'] = serialize($manager);
	/*if(is_file($_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/schemas/'.$_GET['f']))
	{
		$moduleHandler = null;
		if(isset($_SESSION['xsd_parser']['parser']))
		{
			$manager = unserialize($_SESSION['xsd_parser']['parser']);
		}
		
		$schemaFilename = $_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/schemas/'.$_GET['f'];
		
		if(isset($_GET['p']) && is_int(intval($_GET['p']))) loadSchema($schemaFilename, intval($_GET['p']));
		else loadSchema($schemaFilename);
		
		
	}*/
}

// displayConfiguration();
?>