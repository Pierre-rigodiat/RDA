<?php

require_once '../../MongoDB/mongodb.php';
require_once '../../MongoDB/xml2json/parker.php';
require_once '../../MongoDB/xml2json/badgerFish.php';
require_once '../../MongoDB/xml2json/spark.php';
require_once '../../MongoDB/xml2json/gData.php';
require_once '../../MongoDB/xml2json/jsonML.php';


function selectData($match) {
	$query = $_GET['query'];
	switch ($query) {
		case "diffusingSpecies" :
			return array("experiment.experimentType.tracerDiffusivity.diffusingSpecies.element.$" => $match);
			break;
		case "materialName" :
			return array("experiment.experimentType.tracerDiffusivity.material.materialName.$" => $match);
			break;
		case "constituentElement" :
			return array("experiment.experimentType.tracerDiffusivity.material.Composition.constituents.element" => array('$elemMatch' =>array ("$" => $match)));
			break;
	}
}

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


$db = new MongoDBStream ("127.0.0.1","test");
$db->openDB();

if (!isset($_GET['match'])) {
	$queryPath = $_GET;
	$query = selectQuery($queryPath);
	//print_r($query);
}
else {
	$match = $_GET['match'];
	if (is_numeric($match)) {
		$match += 0;
	}
	$query = selectData($match);
}


$cursor = $db->queryData($query, "test");

$echo = '';

if (!$cursor->hasNext()) {
	echo "Empty result for the query";
}
else {
	foreach ($cursor as $doc) {
		$echo .= '<div class="block">'.nl2br(htmlspecialchars(decodeBadgerFish($doc)->saveXml())).'</div>';
	}
	echo $echo;
}

?>