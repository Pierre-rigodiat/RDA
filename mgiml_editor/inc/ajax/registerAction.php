<?php
// XXX Set up the debugger on this script

session_start();

if(isset($_GET['id']) && isset($_GET['action']))
{
	$elementId = 'e'.$_GET['id'];
	
	if(isset($_SESSION[$elementId]))
	{
		switch($_GET['action'])
		{
			case 'add':
				$_SESSION[$elementId] += 1;
				break;
			case 'delete':
				$_SESSION[$elementId] -= 1;
				break;
			default:
				break;
		}
	}
	else
	{
		// XXX Will not work if the number of starting element differs from 1
		switch($_GET['action'])
		{
			case 'add':
				$_SESSION[$elementId] = 2;
				break;
			case 'delete':
				$_SESSION[$elementId] = 0;
				break;
			default:
				break;
		}
	}
}

/*$fileName = '../logs/test.log';

$handler = fopen($fileName, 'a');

fwrite($handler, $_SERVER['QUERY_STRING'].PHP_EOL);

fclose($handler);*/
?>