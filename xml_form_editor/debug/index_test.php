<?php
	session_start();


?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr">
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	<script src="parser/controllers/js/addRemove.js"></script>
	<script src="resources/js/php.js"></script>
	
	<title>Parser Impl v0.1</title>
</head>
<body>
	<?php
		require_once 'parser/core/XsdElement.php';
		
		/**
		 * XsdElement tests
		 */
		/*$element_1 = new XsdElement('Lol', array(), true);
		$element_2 = new XsdElement(3, null, false);
		$element_3 = new XsdElement('Lol', array(), false);
		$element_4 = new XsdElement('Lol', 3);
		$element_5 = new XsdElement('Lol', array('/[0-9]+/'));
		
		// At this point elements 1, 3 and 5 are set
		$element_1->setAttributes(array(12, 13));
		$element_1->setAttributes(array(14, 'ExperimentType'));
		
		$type = $element_1->getType();
		$attr = $element_1->getAttributes();
		echo 'Element 1 has type '.$type.' and attr '.serialize($attr).'<br/>';
		
		var_dump($element_1);
		var_dump($element_3);
		var_dump($element_5);
		
		$element_1->compare(12);
		$element_1->compare('test');
		$element_1->compare($element_5);*/
		
		/**
		 * Parser tests
		 */
		require_once 'parser/core/XsdManager.php';
		require_once 'parser/view/XsdDisplay.php';
	
		$schemaFile = 'resources/files/demo.xsd';
		
		/*$parser = new XsdManager();
		$parser = new XsdManager(0);
		$parser = new XsdManager('test', 12);*/
		
		$parser = new XsdManager($schemaFile, true);
		
		$rootElementsArray = $parser->parseXsdFile();
		
		//var_dump($rootElementsArray);
		
		$parser->buildTree($rootElementsArray[0]);
		
		$tree = $parser->getXmlFormTree();
		$_SESSION['app']['tree'] = serialize($tree);
		
		$display = new XsdDisplay($tree, true);
	?>
	<h1>Configuration view</h1>
	<?php
		echo $display->displayConfiguration();
	?>
	<hr/>
	<h1>HTML Form View</h1>
	<?php
		echo $display->displayHTMLForm();
	?>
	<hr/>
	<h1>XML View</h1>
	<?php
		//$display->displayXMLTree();
	?>
</body>
</html>