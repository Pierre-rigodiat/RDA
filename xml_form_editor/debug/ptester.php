<?php
	session_start();
?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>

	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/dialog.css" media="screen" />
	
	<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js"></script>
	
	<script src="parser/controllers/js/addRemove.js"></script>
	<script src="parser/controllers/js/edit.js"></script>
	<script src="resources/js/php.js"></script>
	<script src="resources/js/ptester.js"></script>
	
	<title>Parser Impl Tester</title>
</head>
<body id="content-wrapper">
	<?php
		require_once '../parser/parser.inc.php';
		
		$schemaFile = '../resources/files/demo_2.xsd';
		loadSchema($schemaFile);
	?>
	<h1>Parser Implementation Tester</h1>
	<div class="warn">
		The purpose of this tool is to test all parser features and verify that all is working good.	
		This is a debug page, not meant for production purposes. 
	</div>
	<h2>Configuration view</h2>
	<?php
		displayConfiguration();
	?>
	<hr/>
	<h2>HTML Form View <span class="icon refresh"></span></h2>
	<?php
		displayHTMLForm();
	?>
	<hr/>
	<h2>XML View</h2>
	<?php
		//displayXMLTree();
	?>
</body>
</html>