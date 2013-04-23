<?php
session_start();
require_once $_SESSION['config']['_ROOT_'].'/inc/db/mongodb/MongoDBStream.php';
require_once $_SESSION['config']['_ROOT_'].'/parser/core/XsdManager.php';
require_once $_SESSION['config']['_ROOT_'].'/parser/view/Display.php';
require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';

$xmlString = displayXMLTree();

$manager = unserialize($_SESSION['xsd_parser']['parser']);
$documentId = $manager -> getXsdManagerId();

$mongoConnection = new MongoDBStream();
$mongoConnection -> setDatabaseName("xsdmgr");
$mongoConnection -> openDB();

$mongoConnection -> insertXmlWithId($xmlString, $documentId, "experiment");