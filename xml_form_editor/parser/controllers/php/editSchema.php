<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';
/**
 * 
 *	Return code:
 * 	* 0 OK, rewrite attributes
 * 	* 1 OK, do not rewrite attributes
 * 	* n (n<0) An error occured
 */
// TODO Avoid to directly use 'xsd' into the code
// TODO Implement the autogeneration pattern
// todo check tree action to improve code

function setUpChildrenToPage($pHandler, $tree, $elementId, $pageId)
{	
	$children = $tree -> getChildren($elementId);
	
	foreach($children as $child)
	{
		$pHandler -> removePagesForId($child);
		$pHandler -> setPageForId($pageId, $child);
		setUpChildrenToPage($pHandler, $tree, $child, $pageId);
	}
}

function setUpChildrenToModule($manager, $tree, $elementId, $moduleName)
{
	$children = $tree -> getChildren($elementId);
	
	foreach($children as $child)
	{
		$manager -> assignIdToModule($child, $moduleName);
		setUpChildrenToModule($manager, $tree, $child, $moduleName);
	}
}


if(isset($_GET['id']) && isset($_GET['minOccurs']) && isset($_GET['maxOccurs']))
{
	if(!isset($_SESSION['xsd_parser']['parser']))
	{
		buildJSON('Parser not set', -1);
		exit;
	}
	
	// Get the parser and modify the organized tree
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	$xsdOrganizedTree = $manager -> getXsdOrganizedTree();
	$xsdOriginalTree = $manager -> getXsdOriginalTree();
	
	$originalTreeId = $xsdOrganizedTree->getObject($_GET['id']);
	$element = $xsdOriginalTree->getObject($originalTreeId);
	
	if($element) $elementAttr = $element->getAttributes();
	else // $xsdOrganizedTree -> getObject($_GET['id']) sent an error
	{
		echo buildJSON('Element with ID '.$_GET['id'].' does not exist in the current tree', -2);
		exit;
	}
	
	// Pre-computing to avoid undefined error
	if(!isset($elementAttr['MINOCCURS'])) $minOccurs = 1;
	else $minOccurs = $elementAttr['MINOCCURS'];
	
	if(!isset($elementAttr['MAXOCCURS'])) $maxOccurs = 1;
	else $maxOccurs = $elementAttr['MAXOCCURS'];
	
	if(!isset($elementAttr['TYPE'])) $dataType = null;
	else $dataType = $elementAttr['TYPE'];
	
	if(!isset($elementAttr['AUTO_GENERATE'])) $autoGen = null;
	else $autoGen = $elementAttr['AUTO_GENERATE'];
	
	// TODO Change the condition
	/*if(!isset($elementAttr['MODULE'])) $module = 'false';
	else $module = $elementAttr['MODULE'];*/
	
	// TODO Change the condition
	/*if(!isset($elementAttr['PAGE'])) $page = 1;
	else $page = $elementAttr['PAGE'];*/
	
	if($_GET['maxOccurs']==-1) $_GET['maxOccurs'] = "unbounded";
	
	// Determine wether or not we have to rewrite the attributes
	$hasAttrChanged = false;
	if($_GET['minOccurs']!=$minOccurs) $hasAttrChanged=true;
	if(!$hasAttrChanged && $_GET['maxOccurs']!=$maxOccurs) $hasAttrChanged=true;
	if(!$hasAttrChanged && isset($_GET['dataType']) && 'xsd:'.$_GET['dataType']!=$dataType) $hasAttrChanged=true;
	if(!$hasAttrChanged && isset($_GET['autoGen']) && $_GET['autoGen']!=$autoGen) $hasAttrChanged=true; //TODO Use autogenerate with the pattern like $attr['AUTO_GENERATE']=$pattern
	if(!$hasAttrChanged && isset($_GET['module'])/* && $_GET['module']!=$module*/) $hasAttrChanged=true;
	if(!$hasAttrChanged && isset($_GET['page']) /*&& $_GET['page']!=$page*/) $hasAttrChanged=true;
	
	if($hasAttrChanged)
	{
		if($_GET['minOccurs']==1) unset($elementAttr['MINOCCURS']);
		else $elementAttr['MINOCCURS'] = $_GET['minOccurs'];
		if($_GET['maxOccurs']==1) unset($elementAttr['MAXOCCURS']);
		else $elementAttr['MAXOCCURS'] = $_GET['maxOccurs'];
		
		if(isset($_GET['dataType'])) $elementAttr['TYPE'] = 'xsd:'.$_GET['dataType'];
		if(isset($_GET['autoGen']) /*&& isset($_GET['pattern'])*/) // TODO Implement the pattern
		{
			$elementAttr['AUTO_GENERATE'] = $_GET['autoGen'];
			if($elementAttr['AUTO_GENERATE']=='false') unset($elementAttr['AUTO_GENERATE']);
		}
		
		/*if($_GET['module'] == 'false') unset($elementAttr['MODULE']);
		else $elementAttr['MODULE'] = $_GET['module'];*/
		
		if(isset($_GET['page']))
		{
			// FIXME Do that in the manager by using XsdManager::assignPageToId
			/*** START ***/
			$pHandler = $manager -> getPageHandler();
			$pHandler -> removePagesForId($_GET['id']);
			$pHandler -> setPageForId($_GET['page'], $_GET['id']);
			
			$elderId = $xsdOrganizedTree -> getParent($_GET['id']);
			
			// Set up elder in the same page
			while($elderId!=-1) // While we are not at the root position
			{
				$pHandler -> removePagesForId($elderId);
				$children = $xsdOrganizedTree -> getChildren($elderId);
				
				$pageArray = array();
				foreach($children as $child)
				{
					$childPageArray = $pHandler -> getPageForId($child);
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
					$pHandler -> setPageForId($page, $elderId);
				}
				
				$elderId = $xsdOrganizedTree -> getParent($elderId);
			}
			
			// Set up the children
			setUpChildrenToPage($pHandler, $xsdOrganizedTree, $_GET['id'], $_GET['page']);
			
			
			$manager -> setPageHandler($pHandler);
			/*** END ***/
		}

		if(isset($_GET['module']))
		{
			if($_GET['module']!='false')
			{
				$manager -> assignIdToModule($_GET['id'], $_GET['module']);
				setUpChildrenToModule($manager, $xsdOrganizedTree, $_GET['id'], $_GET['module']);
				
			}
			else
			{
				// XXX Remove the ID from the module
			}
		}
		
		$xsdOriginalTree->getObject($originalTreeId)->setAttributes($elementAttr);
		$manager -> setXsdOriginalTree($xsdOriginalTree);
		
		$_SESSION['xsd_parser']['parser'] = serialize($manager);
		
		$html = htmlspecialchars(displayAttributes($_GET['id']));
		echo buildJSON($html, 0);
	}
	else
	{
		echo buildJSON('ID '.$_GET['id'].' does not need to be rewritten', 1);
	}
}

?>