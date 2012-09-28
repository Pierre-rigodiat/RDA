<?php
// TODO More debug info & log

session_start();

header("Content-Disposition: attachment; filename=\"migml.xml\"");
header("Content-Type: application/force-download");
header("Cache-control: private");
//header("Connection: close");

echo $_SESSION['xml_content'];

?>