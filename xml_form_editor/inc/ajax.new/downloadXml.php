<?php
// TODO More debug info & log
// TODO more control (to avoid bug )
// XXX Bug on Chrome (warning in the JavaScript console)

session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/parser.inc.php';

header('Content-Disposition: attachment; filename="migml.xml"');
header('Content-Type: application/xml');
header('Cache-control: private');
header('Connection: close');

echo displayXmlTree();
?>