<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/parser.inc.php';
require_once $_SESSION['config']['_ROOT_'] . '/inc/db/mongodb/MongoDBStream.php';
require_once $_SESSION['config']['_ROOT_'] . '/inc/lib/JsonXmlFunctions.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/QueryBuilder.php';

function selectQuery($queryId) {
	
	$result = array();
	if(isset($_SESSION['xsd_parser']['parser']))
	{
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		
		$queryTree = $manager->getXsdQueryTree();
		
		$queryBuilder = new QueryBuilder($queryId, $queryTree);
		
		//print_r($queryId);
		//print_r($queryTree);
		$result = $queryBuilder->buildQuery();
	}
	
	return $result;
}

function addOption($elementID, $option) {
	if(isset($_SESSION['xsd_parser']['parser']))
	{
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$queryTree = $manager->getXsdQueryTree();
		$siblings = $queryTree->getSiblings($elementID);
		
		foreach ($siblings as $siblingsID) {
			$optionAttribute = array('OPTION' => $option);
			$siblingElement = $queryTree->getElement($siblingsID)->addAttributes($optionAttribute);
		}
		
		$_SESSION['xsd_parser']['parser'] = serialize($manager);
		
	}
	else {
		throw new Exception("Parser not initialized", -1);
	}
	
}

$db = new MongoDBStream ("127.0.0.1","xsdmgr");
$db->openDB();

$query = array();
$pattern = array(
		'lte' => '/(lte)([0-9]+)/',
		'gte' => '/(gte)([0-9]+)/'
		);

$option = array(
		'all' => true,
		'exact' => true
		);

if (isset($_GET)) {
	$queryId = array();
	foreach ($_GET as $key => $value)
	{
		if (is_numeric($key))
		{
			$value = is_numeric($value) ? $value+0 : $value;
			$queryId[$key] = $value;
		}
		elseif (array_key_exists($key,$option)) {
			try {
				addOption($value, $key);
			}
			catch (Exception $e) {
				
			}
		}
		else {
			foreach ($pattern as $id => $idPattern) {
				if (preg_match($idPattern, $key)) {
					$temp = preg_split('/'.$id.'/', $key, -1, PREG_SPLIT_NO_EMPTY);
					$newKey = array_pop($temp);
					$queryId[$newKey][$id] = $value;
					break;
				}
			}
		}
	}
	//print_r($queryId);
	$query = selectQuery($queryId);
}

//print_r($query);

$cursor = $db->queryData($query, "experiment");

$echo = '';

if (!$cursor->hasNext()) {
	if (isset($_SESSION['xsd_parser']['qresult'])) {
		unset($_SESSION['xsd_parser']['qresult']);
	}
	echo "empty";
}
else {
	$queryResult = '';
	
	$echo = '[';
	foreach ($cursor as $doc) {
		$queryResult .= decodeBadgerFish($doc)->saveHTML();
		$echo .= '{"data":"'.preg_replace('/[\r\n]/', '', htmlspecialchars(decodeBadgerFish($doc)->saveHTML())).'"},';
	}
	$_SESSION['xsd_parser']['qresult'] = serialize($queryResult);
	echo substr($echo, 0, strlen($echo)-1).']';
}
?>