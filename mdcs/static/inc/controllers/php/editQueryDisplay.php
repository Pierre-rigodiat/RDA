<?php
/**
 * <EditQueryDisplay controller>
 */
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';
/**
 * Edit query display controller 
 * 
 *	Return code:
 * 	* 0 OK, rewrite attributes
 * 	* 1 OK, do not rewrite attributes
 * 	* n (n<0) An error occured
 */
// TODO Avoid to directly use 'xsd' into the code
// TODO Implement the autogeneration pattern
// todo check tree action to improve code


/**
 * @ignore
 */
function setUpQueryChildrenToModule($manager, $tree, $elementId, $moduleName)
{
	$children = $tree -> getChildren($elementId);
	
	foreach($children as $child)
	{
		$manager -> assignIdToModule($child, $moduleName, 'query');
		setUpQueryChildrenToModule($manager, $tree, $child, $moduleName);
	}
}


if(isset($_GET['id']))
{
	if(!isset($_SESSION['xsd_parser']['parser']))
	{
		buildJSON('Parser not set', -1);
		exit;
	}
	
	// Get the parser and modify the organized tree
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	//$xsdOrganizedTree = $manager -> getXsdOrganizedTree();
	$xsdQueryTree = $manager -> getXsdQueryTree();
	
	//$originalTreeId = $xsdOrganizedTree->getObject($_GET['id']);
	$element = $xsdQueryTree->getElement($_GET['id']/*$originalTreeId*/);
	
	if(!$element)
	{
		echo buildJSON('Element with ID '.$_GET['id'].' does not exist in the current tree', -2);
		exit;
	}
	
	// TODO Change the condition
	/*if(!isset($elementAttr['MODULE'])) $module = 'false';
	else $module = $elementAttr['MODULE'];*/
	
	// TODO Change the condition
	/*if(!isset($elementAttr['PAGE'])) $page = 1;
	else $page = $elementAttr['PAGE'];*/
	
	// Determine wether or not we have to rewrite the attributes
	$hasAttrChanged = false;
	if(isset($_GET['module'])/* && $_GET['module']!=$module*/) $hasAttrChanged=true;
	
	// TODO see if we can optimize this function
	// XXX use a diff between arrays, and just add new elements
	if($hasAttrChanged)
	{
		if(isset($_GET['module']))
		{
			if($_GET['module']!='false')
			{
				$manager -> assignIdToModule((integer) $_GET['id'], $_GET['module'], 'query');
				setUpQueryChildrenToModule($manager, /*$xsdOrganizedTree*/$xsdQueryTree, (integer) $_GET['id'], $_GET['module']);
				
			}
			else
			{
				// XXX Remove the ID from the module
			}
		}
		
		//$xsdOriginalTree->getObject($originalTreeId)->setAttributes($elementAttr);
		$manager -> setXsdQueryTree($xsdQueryTree);
		
		$_SESSION['xsd_parser']['parser'] = serialize($manager);
		
		$html = htmlspecialchars(displayAdminQuerySubTree((integer) $_GET['id']));
		echo buildJSON($html, 0);
	}
	else
	{
		echo buildJSON('ID '.$_GET['id'].' does not need to be rewritten', 1);
	}
}

?>