<?php
// TODO Write this element
/**
 * Define global parser variables and store them into $_SESSION['xsd_parser']['conf']
 */

// TODO Configure those variable to be more specific to the parser
$_SESSION['xsd_parser']['conf']['dirname'] = dirname(dirname(__FILE__));
$_SESSION['xsd_parser']['conf']['modules_dirname'] = dirname(__FILE__).'/_plugins';
// TODO Define the directory where external lib are
// $_SESSION['xsd_parser']['conf']['ext_lib_dirname']

//TODO Use this variable in the parser
$appStatus = array(
	"VRB",
	"DEV",
	"DBG",
	"PRD"
);
$SESSION['xsd_parser']['conf']['app_status'] = $appStatus[1];

// Define the log directory & the log file
$_SESSION['xsd_parser']['conf']['logs_dirname'] = $_SESSION['xsd_parser']['conf']['dirname'] . '/logs';
$_SESSION['xsd_parser']['conf']['log_file'] = 'debug.log';


$_SESSION['xsd_parser']['conf']['debug'] = true;


?>