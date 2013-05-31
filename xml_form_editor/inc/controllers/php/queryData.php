<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/parser.inc.php';
require_once $_SESSION['config']['_ROOT_'] . '/inc/db/mongodb/MongoDBStream.php';
require_once $_SESSION['config']['_ROOT_'] . '/inc/lib/JsonXmlFunctions.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/QueryBuilder.php';

function selectQuery($queryId) {
	$result = array();
	/*if ($queryPath != array()) {
		foreach ($queryPath as $path => $elem) {
			if ($path != '_')
			$result[str_replace('_','.', $path)]=$elem;
		}
		return $result;
	}*/
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

$db = new MongoDBStream ("127.0.0.1","xsdmgr");
$db->openDB();

$query = array();
$pattern = array(
		'lte' => '/([0-9]+)(lte)/',
		'gte' => '/([0-9]+)(gte)/'
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
		else {
			foreach ($pattern as $id => $idPattern) {
				if (preg_match($idPattern, $key)) {
					$temp = preg_split('/'.$id.'/', $key, -1, PREG_SPLIT_NO_EMPTY);
					$newKey = $temp[0];
					$queryId[$newKey][] = $id.' '.$value;
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
	echo "empty";
}
else {
	$echo = '[';
	foreach ($cursor as $doc) {
		$echo .= '{"data":"'.preg_replace('/[\r\n]/', '', htmlspecialchars(decodeBadgerFish($doc)->saveHTML())).'"},';
	}
	echo substr($echo, 0, strlen($echo)-1).']';
}
?>