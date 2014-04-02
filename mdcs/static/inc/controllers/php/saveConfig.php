<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/db/mongodb/MongoDBStream.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/XsdManager.php';

if(isset($_SESSION['xsd_parser']['parser']))
{
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	$originalTree = $manager -> getXsdOriginalTree();
	$pageHandler = $manager -> getPageHandler();
	$moduleHandler = $manager -> getModuleHandler();
	
	$mongoDbStream = null;
	
	// Connecting to the default port on localhost
	try
	{
		$mongoDbStream = new MongoDBStream();
		$mongoDbStream -> setDatabaseName("xsdmgr");
		$mongoDbStream -> openDB();
		
		
		//echo '<div class="success">Connexion successfull</div>';
	}
	catch(Exception $e)
	{
		//echo '<div class="error">Impossible to connect to the server</div>';
		exit;
	}
	
	$filename = $manager -> getSchemaFileName();
	$pathElement = explode('/', $filename);
	$schemaId = $pathElement[count($pathElement)-1];
	
	$configToInsert = array(
		'_id' => $schemaId,
		'namespaces' => $manager -> getNamespaces(),
		'pageHandler' => $pageHandler -> __toArray(),
		'moduleHandler' => $moduleHandler -> __toArray(),
		'tree' => $originalTree -> __toArray());
	$mongoDbStream -> insertJson($configToInsert, "config");
}




