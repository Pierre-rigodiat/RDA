<?php
	session_start();
	require("../inc/db/mongodb/MongoDBStream.php");
	require("../parser/core/XsdElement.php");
	require("../parser/core/Tree.php");

?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>

	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	<title>Tree saver</title>
</head>
<body id="content-wrapper">
	<h1>Tree saver</h1>
	<?php		
		$parentElement = new XsdElement('XSD:ELEMENT', array("name" => "parent"));
		$child_1 = new XsdElement('XSD:ELEMENT', array("minOccurs" => "0", "maxOccurs" => "unbounded", "type" => "xsd:integer", "name" => "child1"));
		$child_2 = new XsdElement('XSD:ELEMENT', array("minOccurs" => "0", "type" => "xsd:string", "name" => "child2"));
		
		$tree = new Tree("test-tree");
		$parentIndex = $tree -> insert($parentElement);
		$tree -> insert($child_1, $parentIndex);
		$tree -> insert($child_2, $parentIndex);
		
		$treeArray = $tree -> __toArray();
		
		$mongoDbStream = null;
		
		// Connecting to the default port on localhost
		try
		{
			$mongoDbStream = new MongoDBStream();
			$mongoDbStream -> setDatabaseName("xsdmgr");
			$mongoDbStream -> openDB();
			
			//$cfgCollection = $mongoDbStream -> getCollection("config-test");
			
			echo '<div class="success">Connexion successfull</div>';
		}
		catch(Exception $e)
		{
			echo '<div class="error">Impossible to connect to the server</div>';
			exit;
		}
		
		$treeToInsert = array('_id' => "test_tree", 'tree' => $treeArray);
		
		$mongoDbStream -> insertJson($treeToInsert, "config-test");
	?>	
</body>
</html>
