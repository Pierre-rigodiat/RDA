<?php

session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

function getJSONString(/*$parser, $xsdCompleteTree, */$elementId)
{
	/*$parser -> setXsdCompleteTree($xsdCompleteTree);
	 $_SESSION['xsd_parser']['parser'] = serialize($parser);*/

	$htmlCode = htmlspecialchars(str_replace('\.', '\\\.', displayQueryTree($elementId)));
	
	if(isset($htmlCode))
	{
		return buildJSON($htmlCode, 0);
	}
	else
	{
		return buildJSON('No display or parser configured', -3);
	}
}

function displayQueryTree($grandParentId)
{
	if(isset($_SESSION['xsd_parser']['display']) && isset($_SESSION['xsd_parser']['parser']))
	{
		$treeString = '';

		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();

		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$xsdQueryTree = $manager -> getXsdQueryTree();

		if($grandParentId>=0)
		{
			$children = $xsdQueryTree->getChildren($grandParentId);
			foreach($children as $childId)
			{
				$treeString .= $display->displayQueryElement($childId);
			}
		}
		else $treeString .= $display->displayQueryChild();


		return $treeString;

	}
	else return null;
}

function duplicateElement($xsdQueryTree, $searchHandler, $elementId, $siblingId) {
	if(isset($_SESSION['xsd_parser']['parser']))
	{
		$displayedIdArray = $searchHandler->getIdArray();
		
		if (in_array($elementId, $displayedIdArray)){
			$searchHandler->addId($siblingId);
		}
		$child = $xsdQueryTree->getChildren($elementId);
		if ($child != array()) {
			foreach ($child as $childId) {
				$createdChildId = $xsdQueryTree->duplicate($childId);
				$xsdQueryTree -> setParent($createdChildId, $siblingId);
				duplicateElement($xsdQueryTree, $searchHandler, $childId,$createdChildId);	
			}
		}
		
	}
}

if(isset($_GET['action']) && isset($_GET['id']) && isset($_SESSION['xsd_parser']['parser']))
{
	// Create main variable
	$manager = unserialize($_SESSION['xsd_parser']['parser']);
	$xsdQueryTree = $manager -> getXsdQueryTree();

	$element = $xsdQueryTree->getElement($_GET['id']);

	// Check that we actually got an existing element
	if($element) $elementAttr = $element->getAttributes();
	else // $tree->getObject() returns null
	{
		echo buildJSON('Id '.$_GET['id'].' does not exist inside the current tree', -1);
		exit;
	}

	// Other variables
	$parentId = $xsdQueryTree->getParent($_GET['id']);
	$grandParentId = $xsdQueryTree->getParent($parentId);

	// Check that this part of the tree is not unavailable
	$elderId = $xsdQueryTree->getParent($_GET['id']);
	$elderObject = $xsdQueryTree->getElement($elderId);
	$elderAttributes = $elderObject->getAttributes();

	$isElderAvailable = !(isset($elderAttributes['AVAILABLE']) && !$elderAttributes['AVAILABLE']);

	while($isElderAvailable && $elderId!=0)
	{
		$elderId = $xsdQueryTree->getParent($elderId);
		$elderObject = $xsdQueryTree->getElement($elderId);
		$elderAttributes = $elderObject->getAttributes();

		$isElderAvailable = !(isset($elderAttributes['AVAILABLE']) && !$elderAttributes['AVAILABLE']);
	}

	if(!$isElderAvailable)
	{
		$htmlCode = htmlspecialchars(str_replace('\.', '\\\.', displayQueryTree($grandParentId)));
		echo buildJSON($htmlCode, $elderId);

		exit;
	}

	// Retrieving the number of current siblings
	$siblingCount = count($xsdQueryTree -> getSiblings($_GET['id']));

	/**
	 *
	 */
	switch($_GET['action'])
	{
		case 'a': /*Adding an element*/
			if(isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE']) // Element is not available (it needs to be set as available)
			{
				$availabilityAttr = array('AVAILABLE'=>true);
				$removeResult = $xsdQueryTree->getElement($_GET['id'])->addAttributes($availabilityAttr);
				//$removeResult = $xsdOriginalTree->getObject($originalTreeId)->addAttributes($availabilityAttr);

				// xxx change to original tree
				$manager -> setXsdQueryTree($xsdQueryTree);
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
					$elementId = $_GET['id'];
					$searchHandler = $manager->getSearchHandler();
					$siblingId = $xsdQueryTree->duplicate($elementId);
					duplicateElement($xsdQueryTree, $searchHandler, $elementId, $siblingId);
					
					$xsdQueryTree -> setBrother($elementId, $siblingId);
					

					if($elementId>=0)
					{
						$manager -> setXsdQueryTree($xsdQueryTree);

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
				
			if($minOccurs!=0 && $siblingCount>$minOccurs) { // minOccurs > 0, number of elements higher than minOccurs
				$computationResult = $xsdQueryTree->delete($_GET['id'], true);
				$manager->getSearchHandler()->removeId($_GET['id']);
			}
			else if($minOccurs==0 && $siblingCount>$minOccurs+1) { // minOccurs = 0, number of element higher than 1
				$computationResult = $xsdQueryTree->delete($_GET['id'], true);
				$manager->getSearchHandler()->removeId($_GET['id']);
			}
			else // minOccurs = 0, number of element = 0
			{
				$availabilityAttr = array('AVAILABLE'=>false);
				$computationResult = $xsdQueryTree->getElement($_GET['id'])->addAttributes($availabilityAttr);
			}
				
			if($computationResult>=0) // ResultCode >= 0 do not break the app
			{
				$manager -> setXsdQueryTree($xsdQueryTree);
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