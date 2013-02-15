<?php
/**
 * 
 */
session_start();

require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

// TODO Send JSON string as a response
if(isset($_FILES) && isset($_FILES['table_input']) && isset($_FILES['table_input']['error']))
{
	if(end($_FILES['table_input']['error'])==0)
	{
		// todo check if the repository exists
		$repository = $_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/tables';
		
		// todo separate into several project, etc
		move_uploaded_file(end($_FILES["table_input"]["tmp_name"]), $repository.'/'.end($_FILES["table_input"]["name"]));
		
		echo buildJSON('File successfully uploaded', 0);
	}
	else {
		echo buildJSON('Error with the uploaded file ($_FILES error '.$_FILES['table_input']['error'][0].')', -2);
	}
}
else
{
	if(!isset($_FILES)) echo buildJSON('$_FILES array have not been set', -1);
	else if(!isset($_FILES['table_input']) || !isset($_FILES['table_input']['error'])) echo buildJSON('No correct file input(s) sent', -1);
	else echo buildJSON('An unknown error happened, contact the system administrator', -1);
}
?>