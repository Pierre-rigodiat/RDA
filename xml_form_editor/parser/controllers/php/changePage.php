<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

if(isset($_SESSION['xsd_parser']['display']) && isset($_SESSION['xsd_parser']['parser']))
{
	if(isset($_GET['p']))
	{		
		// Setup the correct current page and register the change
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$pHandler = $manager -> getPageHandler();
		$currentPage = $pHandler -> getCurrentPage();
		
		switch($_GET['p'])
		{
			case 'icon next':
				if($currentPage<$pHandler->getNumberOfPage()) $currentPage += 1;
				break;
			case 'icon previous':
				if($currentPage>1) $currentPage -= 1;
				break;
			case 'icon begin':
				$currentPage = 1;
				break;
			case 'icon end':
				$currentPage = $pHandler -> getNumberOfPage();
				break;
			default:
				$currentPage = intval($_GET['p']);
				break;
		}
		
		if(/*is_int($currentPage) && */$currentPage>0 && $currentPage<=$pHandler->getNumberOfPage())
		{
			$pHandler -> setCurrentPage($currentPage);
			$manager -> setPageHandler($pHandler);
			
			$_SESSION['xsd_parser']['parser'] = serialize($manager);
			
			// Update the display
			$display = unserialize($_SESSION['xsd_parser']['display']);
			$display -> update();
			
			$pageChooser = htmlspecialchars($display -> displayPageNavigator());
			
			echo buildJSON($pageChooser, 0);
		}
		else
		{
			echo buildJSON('Wrong parameter given', -2);
		}
	}
	else
	{
		// Update the display
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		$pageContent = htmlspecialchars($display -> displayHTMLForm());
		
		echo buildJSON($pageContent, 0);
	}
}
else 
{
	echo buildJSON('No display or XSD manager in memory', -1);
}
?>