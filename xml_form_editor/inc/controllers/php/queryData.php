<?php
session_start();
require_once $_SESSION['config']['_ROOT_'] . '/parser/parser.inc.php';
require_once  $_SESSION['config']['_ROOT_'] . '/inc/db/mongoDB/MongoDBStream.php';
require_once  $_SESSION['config']['_ROOT_'] . '/inc/lib/JsonXmlFunctions.php';
//require_once  $_SESSION['config']['_ROOT_'] . '/MongoDB/xml2json/jsonML.php';



function selectQuery($queryPath) {
	$result = array();
	if ($queryPath != array()) {
		foreach ($queryPath as $path => $elem) {
			if ($path != '_')
			$result[str_replace('_','.', $path)]=$elem;
		}
		return $result;
	}
}


$db = new MongoDBStream ("127.0.0.1","xsdmgr");
$db->openDB();

if (!isset($_GET['match'])) {
	$queryPath = $_GET;
	$query = selectQuery($queryPath);
	//print_r($query);
}


$cursor = $db->queryData($query, "experiment");

$echo = '';

if (!$cursor->hasNext()) {
	echo "Empty result for the query";
}
else {
	foreach ($cursor as $doc) {
		$echo .= nl2br(htmlspecialchars(decodeBadgerFish($doc)->saveXml()));
	}
	echo $echo;
}

?>