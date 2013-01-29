<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/ModuleHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

/**
 * 
 */
if(isset($_GET['m']))
{
	if(isset($_SESSION['xsd_parser']['parser']))
	{
		//$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$mHandler = $manager -> getModuleHandler();
		$mStatus = $mHandler->getModuleStatus($_GET['m']);
		
		// Configure the module status and send the status to display via JSON
		switch($mStatus)
		{
			case 0:
				$mHandler->setModuleStatus($_GET['m'], true);
				echo buildJSON("on", 0);
				break;
			case 1:
				$mHandler->setModuleStatus($_GET['m'], false);
				echo buildJSON("off", 0);
				break;
			case -1:
			default:
				echo buildJSON("Module ".$_GET['m']." does not exists", -3);
				break;
		}
		
		// Register the new handler into session
		$manager -> setModuleHandler($mHandler);
		$_SESSION['xsd_parser']['parser'] = serialize($manager);
	}
	else echo buildJSON("XsdManager not initialized", -2);
}
else echo buildJSON("No module to toggle", -1);


?>