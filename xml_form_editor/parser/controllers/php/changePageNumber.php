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
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';

require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

if(isset($_GET['p']) && isset($_SESSION['xsd_parser']['parser']))
{
	$newPageHandler = new PageHandler(intval($_GET['p']));
	
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	$manager -> setPageHandler($newPageHandler);
	
	$_SESSION['xsd_parser']['parser'] = serialize($manager);
	
	if(isset($_SESSION['xsd_parser']['display']))
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		$response = htmlspecialchars($display -> displayConfiguration());
		echo buildJSON($response, 0);
	}
}
?>