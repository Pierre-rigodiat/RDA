<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>

	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	<title>Neo4j Tester</title>
</head>
<body id="content-wrapper">
	<h1>Neo4j Tester</h1>
	<?php
		require("../inc/db/neo4j/neo4jphp.phar");
		
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
			echo '<div class="success">Connexion successfull</div>';
		}
		catch(Exception $e)
		{
			echo '<div class="error">Impossible to connect to the server</div>';
			exit;
		}
		
		// The following query searches every node with a name begginning with "Material"
		$testQuery = "g.V.hasNot('name', null).filter{it.name.matches('Material.*')}.name";
		//$testQuery='fail';
		$expectedNumberOfEntries=23;
		
		try
		{
			$query = new Everyman\Neo4j\Gremlin\Query($client, $testQuery);
			$resultSet = $query->getResultSet();
			
			if(count($resultSet)==$expectedNumberOfEntries)
			{
				echo '<div class="success">Query return the correct number of element</div>';
				
				echo '<u>Result(s) for query :</u><b>'.$testQuery.'</b><br/>';
				foreach ($resultSet as  $result) {
					var_dump($result[0]);
				}
				
			}
			else 
			{
				echo '<div class="warn">'.count($resultSet).' / '.$expectedNumberOfEntries.' element(s) returned</div>';
				
				// TODO Add more explanation
				/*$problem = false;
				foreach ($expectedEntries as $entry) {
					if(!in_array($entry, $result['data']))
					{
						$problem = true;
						echo '<div class="error">Element "'.$entry.'" not found</div>';
					}
				}*/
			}
			
			
		}
		catch(Exception $e)
		{
			echo '<div class="error">Gremlin query "'.$testQuery.'" failed</div>';
		}
		 
		
	?>	
</body>
</html>
