<?php
	// TODO implement debug
	function listDir($dir)
	{
		$resultArray = array("error"=>0, "files"=>array());
	
		if(is_dir($dir))
		{
			if ($dh = opendir($dir)) {
		        while (($file = readdir($dh)) !== false) {
		        	$fileInfoArray = array($file, filetype($dir .'/'. $file));
		        	array_push($resultArray["files"], $fileInfoArray);
				}
				
	        	closedir($dh);
			}
			else 
			{
				$resultArray["error"] = 2; // TODO name the error
			}
		}
		else
		{
			$resultArray["error"] = 1; // TODO name the error
		}
		
		return $resultArray;
	}
?>