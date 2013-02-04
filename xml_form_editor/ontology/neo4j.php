<?php

require("../inc/db/neo4j/neo4jphp.phar");

$search = "";
$relation = "";

$unit = array("unitOfMeasureType", "name");
$crystal = array("crystalStructure", "name");
$form = array("materialForm", "name");
$phase = array("phase", "name");

$element = array($_GET["parent"], $_GET["node"]);

if (array_diff($element, $crystal) == array()) {
	$search = "CrystalLattice";
	$relation = "subClassOf";
}
if (array_diff($element, $form) == array()) {
	$search = "MaterialForm";
	$relation = "type";
}
if (array_diff($element, $phase) == array()) {
	$search = "MaterialPhaseComposition";
	$relation = "subClassOf";
}
if (array_diff($element, $unit) == array()) {
	$search = "UnitOfMeasure";
	$relation = "subClassOf";
}

if ($search != "") {	
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
		$testQuery = "g.V.has('name','".$search."').in('".$relation."').name";
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
