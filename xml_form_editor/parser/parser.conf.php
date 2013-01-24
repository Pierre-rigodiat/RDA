<?php
// TODO Write this element
/**
 * Define global parser variables and store them into $_SESSION['xsd_parser']['conf']
 */

// TODO Define variable names and use it within the code
//$_SESSION['xsd_parser']['conf']['sess_obj_name'] = array('tree'=>'tree', 'mHandler'=>'mHandler', 'pHandler'=>'pHandler')
 
$_SESSION['xsd_parser']['conf']['dirname'] = dirname(dirname(__FILE__));
$_SESSION['xsd_parser']['conf']['modules_dirname'] = dirname(__FILE__).'/_plugins';
// TODO Define the directory where external lib are
// $_SESSION['xsd_parser']['conf']['ext_lib_dirname']
// TODO Define the log directory
$_SESSION['xsd_parser']['conf']['logs_dirname'] = $_SESSION['xsd_parser']['conf']['dirname'] . '/logs';
// TODO Define the log file
$_SESSION['xsd_parser']['conf']['log_file'] = 'debug.log';


$_SESSION['xsd_parser']['conf']['debug'] = true;


?>