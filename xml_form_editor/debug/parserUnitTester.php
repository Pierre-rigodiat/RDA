<?php
	session_start();
	require_once 'lib/simpletest/autorun.php';
	require_once '../parser/parser.inc.php';
?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	<title>XsdElement tester</title>
</head>
<body id="content-wrapper">
	<a href="http://www.simpletest.org/">SimpleTest</a>
	<?php
		class RunTests extends TestSuite {			
		    function RunTests() {
		    	$this->TestSuite('Run all tests');
		        $this->addFile('UnitTest/XsdElementUnitTest.php');
				//$this->addFile('UnitTest/TreeUnitTest.php');
		    }
		}
	?>
</body>