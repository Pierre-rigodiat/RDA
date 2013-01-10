<?php
// TODO Write this element
/**
 * Define global parser variables and store them into $_SESSION['xsd_parser']['conf']
 */
$_SESSION['xsd_parser']['conf']['dirname'] = dirname(dirname(__FILE__));
$_SESSION['xsd_parser']['conf']['modules_dirname'] = dirname(__FILE__).'/_plugins';
// TODO Define the directory where external lib are
// $_SESSION['xsd_parser']['conf']['ext_lib_dirname']
// TODO Define the log directory
// $_SESSION['xsd_parser']['conf']['logs_dirname']

$_SESSION['xsd_parser']['conf']['debug'] = true;


?>