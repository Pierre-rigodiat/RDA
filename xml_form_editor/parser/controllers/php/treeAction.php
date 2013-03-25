<?php
/**
 * <TreeAction controller>
 * 
 * 
 * @package XsdMan\Controllers
 */
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

/**
 * @ignore
 */
function setUpChildrenToPage($pageHandler, $tree, $origElementId, $destElementId)
{
	$origChildren = $tree -> getChildren($origElementId);
	$destChildren = $tree -> getChildren($destElementId);
	
	// FIXME Those 2 line do not belong here, there must be a problem elsewhere
	$origChildren = array_values($origChildren);
	$destChildren = array_values($destChildren);
	/*echo 'Orig: '.count($origChildren).'; Dest: '.count($destChildren);
	print_r($origChildren);
	print_r($destChildren);*/
	
	foreach($destChildren as $id => $child)
	{
		$pageArray = $pageHandler -> getPageForId($origChildren[$id]);
		foreach($pageArray as $page)
		{
			$pageHandler -> setPageForId($page, $child);
		}
		
		setUpChildrenToPage($pageHandler, $tree, $origChildren[$id], $child);
	}
}



//todo optimize script
//todo secure script
//todo add a logger
//todo remove unused require_once
/**
 * Return object for the script
 * {"result":(string)html_code or error_message, "code":(int)return_code}
 * 
 * Return code:
 * 0 		-> All is OK, just copy the text
 * n(<0) 	-> An error occured
 * 
 * 
 * */
 /**
 * @ignore
 */
function getJSONString(/*$parser, $xsdCompleteTree, */$elementId)
{
	/*$parser -> setXsdCompleteTree($xsdCompleteTree);
	$_SESSION['xsd_parser']['parser'] = serialize($parser);*/
	
	$htmlCode = htmlspecialchars(displayTree($elementId));
	
	if(isset($htmlCode))
	{
		return buildJSON($htmlCode, 0);
	}
	else 
	{
		return buildJSON('No display or parser configured', -3);
	}
}

if(isset($_GET['action']) && isset($_GET['id']) && isset($_SESSION['xsd_parser']['parser']))
{
	// Create main variable
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	$xsdCompleteTree = $manager -> getXsdCompleteTree();
	//$xsdOriginalTree = $manager -> getXsdOriginalTree();
	
	$element = $xsdCompleteTree->getElement($_GET['id']);
	//$element = $xsdOriginalTree->getObject($originalTreeId);
	
	// Check that we actually got an existing element
	if($element) $elementAttr = $element->getAttributes();
	else // $tree->getObject() returns null
	{
		echo buildJSON('Id '.$_GET['id'].' does not exist inside the current tree', -1);
		exit;
	}
	
	// Other variables
	$parentId = $xsdCompleteTree->getParent($_GET['id']);
	$grandParentId = $xsdCompleteTree->getParent($parentId);
	
	// Check that this part of the tree is not unavailable
	$elderId = $xsdCompleteTree->getParent($_GET['id']);
	$elderObject = $xsdCompleteTree->getElement($elderId);
	$elderAttributes = $elderObject->getAttributes();
	
	$isElderAvailable = !(isset($elderAttributes['AVAILABLE']) && !$elderAttributes['AVAILABLE']);
	
	while($isElderAvailable && $elderId!=0)
	{
		$elderId = $xsdCompleteTree->getParent($elderId);
		$elderObject = $xsdCompleteTree->getElement($elderId);
		$elderAttributes = $elderObject->getAttributes();
		
		$isElderAvailable = !(isset($elderAttributes['AVAILABLE']) && !$elderAttributes['AVAILABLE']);
	}
	
	if(!$isElderAvailable) 
	{
		$htmlCode = htmlspecialchars(displayTree($grandParentId));
		echo buildJSON($htmlCode, $elderId);
		
		exit;
	}		
	
	// Retrieving the number of current siblings
	$siblingCount = count($xsdCompleteTree -> getSiblings($_GET['id']));
	
	/**
	 * 
	 */
	switch($_GET['action'])
	{
		case 'a': /*Adding an element*/
			if(isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE']) // Element is not available (it needs to be set as available)
			{
				$availabilityAttr = array('AVAILABLE'=>true);
				$removeResult = $xsdCompleteTree->getElement($_GET['id'])->addAttributes($availabilityAttr);
				//$removeResult = $xsdOriginalTree->getObject($originalTreeId)->addAttributes($availabilityAttr);
				
				// xxx change to original tree
				$manager -> setXsdCompleteTree($xsdCompleteTree);
				//$manager -> setXsdOriginalTree($xsdOriginalTree);
				$_SESSION['xsd_parser']['parser'] = serialize($manager);
				
				echo getJSONString($grandParentId);
			}
			else // Element is available (it needs a new element)
			{
				// Check the maximum element we could have
				if(isset($elementAttr['MAXOCCURS']) && is_numeric($elementAttr['MAXOCCURS'])) $maxOccurs = $elementAttr['MAXOCCURS'];
				else if($elementAttr['MAXOCCURS']=='unbounded') $maxOccurs = -1;
				else $maxOccurs = 1;
				
				if($maxOccurs==-1 || $maxOccurs>$siblingCount)
				{
					$elementId = $xsdCompleteTree->duplicate($_GET['id'], true);
					$xsdCompleteTree -> setBrother($_GET['id'], $elementId);
				
					if($elementId>=0)
					{
						$manager -> setXsdCompleteTree($xsdCompleteTree);
						//$manager -> setXsdOriginalTree($xsdOriginalTree);
						
						$pageHandler = $manager -> getPageHandler();
						$pageArray = $pageHandler -> getPageForId($_GET['id']);
						
						foreach($pageArray as $page)
						{
							$pageHandler -> setPageForId($page, $elementId);
						}
						
						setUpChildrenToPage($pageHandler, /*$xsdCompleteTree*/$manager -> getXsdCompleteTree(), $_GET['id'], $elementId);
						
						$manager -> setPageHandler($pageHandler);
						
						$_SESSION['xsd_parser']['parser'] = serialize($manager);
						
						echo getJSONString($grandParentId);
					}
					else // Copy failed
						echo buildJSON('Copy of element '.$_GET['id'].' failed', -5);
				}
				else // maxOccurs is reached 
				{
					//TODO Use a logger to notify that maxOccurs has been reached
				}
			}
			break;
		case 'r': /*Removing an element*/
			// Check the minimum of element we could have
			if(isset($elementAttr['MINOCCURS'])) $minOccurs = $elementAttr['MINOCCURS'];
			else $minOccurs = 1;
			
			if($minOccurs!=0 && $siblingCount>$minOccurs) // minOccurs > 0, number of elements higher than minOccurs
				$computationResult = $xsdCompleteTree->delete($_GET['id'], true);
			else if($minOccurs==0 && $siblingCount>$minOccurs+1) // minOccurs = 0, number of element higher than 1
				$computationResult = $xsdCompleteTree->delete($_GET['id'], true);
			else // minOccurs = 0, number of element = 0
			{
				$availabilityAttr = array('AVAILABLE'=>false);
				$computationResult = $xsdCompleteTree->getElement($_GET['id'])->addAttributes($availabilityAttr);
			} 
			
			if($computationResult>=0) // ResultCode >= 0 do not break the app
			{
				$manager -> setXsdCompleteTree($xsdCompleteTree);
				//$manager -> setXsdOriginalTree($xsdOriginalTree);
				$_SESSION['xsd_parser']['parser'] = serialize($manager);
				
				echo getJSONString($grandParentId);
			}
			else // Procedure has not went well
			{
				echo buildJSON('Removal of element '.$_GET['id'].' failed', -6);
			}
			
			break;
		default:
			echo buildJSON('Unknown command sent', -4);
			break;
	}
}
else 
	echo buildJSON('$_SESSION environment not set', -2);