<?php
	/*session_start();
	// todo add some security
	// LIKE we will just call md5 of the file

	if(isset($_GET['xls_file'])) {
		
		$pythonFile = '../../resources/python/excelToHDF5.py';
		$excelFile = '../../resources/files/'.$_GET['xls_file']; // todo test if the file exists (if not it returns an error)
		$output = array();
		
		// todo change the path to the file
		//exec('"C:/Program Files/Python/273/python.exe" '.$pythonFile.' "'.$excelFile.'"', $output, $ret_val);
		exec('"C:/Program Files (x86)/Python/273/python.exe" '.$pythonFile.' "'.$excelFile.'"', $output, $ret_val);
		
		if($ret_val==0)
		{
			$table = "";
			foreach($output as $print_element)
			{
				$table.=htmlspecialchars($print_element);
			}
			
			if(!isset($_SESSION['app']['xml'])) $_SESSION['app']['xml'] = array(); // todo remove it when it is used before (need the datastructure update) 
			if(!isset($_SESSION['app']['xml']['tables'])) $_SESSION['app']['xml']['tables'] = array();
			array_push($_SESSION['app']['xml']['tables'], $table);
			
			echo '0';
		}
		else
		{
			echo 'Python Error (script returns '.$ret_val.'):<br/>';
			//print_r($output);
			//echo htmlspecialchars(end($output));
			
			echo $ret_val;
		}
	}*/
?>