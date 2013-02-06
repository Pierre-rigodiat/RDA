<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/parser.inc.php';

// Send the $_GET array to the parser
if(isset($_GET) && isset($_GET['a']) && count($_GET)>1)
{
	switch($_GET['a']) // Different type of possible action on the form
	{
		case 's': // Save data
			saveData($_GET);
			break;
		case 'c': // Clear data
			clearData();
			break;
		default:
			break;
	}
}
	



?>