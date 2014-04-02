<?php
/**
 * 
 */
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

if(isset($_SESSION['xsd_parser']['parser']))
{	
	if (isset($_GET)) {
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		
		$idArray = array();
		foreach ($_GET as $key => $id)
		{
			if (is_numeric($key))
			{
				$idArray[]=$id;
			}
		}
		$search = $manager->getSearchHandler();
		$search->setIdArray($idArray);
		
		$_SESSION['xsd_parser']['parser'] = serialize($manager);
		
		echo buildJSON('Query schema generated', 0);
	}
	else 
	{
		echo buildJSON('No Id selected for the exploration', -2);
	}

}
else
{
	echo buildJSON('parser not initialized', -1);
}