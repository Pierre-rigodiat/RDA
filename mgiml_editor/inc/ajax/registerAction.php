<?php
// XXX Set up the debugger on this script

session_start();

// todo make it compliant with the default number of element (MINOCCURS)
// XXX Will not work if the number of starting element differs from 1
// todo use better path (to be able to determinate if we are violating MIN or MAXOCCURS rules)
if(isset($_GET['action']) && isset($_GET['path']))
{
	if(!isset($_SESSION['app']['actions'])) $_SESSION['app']['actions'] = array();
	
	switch($_GET['action']) 
	{
		case 'a': // Add
			array_push($_SESSION['app']['actions'], 'add|'.$_GET['path']);
			//$_SESSION['app']['multiplicity'][$_GET['path']] += 1;
			break;
		case 'r': // Remove
			array_push($_SESSION['app']['actions'], 'remove|'.$_GET['path']);
			break;
		default:
			echo 'ERROR'; // TODO try to be more explicit
			break;
	}
}
else 
{
	echo 'ERROR'; // TODO try to be more explicit
}
?>