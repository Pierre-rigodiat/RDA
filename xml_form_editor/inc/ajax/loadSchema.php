<?php
	session_start();
	//require_once $_SESSI'inc/global/config.php';
	require_once $_SESSION['config']['_ROOT_'].'/inc/lib/StringFunctions.php';
	require_once $_SESSION['config']['_ROOT_'].'/inc/classes/XsdManager.php';
	
	if(isset($_GET['file']) && trim($_GET['file'])!="")
	{
		/* Sleep for 600ms to tell the user the system is working */
		define('MILLISECONDS',1000);
		usleep(600*MILLISECONDS);
			
		// We begin to parse the file
		$xsd_parser = new XsdManager($_SESSION['config']['_XSDFOLDER_'].'/'.$_GET['file']/*, true*/); // xxx What if $_SESSION variable does not exist
		// todo implement XsdDisplay class
		
		if(isset($_GET['root']) && trim($_GET['root'])!="")
		{
			
		}	
		
		// todo 2 different functions (2 different classes? - 1 for the engineering part the other for the display...)
		$xsd_parser->buildForm();
		// todo Now produce the display XsdDisplay class
		
		
		/*echo '<hr/>'; XXX DEBUG
		print_r($xsd_parser->getElementList());*/ 
		
		// todo use new variables...
		$_SESSION['elementList']=$xsd_parser->getElementList();
		$_SESSION['rootElement']=$xsd_parser->getRoot();
		$_SESSION['namespace']=$xsd_parser->getNamespace();
		
		// todo find a real unique_id
		// xxx avoid using the PHP_SESSID which is not really unique
		/*$_SESSION['app']['global']['elementList']=$xsd_parser->getElementList();
		$_SESSION['app']['unique_id']['elementList']=$xsd_parser->getElementList();
		$_SESSION['app']['global']['rootElement']=$xsd_parser->getRoot();
		$_SESSION['app']['global']['namespace']=$xsd_parser->getNamespace();*/
		
	}
	else
	{
		echo 'Error: No schema specified'; // todo make it an error message
	}
?>