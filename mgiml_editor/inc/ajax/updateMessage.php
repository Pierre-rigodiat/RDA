<?php
	session_start();

	// TODO put severity in message (info, warning, error)
	if(isset($_SESSION['i_m']))
	{
		echo $_SESSION['i_m'];
	}
?>