<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/parser.inc.php';

// Send the $_GET array to the parser
if(isset($_GET) && count($_GET)>0)
	saveData($_GET);



?>