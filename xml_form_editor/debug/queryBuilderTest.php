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

/*if (isset($_GET)) {
	$queryId = array();
	foreach ($_GET as $key => $value)
	{
		if (is_numeric($key))
		{
			$queryId[$key]=$value;
		}
	}
	//print_r($queryId);
	$query = selectQuery($queryId);
}*/

$queryId = array();
$queryId[16] = "Al";
$queryId[496] = "Mg";
/*$queryId[17] = 99.9;
$queryId[5] = "Mg";
$queryId[518] = "Ac";
$queryId[519] = "Mg";*/
$query = selectQuery($queryId);

//$query = Array ( 'experiment.experimentType.tracerDiffusivity.material.composition.constituents.element' => Array ( '$all' => Array ( Array('$' => 'Al'), Array('$' => 'Mg') ) ) );
//$query = Array ('$and' => Array( Array(/*'experiment.experimentType.tracerDiffusivity.material.composition.constituents.element' => Array ( '$all' => Array ( Array('$' => 'Ac'), Array('$' => 'Mg') ) )*/ /*), /*Array(*/'experiment.experimentType.tracerDiffusivity.material.composition.constituents.element.$' => 'Ac'), Array('experiment.experimentType.tracerDiffusivity.material.composition.constituents.element.$' => 'Mg') ) );
//$query = Array ('$and' => Array( Array( 'experiment.experimentType.tracerDiffusivity.material.composition.constituents' => Array ( '$elemMatch' => Array ( 'element' => Array( '$all' =>( Array ( Array('$' => 'Al'), Array('$' => 'Mg')))), 'purity.$' => 99.9))),  Array( 'experiment.experimentType.tracerDiffusivity.material.composition.constituents' => Array( '$elemMatch' => Array ( 'element' => Array( '$all' =>( Array ( Array('$' => 'Ac'), Array('$' => 'Mg')))), 'purity.$' => 99.9)))));
//$query = Array ('experiment.experimentType.tracerDiffusivity.material.composition.constituents.quantity.$' => Array ('$lte' => 99.9, '$gte' => 99.9 ) );
print_r($query);

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
