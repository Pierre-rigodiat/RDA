<?php
session_start();
require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';

if(!isset($_SESSION['xsd_parser']['parser']) || !isset($_GET['id']))
{
	throw new Exception("Unitialized variables", -1);
}



$manager = unserialize($_SESSION['xsd_parser']['parser']);
$manager -> removeFormData();

$manager -> setXsdManagerId($_GET['id']);

$manager -> saveFormData();

$_SESSION['xsd_parser']['parser'] = serialize($manager);