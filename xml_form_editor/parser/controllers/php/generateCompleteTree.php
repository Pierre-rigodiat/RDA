<?php
/**
 * <generateCompleteSchema controller>
 */
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';
/**
 * Generates the complete tree in the background. Avoid people to wait for it during
 * register form loads.
 */
if(isset($_SESSION['xsd_parser']['parser']))
{
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	$manager -> buildCompleteTree();
	
	$_SESSION['xsd_parser']['parser'] = serialize($manager);
	
	echo buildJSON('Complete schema generated', 0);
}
else
{
	echo buildJSON('Parser not initialized', -1);
}