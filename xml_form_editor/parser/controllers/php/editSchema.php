<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdParser.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';
/**
 * 
 *	Return code:
 * 	* 0 OK, rewrite attributes
 * 	* 1 OK, do not rewrite attributes
 * 	* n (n<0) An error occured
 */
//TODO Avoid to directly use 'xsd' into the code


if(isset($_GET['id']) && isset($_GET['minOccurs']) && isset($_GET['maxOccurs']))
{
	// Create main variable
	$tree = unserialize($_SESSION['xsd_parser']['xsd_tree']);
	$element = $tree->getObject($_GET['id']);
	
	if($element) $elementAttr = $element->getAttributes();
	else 
	{
		echo buildJSON('Element with ID '.$_GET['id'].' does not exist in the current tree', -1);
		exit;
	}
	
	// Pre-computing to avoid undefined error and such things
	if(!isset($elementAttr['MINOCCURS'])) $minOccurs = 1;
	else $minOccurs = $elementAttr['MINOCCURS'];
	
	if(!isset($elementAttr['MAXOCCURS'])) $maxOccurs = 1;
	else $maxOccurs = $elementAttr['MAXOCCURS'];
	
	if(!isset($elementAttr['TYPE'])) $dataType = null;
	else $dataType = $elementAttr['TYPE'];
	
	if(!isset($elementAttr['AUTO_GENERATE'])) $autoGen = null;
	else $autoGen = $elementAttr['AUTO_GENERATE'];
	
	if($_GET['maxOccurs']==-1) $_GET['maxOccurs'] = "unbounded";
	
	// Determine wether or not we have to rewrite the attributes
	$hasAttrChanged = false;
	if($_GET['minOccurs']!=$minOccurs) $hasAttrChanged=true;
	if(!$hasAttrChanged && $_GET['maxOccurs']!=$maxOccurs) $hasAttrChanged=true;
	if(!$hasAttrChanged && isset($_GET['dataType']) && 'xsd:'.$_GET['dataType']!=$dataType) $hasAttrChanged=true;
	if(!$hasAttrChanged && isset($_GET['autoGen']) && $_GET['autoGen']!=$autoGen) $hasAttrChanged=true; //TODO Use autogenerate with the pattern like $attr['AUTO_GENERATE']=$pattern
	
	if($hasAttrChanged)
	{
		$elementAttr['MINOCCURS'] = $_GET['minOccurs'];
		$elementAttr['MAXOCCURS'] = $_GET['maxOccurs'];
		
		if(isset($_GET['dataType'])) $elementAttr['TYPE'] = 'xsd:'.$_GET['dataType'];
		if(isset($_GET['autoGen']) /*&& isset($_GET['pattern'])*/)
		{
			$elementAttr['AUTO_GENERATE'] = $_GET['autoGen'];
			if($elementAttr['AUTO_GENERATE']=='false') unset($elementAttr['AUTO_GENERATE']);
		}
		
		$tree->getObject($_GET['id'])->setAttributes($elementAttr);
		$_SESSION['xsd_parser']['xsd_tree'] = serialize($tree);
		
		// Updates the xml tree within the parser
		$parser = unserialize($_SESSION['xsd_parser']['parser']);
		$parser->setXmlTree($tree);
		$_SESSION['xsd_parser']['parser'] = serialize($parser);
		
		// Unset the xml tree to allow update
		unset($_SESSION['xsd_parser']['xml_tree']);
		
		$html = htmlspecialchars(displayAttributes($tree, $_GET['id']));
		echo buildJSON($html, 0);
	}
	else
	{
		echo buildJSON('ID '.$_GET['id'].' does not need to be rewritten', 1);
	}
}

?>