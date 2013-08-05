<?php
session_start();
require_once $_SESSION['config']['_ROOT_'].'/inc/lib/JsonXmlFunctions.php';

if (isset($_SESSION['xsd_parser']['qresult'])) {
	
	header('Content-Disposition: attachment; filename="experiment.xml"');
	header('Content-Type: application/xml');
	header('Cache-control: private');
	header('Connection: close');
	
	$queryResult = unserialize($_SESSION['xsd_parser']['qresult']);
	//var_dump($queryResult);
	
	echo $queryResult;
}
else {
	echo '';
}