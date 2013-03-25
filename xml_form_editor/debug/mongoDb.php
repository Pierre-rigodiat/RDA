<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>

	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	<title>MongoDB Tester</title>
</head>
<body id="content-wrapper">
	<h1>MongoDB Tester</h1>
	<?php
		require("../inc/db/mongodb/mongodb.php");
		
		$sectionCollection = null;
		
		// Connecting to the default port on localhost
		try
		{
			$mongoDbStream = new MongoDBStream();
			$mongoDbStream -> setDatabaseName("website");
			$mongoDbStream -> openDB();
			
			$sectionCollection = $mongoDbStream -> getCollection("sections");
			
			echo '<div class="success">Connexion successfull</div>';
		}
		catch(Exception $e)
		{
			echo '<div class="error">Impossible to connect to the server</div>';
			exit;
		}
		
		try
		{
			$query = array(
				"name" => "admin"
			);
			
			$queryCursor = $sectionCollection -> find();
			var_dump(iterator_to_array($queryCursor));
		}
		catch(Exception $e)
		{
			echo '<div class="error">Impossible to connect to the server</div>';
			exit;
		}
	?>	
</body>
</html>
