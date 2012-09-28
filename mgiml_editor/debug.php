<?php
	session_start();
	
	print_r($_SERVER);
	
	if(isset($_GET['clear_sess']))
	{
		session_destroy();
	}
	
	if (function_exists('exec'))
	{
		$output = array();
	
		if (substr(strtoupper(PHP_OS), 0, 3) == 'WIN')
		{
			exec('tasklist /FI "PID eq ' . getmypid() . '" /FO LIST', $output);
	
			$result = preg_replace('/[\D]/', '', $output[5]);
		}
	
		else
		{
			exec('ps -eo%mem,rss,pid | grep ' . getmypid(), $output);
	
			$output = explode('  ', $output[0]);
	
			$result = $output[1];
		}
	}
	
	echo $result.'<br/>';
	
	
	echo memory_get_usage(true).'<br/><br/>';
	echo ini_get('memory_limit').'<br/><br/>';
	
	if(isset($_SESSION))
	{
		print_r($_SESSION);
	}

?>