<?php
/**
 * 
 */
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

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

// Checks if the file has been submitted by POST
if(isset($_FILES) && isset($_FILES['table_input']) && isset($_FILES['table_input']['error']))
{
	if(end($_FILES['table_input']['error'])==0) // No error during the submission
	{
		// todo check if the repository exists
		$repository = $_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/tables';
		
		// todo separate into several project, etc
		move_uploaded_file(end($_FILES["table_input"]["tmp_name"]), $repository.'/'.end($_FILES["table_input"]["name"]));
		
		
		$tableModule -> addFile(end($_FILES["table_input"]["name"]));
		$_SESSION['xsd_parser']['modules']['table']['model'] = serialize($tableModule);
		
		
		$response = htmlspecialchars($tableDisplay -> update());
		$_SESSION['xsd_parser']['modules']['table']['view'] = serialize($tableDisplay);
		
		echo buildJSON($response, 0);
	}
	else {
		echo buildJSON('Error with the uploaded file ($_FILES error '.$_FILES['table_input']['error'][0].')', -3);
	}
}
else
{
	if(isset($_GET) && isset($_GET['name']))
	{
		if(($start = strpos($_GET['name'], '[')) !== FALSE && ($end = strpos($_GET['name'], ']')) !== FALSE)
		{
			// Getting the correct index of the file in the module list
			$start += 1; // To avoid having '[' in the substring
			$inputId = substr($_GET['name'], $start, $end - $start);
			
			// Removing the file and saving session variable
			$tableModule -> removeFile($inputId);
			$_SESSION['xsd_parser']['modules']['table']['model'] = serialize($tableModule);
		
			// Getting the new display
			$response = htmlspecialchars($tableDisplay -> update());
			$_SESSION['xsd_parser']['modules']['table']['view'] = serialize($tableDisplay);
			
			echo buildJSON($response, 0);
		}
		else {
			echo buildJSON('Invalid parameter sent', -3);	
		}
	}
	else 
	{
		echo buildJSON('Invalid request sent', -2);
	}
}
?>