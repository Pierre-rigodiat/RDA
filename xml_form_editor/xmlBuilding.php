<?php
	session_start();
	require_once 'inc/classes/XsdParser.php';

	print_r($_SESSION['app']['data_tree']);
	echo '<hr/>';
	
	$actions = array();
	if(isset($_SESSION['app']['actions'])) print_r($_SESSION['app']['actions']);
	else echo 'NO ACTIONS';
	echo '<hr/>';
	
	$xsd_parser = new XsdParser($_SESSION['elementList'], $_SESSION['rootElement'], $_SESSION['namespace']);
	$xmlContent = $xsd_parser->buildXML($_SESSION['app']['data_tree'], $_SESSION['app']['actions']);
	
	echo htmlspecialchars($xmlContent);

?>