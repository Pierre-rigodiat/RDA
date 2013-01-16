<?php
/**
 * PHP Functions used by controllers
 * 
 * 
 */
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/ModuleDisplay.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/XsdDisplay.php';
// TODO Setup debug using the session variable

/**
 * Function to display the every brother of the father of the element we have clicked on.
 * A ModuleHandler object should have been configured before.
 * @param $tree
 * @param $grandParentId
 * 
 * @return (string)
 */
function displayTree($tree, $grandParentId)
{
	if(isset($_SESSION['xsd_parser']['mhandler']) && isset($_SESSION['xsd_parser']['phandler']))
	{
		$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		$moduleDisplay = new ModuleDisplay($mHandler, true);
		
		$result = '';
	
		$display = new XsdDisplay($tree, unserialize($_SESSION['xsd_parser']['phandler']), $moduleDisplay, true);
							
		if($grandParentId>=0)
		{
			$children = $tree->getChildren($grandParentId);
			foreach($children as $childId)
			{
				$result .= $display->displayHTMLForm($childId, true);
			}
		}
		else $result .= $display->displayHTMLForm(0, true);
		
		return $result;
	}
	else return null;
}

/**
 * 
 * A ModuleHandler object should have been configured before.
 * 
 * 
 */
function displayAttributes($tree, $elementId)
{
	if(isset($_SESSION['xsd_parser']['mhandler']) && isset($_SESSION['xsd_parser']['phandler']))
	{
		$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		$moduleDisplay = new ModuleDisplay($mHandler, true);
		
		$display = new XsdDisplay($tree, unserialize($_SESSION['xsd_parser']['phandler']), $moduleDisplay, true);	
		return $display->displayConfigurationElement($elementId, true);
	}
	else return null;
}

/**
 * Function to build a JSON string compliant with the format read in the addRemove.js script
 * @param $message
 * @param $code
 * 
 * @return (string) The actua
 */
function buildJSON($message, $code)
{
	if(is_string($message) && is_integer($code)) return '{"result":"'.$message.'", "code":'.$code.'}';
	else return '{"result":"Wrong parameter given to the function. Impossible to build the JSON", "code":-9999}';
}


?>