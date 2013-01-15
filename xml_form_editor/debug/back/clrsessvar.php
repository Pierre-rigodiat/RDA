<?php
session_start();

if(isset($_GET['v']))
{
	switch($_GET['v'])
	{
		case 'parser':
			unset($_SESSION['xsd_parser']);
			break;
		default:
			break;
	}
}

header('Location: ../appsessvar.php');
?>