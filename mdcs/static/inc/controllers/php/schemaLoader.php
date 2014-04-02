<?php
session_start();
require_once $_SESSION['config']['_ROOT_'] . '/parser/parser.inc.php';

if(isset($_GET['n']))
{
	loadSchema($_SESSION['config']['_XSDFOLDER_'].'/'.$_GET['n']);
}
//else
	// Log error message

?>