<?php
	if(isset($_SESSION))
	{
		echo '<h2>Session</h2>';
		
		$session_keys = array_keys($_SESSION);
		
		foreach($session_keys as $key)
		{
			echo '<h5>'.ucfirst($key).'</h5>';
			//var_dump($_SESSION[$key]);
			echo gettype($_SESSION[$key]);
		}
	}
?>