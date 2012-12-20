<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/XsdDisplay.php';

//todo optimize script
//todo secure script
//todo factorize code
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
 * Function to display the every brother of the father of the element we have clicked on
 * @param $tree
 * @param $grandParentId
 * 
 * @return (string)
 */
function displayTree($tree, $grandParentId)
{
	$result = '';
	
	$display = new XsdDisplay($tree, true);
						
	if($grandParentId>=0)
	{
		$children = $tree->getChildren($grandParentId);
		foreach($children as $childId)
		{
			$result .= $display->displayHTMLForm($childId, true);
		}
	}
	else
	{
		$result .= $display->displayHTMLForm(0, true);
	}
	
	return $result;
}

/**
 * Function to build a JSON string compliant with the format read in the addRemove.js script
 * @param $message
 * @param $code
 * 
 * @return (string)
 */
function buildJSON($message, $code)
{
	if(is_string($message) && is_integer($code)) return '{"result":"'.$message.'", "code":'.$code.'}';
	else return '{"result":"Wrong parameter given to the function. Impossible to build the JSON", "code":-9999}';
}

if(isset($_GET['action']) && isset($_GET['id']) && isset($_SESSION['xsd_parser']['tree']))
{
	// Create main variable
	$tree = unserialize($_SESSION['xsd_parser']['tree']);
	$element = $tree->getObject($_GET['id']);
	
	// Check that we actually got an existing element
	if($element) $elementAttr = $element->getAttributes();
	else // $tree->getObject() returns null
	{
		echo buildJSON('Id '.$_GET['id'].' does not exist inside the current tree', -1);
		exit;
	}
	
	// Other variables
	$parentId = $tree->getParent($_GET['id']);
	$grandParentId = $tree->getParent($parentId);
	
	// Check that this part of the tree is not unavailable
	$elderId = $tree->getParent($_GET['id']);
	$elderObject = $tree->getObject($elderId);
	$elderAttributes = $elderObject->getAttributes();
	
	$isElderAvailable = !(isset($elderAttributes['AVAILABLE']) && !$elderAttributes['AVAILABLE']);
	
	while($isElderAvailable && $elderId!=0)
	{
		$elderId = $tree->getParent($elderId);
		$elderObject = $tree->getObject($elderId);
		$elderAttributes = $elderObject->getAttributes();
		
		$isElderAvailable = !(isset($elderAttributes['AVAILABLE']) && !$elderAttributes['AVAILABLE']);
	}
	
	if(!$isElderAvailable) 
	{
		$htmlCode = htmlspecialchars(displayTree($tree, $grandParentId));
		echo buildJSON($htmlCode, $elderId);
		
		exit;
	}
			
	
	// Retrieving the number of current siblings
	$siblingsIdArray = $tree->getId($element);
	$siblingCount = 0;
	
	foreach ($siblingsIdArray as $siblingId) 
	{
		$siblingParentId = $tree->getParent($siblingId);
		if($siblingParentId==$parentId)  $siblingCount += 1;
	}
	
	switch($_GET['action'])
	{
		case 'a': /*Adding an element*/
			if(isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE'])
			{
				$availabilityAttr = array('AVAILABLE'=>true);
				$removeResult = $tree->getObject($_GET['id'])->addAttributes($availabilityAttr);
				
				$htmlCode = htmlspecialchars(displayTree($tree, $grandParentId));
				echo buildJSON($htmlCode, 0);
			}
			else
			{
				// Check the maximum element we could have
				if(isset($elementAttr['MAXOCCURS']) && is_numeric($elementAttr['MAXOCCURS'])) $maxOccurs = $elementAttr['MAXOCCURS'];
				else if($elementAttr['MAXOCCURS']=='unbounded') $maxOccurs = -1;
				else $maxOccurs = 1;
				
				if($maxOccurs==-1 || $maxOccurs>$siblingCount)
				{
					$elementId = $tree->copyTreeBranch($_GET['id']);
				
					if($elementId>=0)
					{						
						$htmlCode = htmlspecialchars(displayTree($tree, $grandParentId));
						echo buildJSON($htmlCode, 0);
					}
					else
					{
						//XXX An error occured during the copy
					}
				}
				else // maxOccurs is reached 
				{
					//todo return something
				}
			}
						
			break;
		case 'r': /*Removing an element*/
			// Check the minimum of element we could have
			if(isset($elementAttr['MINOCCURS'])) $minOccurs = $elementAttr['MINOCCURS'];
			else $minOccurs = 1;
			
			// Regarding the number of siblings we do different things (addRemove.js will handle the return code)
			/* Returns:
			 * -1 	|	Error on $tree->removeElement
			 * 0  	|	$tree->removeElement OK and we can remove elements
			 * n(>0)|  	$tree->removeElement OK but minOccurs is reached so we cannot remove more elements
			 */
			// todo rename removeResult with computationResult 
			
			if($minOccurs!=0 && $siblingCount>$minOccurs) $computationResult = $tree->removeElement($_GET['id'], true);
			else if($minOccurs==0 && $siblingCount>$minOccurs+1) $computationResult = $tree->removeElement($_GET['id'], true);
			else // minOccurs is reached, no element must be removed but the XsdElement must be updated
			{
				$availabilityAttr = array('AVAILABLE'=>false);
				$computationResult = $tree->getObject($_GET['id'])->addAttributes($availabilityAttr);
			} 
			
			if($computationResult==0)
			{
				$htmlCode = htmlspecialchars(displayTree($tree, $grandParentId));
				echo buildJSON($htmlCode, 0);
			}
			else 
			{
				//xxx An error occured when removing ID
			}
			
			break;
		default:
	}
	
	$_SESSION['xsd_parser']['tree'] = serialize($tree);
}
?>