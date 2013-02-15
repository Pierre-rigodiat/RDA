<?php
session_start();

require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

// todo add some security
// TODO return a JSON string as a response
if(isset($_GET['t_file'])) {
	
	// TODO Change to a configuration variable
	$pythonExec = '"C:/Program Files (x86)/Python/273/python.exe"';
	
	// TODO Check if we cannot create a most practical session value
	$pythonFile = $_SESSION['xsd_parser']['conf']['modules_dirname'].'/table/controllers/python/excelToHDF5.py';
	
	$excelFile = $_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/tables/'.$_GET['t_file']; // todo test if the file exists (if not it returns an error)
	$output = array();
	
	// todo change the path to the file
	//exec('"C:/Program Files/Python/273/python.exe" '.$pythonFile.' "'.$excelFile.'"', $output, $ret_val);
	exec($pythonExec.' '.$pythonFile.' "'.$excelFile.'"', $output, $ret_val);
	
	if($ret_val==0)
	{
		$table = "";
		foreach($output as $print_element)
		{
			$table.=htmlspecialchars($print_element);
		}
		
		/*if(!isset($_SESSION['app']['xml'])) $_SESSION['app']['xml'] = array(); // todo remove it when it is used before (need the update of the datastructure) 
		if(!isset($_SESSION['app']['xml']['tables'])) $_SESSION['app']['xml']['tables'] = array();
		array_push($_SESSION['app']['xml']['tables'], $table);
		*/
		
		$success_message = 'Table successfully converted<span class="icon remove input"></span>';
		$success_message = htmlspecialchars($success_message);
		
		//echo $table;
		echo buildJSON($success_message, 0);
		//echo '0';
	}
	else
	{
		echo buildJSON('Python command line error '.$ret_val, -1);
	}
}
?>