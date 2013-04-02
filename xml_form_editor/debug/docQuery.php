<!DOCTYPE html>
<html>
<head>

	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js"></script>
	
	<script src="front/ptester.js"></script>
	<script src="../inc/controllers/js/php.js"></script>
	
	<title>Query Tester</title>
</head>
<body id="content-wrapper">
	<span id="top_page"></span>
	<h1>Query Handler</h1>
	<div id="page_content">
	<div class="block">
<?php

session_start();

require_once dirname(__FILE__).'/../parser/parser.conf.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/ModuleHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/SearchHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';


$numberOfPage = 1;
$debug = false;
$moduleDir = null;
$schemaFolder = '../resources/files/schemas';
$schemaFilename = $schemaFolder.'/demo.diffusion.xsd';

// Build the page handler
$pHandler = new PageHandler($numberOfPage, $debug);

// Build the module handler
$mHandler = new ModuleHandler($moduleDir, $debug);

// Parse the file
$manager = new XsdManager($schemaFilename, $pHandler, $mHandler, $debug);
$rootElementsArray = $manager->parseXsdFile();
$manager->buildOrganizedTree($rootElementsArray[0]);
$manager->buildQueryTree();

// Build the search handler
$search = $manager->getSearchHandler();
$search->setIdArray(array(5,16,27,159,170,181,192,336,347,369,513,515));

$_SESSION['xsd_parser']['parser'] = serialize($manager);

$display = new Display($manager);

/*if($manager) var_dump($manager);
else echo 'Parser variables not set';*/

if ($display) {
$_SESSION['xsd_parser']['display'] = serialize($display);
echo $display->displayQuery();
}

/*if($manager)
	{
		$pre = '';
		$queryTree = $manager->getXsdQueryTree();
		$queryElements = $queryTree->getElementList();
		//var_dump($originalTree);
		echo '<ul>';
		
		foreach ($queryElements as $elementId => $treeLeaf) {
			echo '<li>';
			$queryLeaf = $queryTree->getElement($elementId);
			
			echo 'id = '.$elementId.', ';
			
			echo 'type = '.$queryLeaf->getType();
			$leafAttr = $queryLeaf->getAttributes();
				
				if ($leafAttr != null) {
					echo ', {';
					$attr = '';
					foreach ($leafAttr as $key => $value) {
						echo $attr.$key.' = ';
						
						$attrEnum = '';
						if (is_array($value)) {
							echo '(';
							foreach ($value as $enum) {
								echo $attrEnum.$enum;
								$attrEnum = ', ';
							}
							echo ')';
						}
						else echo $value;
						
						$attr = ' | ';
					}
					
					echo '}';
				}
			
			echo '</li>';
		}
		
		echo '</ul>';
	}
else echo 'XsdManager not set';*/
?>
	</div>
	<div class="icon legend retrieve query">Submit Query</div>
	<div id="query_result"></div>
	</div>
</body>
</html>