<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/parser.inc.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

// Send the $_GET array to the parser
if(isset($_GET) && isset($_GET['a']) && count($_GET)>1)
{
	switch($_GET['a']) // Different type of possible action on the form
	{
		case 's': // Save data in session
			saveData($_GET);
			break;
		case 'd': // Save data in db
			saveData($_GET, 'db');
			break;
		case 'l': // Load data
			clearData();
			echo buildJSON(htmlspecialchars(loadData($_GET["id"])), 0);
			break;
		case 'c': // Clear data
			clearData();
			break;
		default:
			// XXX Make a logger ?
			break;
	}
}