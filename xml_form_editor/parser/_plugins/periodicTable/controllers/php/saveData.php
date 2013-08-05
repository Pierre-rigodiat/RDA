<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/_plugins/periodicTable/core/PeriodicTableModule.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/_plugins/periodicTable/view/PeriodicTableDisplay.php';

if( !isset($_GET) || count($_GET) == 0 )
{
	return;
}

if( !isset($_SESSION['xsd_parser']['modules']['pertable']['model']) )
{
	return;
}

$periodicTable = unserialize($_SESSION['xsd_parser']['modules']['pertable']['model']);

foreach($_GET as $elementName => $elementData)
{
	$data = explode(";", $elementData);
	$periodicTable -> setDataForElement($elementName, $data[0], $data[1], $data[2]===''?null:$data[2]);
}

$_SESSION['xsd_parser']['modules']['pertable']['model'] = serialize($periodicTable);

$periodicTableView = unserialize($_SESSION['xsd_parser']['modules']['pertable']['view']);
$periodicTableView -> update();
$_SESSION['xsd_parser']['modules']['pertable']['view'] = serialize($periodicTableView);

