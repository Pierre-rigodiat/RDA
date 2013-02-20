<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

// TODO test if model and view are existing
if(!isset($_SESSION['xsd_parser']['modules']['table']))
{
	echo buildJSON('Module not loaded', -1);
	exit();
}
else 
{
	// Unserialize the two objects to be able to use them further
	$tableModule = unserialize($_SESSION['xsd_parser']['modules']['table']['model']);
	$tableDisplay = unserialize($_SESSION['xsd_parser']['modules']['table']['view']);
}

// todo add some security
// TODO return a JSON string as a response
if(isset($_GET['t_file'])) {
	
	$returnCode = $tableModule -> parseFile($_GET['t_file']);
	$_SESSION['xsd_parser']['modules']['table']['model'] = serialize($tableModule);
	
	if($returnCode == 0) echo buildJSON('Table successfully converted', 0);
	else echo buildJSON('Python command line error '.$returnCode, -1);
}
?>