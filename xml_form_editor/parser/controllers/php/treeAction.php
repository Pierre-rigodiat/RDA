<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdParser.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

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
function getJSONString($parser, $xsdCompleteTree, $elementId)
{
	$parser -> setXsdCompleteTree($xsdCompleteTree);
	$_SESSION['xsd_parser']['parser'] = serialize($parser);
	
	$htmlCode = htmlspecialchars(displayTree($elementId));
	
	if($htmlCode)
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
	$parser = unserialize($_SESSION['xsd_parser']['parser']);
	$xsdCompleteTree = $parser -> getXsdCompleteTree();
	
	$element = $xsdCompleteTree->getObject($_GET['id']);
	
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
	$elderObject = $xsdCompleteTree->getObject($elderId);
	$elderAttributes = $elderObject->getAttributes();
	
	$isElderAvailable = !(isset($elderAttributes['AVAILABLE']) && !$elderAttributes['AVAILABLE']);
	
	while($isElderAvailable && $elderId!=0)
	{
		$elderId = $xsdCompleteTree->getParent($elderId);
		$elderObject = $xsdCompleteTree->getObject($elderId);
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
	$siblingsIdArray = $xsdCompleteTree->getId($element);
	$siblingCount = 0;
	
	foreach ($siblingsIdArray as $siblingId) 
	{
		$siblingParentId = $xsdCompleteTree->getParent($siblingId);
		if($siblingParentId==$parentId)  $siblingCount += 1;
	}
	
	switch($_GET['action'])
	{
		case 'a': /*Adding an element*/
			if(isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE'])
			{
				$availabilityAttr = array('AVAILABLE'=>true);
				$removeResult = $xsdCompleteTree->getObject($_GET['id'])->addAttributes($availabilityAttr);
				
				echo getJSONString($parser, $xsdCompleteTree, $grandParentId);
			}
			else
			{
				// Check the maximum element we could have
				if(isset($elementAttr['MAXOCCURS']) && is_numeric($elementAttr['MAXOCCURS'])) $maxOccurs = $elementAttr['MAXOCCURS'];
				else if($elementAttr['MAXOCCURS']=='unbounded') $maxOccurs = -1;
				else $maxOccurs = 1;
				
				if($maxOccurs==-1 || $maxOccurs>$siblingCount)
				{
					$elementId = $xsdCompleteTree->copyTreeBranch($_GET['id']);
				
					if($elementId>=0)
					{
						echo getJSONString($parser, $xsdCompleteTree, $grandParentId);
					}
					else // Copy failed
					{
						echo buildJSON('Copy of element '.$_GET['id'].' failed', -5);
					}
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
			
			if($minOccurs!=0 && $siblingCount>$minOccurs) $computationResult = $xsdCompleteTree->removeElement($_GET['id'], true);
			else if($minOccurs==0 && $siblingCount>$minOccurs+1) // If minOccurs == 0 & is reached then, we do not want to erase the item but disable it
				$computationResult = $xsdCompleteTree->removeElement($_GET['id'], true);
			else // minOccurs is reached, no element must be removed but the XsdElement must be updated
			{
				$availabilityAttr = array('AVAILABLE'=>false);
				$computationResult = $xsdCompleteTree->getObject($_GET['id'])->addAttributes($availabilityAttr);
			} 
			
			if($computationResult==0)
			{
				echo getJSONString($parser, $xsdCompleteTree, $grandParentId);
			}
			else // Procedure has not went well
			{
				echo buildJSON('Removal of element '.$_GET['id'].' failed', -6);
			}
			
			break;
		default:
			echo buildJSON('Bad command sent', -4);
			break;
	}
}
else echo buildJSON('Variables not set in the $_SESSION environment', -2);
?>