<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/parser.inc.php';

if(isset($_GET['f']))
{
	if(is_file($_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/schemas/'.$_GET['f']))
	{
		$moduleHandler = null;
		if(isset($_SESSION['xsd_parser']['parser']))
		{
			$manager = unserialize($_SESSION['xsd_parser']['parser']);
		}
		
		$schemaFilename = $_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/schemas/'.$_GET['f'];
		
		if(isset($_GET['p']) && is_int(intval($_GET['p']))) loadSchema($schemaFilename, intval($_GET['p']));
		else loadSchema($schemaFilename);
		
		
		
		// Unset the current xml tree as it should be reloaded 
		//if(isset($_SESSION['xsd_parser']['xml_tree'])) unset($_SESSION['xsd_parser']['xml_tree']);
	}
}

displayConfiguration();
?>