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
	
	<title>Tree loader</title>
</head>
<body id="content-wrapper">
	<h1>Tree loader</h1>
	<?php
		$mongoDbStream = null;
		
		// Connecting to the default port on localhost
		try
		{
			$mongoDbStream = new MongoDBStream();
			$mongoDbStream -> setDatabaseName("xsdmgr");
			$mongoDbStream -> openDB();
			
			echo '<div class="success">Connexion successfull</div>';
		}
		catch(Exception $e)
		{
			echo '<div class="error">Impossible to connect to the server</div>';
			exit;
		}
		
		$resultCursor = $mongoDbStream -> queryData(array("_id" => "test_tree"), "config-test");
		$resultArray = iterator_to_array($resultCursor);
		
		if(count($resultArray) == 1)
		{
			var_dump($resultArray);
			
			$tree = $resultArray[0]["tree"];
			$elementList = $tree["elementList"];
			$ancestorTable = $tree["ancestorTable"];
			
			$trueElementList = array();
			foreach ($elementList as $element) {
				$trueElementList[$element["_id"]] = new XsdElement($element["element"]["type"],$element["element"]["attr"]);
			}
			
			$tree = new Tree("test");
			$tree -> setTree($trueElementList, $ancestorTable);
			
			var_dump($tree);
			
			$el = $tree -> getElementList();
			echo $el[1];
		}		
	?>	
</body>
</html>
