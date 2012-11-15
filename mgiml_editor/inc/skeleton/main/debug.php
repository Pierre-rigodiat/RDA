<?php
	if(isset($_SESSION))
	{
		echo '<h2>Session</h2>';
		
		$session_keys = array_keys($_SESSION);
		
		foreach($session_keys as $key)
		{
			$session = $_SESSION[$key];
			$type = gettype($session);
			
			echo '<h5>'.ucfirst($key).' ('.$type.')</h5>';
			
			if($type=='array')
			{
				echo '<ul>';
				
				foreach($session as $sess_elem)
				{
					echo '<li>';
					print_r($sess_elem);
					echo '</li>';
				}	
							
				echo '</ul>';
			}
			else
			{
				echo '<p>'.htmlspecialchars($session).'</p>';
			}
		}
	}
?>