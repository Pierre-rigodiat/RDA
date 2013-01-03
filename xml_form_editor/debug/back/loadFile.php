<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/parser.inc.php';

if(isset($_GET['f'])/* && isset($_GET['d'])*/)
{
	if(is_file($_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/schemas/'.$_GET['f']))
	{
		$schemaFilename = $_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/schemas/'.$_GET['f'];
		loadSchema($schemaFilename);
		
		displayConfiguration();
	}
}
?>