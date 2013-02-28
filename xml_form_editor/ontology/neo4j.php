<?php

require("../inc/db/neo4j/neo4jphp.phar");

$testQuery = "";

$unitType = array("UnitOfMeasureType", "Name");
$unit = array("Unit", "Name");
$xUnit = array("XUnit", "Name");
$yUnit = array("YUnit", "Name");
$qUnit = array("QUnit", "Name");
$d0Unit = array("D0Unit", "Name");
$spaceGroup = array("SpaceGroup", "SymbolOrNumber");

$element = array($_GET["parent"], $_GET["node"]);

if (array_diff($element, $spaceGroup) == array()) {
	$testQuery = "g.V.has('name','CrystalLattice').in('subClassOf').name";
}
if (array_diff($element, $unitType) == array()) {
	$testQuery = "g.V.has('name','UnitOfMeasure').in('subClassOf').name";
}
if (array_diff($element, $unit) == array() || array_diff($element, $xUnit) == array() || array_diff($element, $yUnit) == array() || array_diff($element, $qUnit) == array() ||array_diff($element, $d0Unit) == array()) {
	$testQuery = "g.V.has('name','UnitOfMeasure').in('subClassOf').in('type').name";
}

if ($testQuery != "") {	
		// Connecting to the default port 7474 on localhost
		try
		{
			$client = new Everyman\Neo4j\Client();
			
			// Connecting to a different port or host
			//$client = new Everyman\Neo4j\Client('host.example.com', 7575);
			
			// Connecting using HTTPS and Basic Auth
			/*$client = new Everyman\Neo4j\Client();
			$client->getTransport()
			  ->useHttps()
			  ->setAuth('username', 'password');*/
			
			$client->getServerInfo(); // Test to throw the exception if the client is not connected
		}
		catch(Exception $e)
		{
			echo '<div class="error">Impossible to connect to the server</div>';
			exit;
		}
		
		// The following query searches every node
		//$testQuery='fail';
		$expectedNumberOfEntries=23;
		
		try
		{
			$query = new Everyman\Neo4j\Gremlin\Query($client, $testQuery);
			$resultSet = $query->getResultSet();
			
			/*foreach ($resultSet as  $result) {
				var_dump($result[0]);
			}*/
		}
		catch(Exception $e)
		{
			echo '<div class="error">Gremlin query "'.$testQuery.'" failed</div>';
			exit;
		}

	$pattern = $_GET["term"];
	$match = array();
	if ($resultSet) {
	foreach($resultSet as  $result) {
	   if (($buffer = $result[0]) !== false) {
		if (stristr($buffer,$pattern) !== false)
			array_push($match, trim($buffer));
		}
	   }
	}
	if ($match[0] != null)
		echo implode(",", $match);
}
else echo "";
?>
