<?php 
	$file = '../tests/test.xml';
	$data = $_POST['data'];
	
	// TODO The XML need to be validate by this script regarding its schema
	$fh = fopen($file, 'w');
	fwrite($fh, $data);
	fclose($fh);
?>