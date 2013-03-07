<?php
/**
 * Load a correct configuration for the demo schema. The purpose of this tool is to avoid
 * Material Scientists to redo all the configuration if the session is closed
 */

session_start();

unset($_SESSION['xsd_parser']);

require_once '../parser/parser.inc.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/debug/lib/loadingFunctions.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';

// Load the schema
$fileToLoad = '/resources/files/schemas/demo.diffusion.xsd';
$nbPages = 7;

loadSchema($_SESSION['xsd_parser']['conf']['dirname'].$fileToLoad, $nbPages);

// Get all interesting information
$xsdManager = unserialize($_SESSION['xsd_parser']['parser']);
$xsdManager -> buildCompleteTree();

$xsdTree = $xsdManager -> getXsdCompleteTree();
$pageHandler = $xsdManager -> getPageHandler();
$moduleHandler = $xsdManager -> getModuleHandler();

// Set the pages
$pageArray = array(
	2 => array(
		6, 614, 1277
	),
	3 => array(
		189,320
	),
	4 => array(
		372
	),
	5 => array(
		388
	),
	6 => array(
		490
	),
	7 => array(
		535
	)
);

foreach($pageArray as $page => $idArray)
{
	foreach($idArray as $elementId)
	{
		echo 'Setting page for '.$elementId.'...';
		
		$pageHandler -> removePagesForId($elementId);
		$pageHandler -> setPageForId($page, $elementId);
		
		$elderId = $xsdTree -> getParent($elementId);	
		// Set up elder in the same page
		while($elderId!=-1) // While we are not at the root position
		{
			$pageHandler -> removePagesForId($elderId);
			$children = $xsdTree -> getChildren($elderId);
			
			$pageArray = array();
			foreach($children as $child)
			{
				$childPageArray = $pageHandler -> getPageForId($child);
				if(count($childPageArray) > 0)
				{
					foreach ($childPageArray as $childPage) {
						if(!in_array($childPage, $pageArray))
							array_push($pageArray, $childPage);
					}
				}
				else if(!in_array(1, $pageArray)) array_push($pageArray, 1);
			}
			
			foreach($pageArray as $page)
			{
				$pageHandler -> setPageForId($page, $elderId);
			}
			
			$elderId = $xsdTree -> getParent($elderId);
		}		
		
		setUpChildrenToPage($pageHandler, $xsdTree, $elementId, $page);
		
		echo 'Page set for '.$elementId;
	}
}

// Set the module
$moduleHandler -> setModuleStatus('table', true);
$moduleHandler -> setIdWithModule(523, 'table');


// Save the xsdManager
$xsdManager -> setModuleHandler($moduleHandler);
$xsdManager -> setPageHandler($pageHandler);
$_SESSION['xsd_parser']['parser'] = serialize($xsdManager);

echo 'Schema loaded';
