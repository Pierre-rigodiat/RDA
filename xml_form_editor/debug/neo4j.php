<?php
	require("../inc/db/neo4j/neo4jphp.phar");


	// Connecting to the default port 7474 on localhost
	$client = new Everyman\Neo4j\Client();
	var_dump($client -> getServerInfo());
	
	// Connecting to a different port or host
	//$client = new Everyman\Neo4j\Client('host.example.com', 7575);
	
	// Connecting using HTTPS and Basic Auth
	/*$client = new Everyman\Neo4j\Client();
	$client->getTransport()
	  ->useHttps()
	  ->setAuth('username', 'password');*/
	 
	// The following query searches every node with a name begginning with "Material"
	$testQuery = "g.V.hasNot('name', null).filter{it.name.matches('Material.*')}.name";
	$query = new Everyman\Neo4j\Gremlin\Query($client, $testQuery);
	$result = $query->getResultSet();
	
	var_dump($result);
	
	echo count($result).'/23 result found';
?>