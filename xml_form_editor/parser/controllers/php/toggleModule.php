<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/ModuleHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

/**
 * 
 */
if(isset($_GET['m']))
{
	if(isset($_SESSION['xsd_parser']['mhandler']))
	{
		$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
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
		$_SESSION['xsd_parser']['mhandler'] = serialize($mHandler);
	}
	else echo buildJSON("Module handler not initialized", -2);
}
else echo buildJSON("No module to toggle", -1);


?>