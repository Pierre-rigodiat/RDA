<?php
/**
 * 
 */
session_start();

// Require lib to write JSON message
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/PhpControllersFunctions.php';

if(!isset($_SESSION['xsd_parser']['parser']) || !isset($_SESSION['xsd_parser']['display']))
{
	return buildJSON('Main classes are not in memory', -1); 
}

if(isset($_GET['parent']) && isset($_GET['child']))
{
	// Convert values to integer
	$choiceElementID = intval($_GET['parent']);
	$choosenId = intval($_GET['child']);
	
	// Require needed object
	require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
	require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
	require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
	require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
	
	// Build the necessary items
	$xsdManager = unserialize($_SESSION['xsd_parser']['parser']);
	$xsdQueryTree = $xsdManager -> getXsdQueryTree();
	
	// Modify the XsdElement choice (to specify the selected item)
	// TODO Another possible way is to change element attribute without building another one
	// XXX Possible way of lowering the use of resources
	$choiceElement = $xsdQueryTree -> getElement($choiceElementID);
	//$choiceElement = $xsdManager -> getXsdOriginalTree() -> getElement($choiceOriginalId);
	$choiceElementAttribute = $choiceElement -> getAttributes();
	
	$choiceKey = array_search($choosenId, $choiceElementAttribute['CHOICE']);
	unset($choiceElementAttribute['CHOICE'][$choiceKey]);
	
	array_unshift($choiceElementAttribute['CHOICE'], $choosenId);
	$newChoiceElement = new XsdElement('XSD:ELEMENT', $choiceElementAttribute);
	
	$xsdManager -> getXsdOriginalTree() -> setElement($choiceElementID, $newChoiceElement);
	
	$_SESSION['xsd_parser']['parser'] = serialize($xsdManager);
	
	// Get the HTML code of the new element	
	$childOrganizedId = $xsdQueryTree -> find(intval($_GET['child']));
	$childId = -1;
	
	foreach($childOrganizedId as $possibleChildId)
	{
		if($xsdQueryTree -> getParent($possibleChildId) == intval($_GET['parent']))
		{
			$childId = $possibleChildId;
			break;
		}
	}
	
	// Send the JSON response
	if($childId != -1)
	{
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		$jsonMessage = htmlspecialchars($display->displayQueryElement($childId));
		
		echo buildJSON($jsonMessage, 0);
	}
	else echo buildJSON('ID '.$_GET['child'].' with parent '.$_GET['parent'].' not found', -2);
}