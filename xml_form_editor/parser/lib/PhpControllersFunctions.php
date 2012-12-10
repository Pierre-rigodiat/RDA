<?php
/**
 * PHP Functions used by controllers
 * 
 * 
 */
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/XsdDisplay.php';


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

function displayAttributes($tree, $elementId)
{
	$display = new XsdDisplay($tree, true);	
	return $display->displayConfigurationElement($elementId, true);
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


?>