<?php
/**
 * 
 *	Return code:
 * 	* 0 OK, rewrite attributes
 * 	* 1 OK, do not rewrite attributes
 * 	* n (n<0) An error occured
 */
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

if(isset($_GET['id']) && isset($_GET['minOccurs']) && isset($_GET['maxOccurs']))
{
	// Create main variable
	$tree = unserialize($_SESSION['xsd_parser']['tree']);
	$element = $tree->getObject($_GET['id']);
	
	if($element) $elementAttr = $element->getAttributes();
	else 
	{
		//todo display an error message
	}
	
	// Pre-computing to avoid undefined error and such things
	if(!isset($elementAttr['MINOCCURS'])) $minOccurs = 1;
	else $minOccurs = $elementAttr['MINOCCURS'];
	
	if(!isset($elementAttr['MAXOCCURS'])) $maxOccurs = 1;
	else $maxOccurs = $elementAttr['MAXOCCURS'];
	
	if($_GET['maxOccurs']==-1) $_GET['maxOccurs'] = "unbounded";
	
	// Determine wether or not we have to rewrite the attributes
	$hasAttrChanged = false;
	if($_GET['minOccurs']!=$minOccurs) $hasAttrChanged=true;
	if(!$hasAttrChanged && $_GET['maxOccurs']!=$maxOccurs) $hasAttrChanged=true;
	
	
	if($hasAttrChanged)
	{
		$elementAttr['MINOCCURS'] = $_GET['minOccurs'];
		$elementAttr['MAXOCCURS'] = $_GET['maxOccurs'];
		
		$tree->getObject($_GET['id'])->setAttributes($elementAttr);
		$_SESSION['xsd_parser']['tree'] = serialize($tree);
		
		$html = htmlspecialchars(displayAttributes($tree, $_GET['id']));
		echo buildJSON($html, 0);
	}
	else
	{
		// todo send 1->nothing has to be rewrite
	}
}

?>