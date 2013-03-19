<?php
/**
 * PHP Functions used by controllers
 * 
 * 
 */
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree_.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/ReferenceTree.php';

require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/view/Display.php';
// TODO Setup debug using the session variable
//todo see treeAction to improve the code

/**
 * Function to display the every brother of the father of the element we have clicked on.
 * A ModuleHandler object should have been configured before.
 * @param $grandParentId
 * 
 * @return (string)
 */
function displayTree($grandParentId)
{
	if(isset($_SESSION['xsd_parser']['display']) && isset($_SESSION['xsd_parser']['parser']))
	{
		$treeString = '';
		
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		$manager = unserialize($_SESSION['xsd_parser']['parser']);
		$xsdCompleteTree = $manager -> getXsdCompleteTree();
		
		if($grandParentId>=0)
		{
			$children = $xsdCompleteTree->getChildrenId($grandParentId);
			foreach($children as $childId)
			{
				$treeString .= $display->displayHTMLForm($childId, true);
			}
		}
		else $treeString .= $display->displayHTMLForm(0, true);
		
		
		return $treeString;
		
	}
	else return null;
}

/**
 * 
 * A ModuleHandler object should have been configured before.
 * 
 * 
 */
function displayAttributes($elementId)
{
	if(isset($_SESSION['xsd_parser']['display'])/* && isset($_SESSION['xsd_parser']['phandler'])*/)
	{
		/*$mHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
		$moduleDisplay = new ModuleDisplay($mHandler, true);
		
		$display = new XsdDisplay($tree, unserialize($_SESSION['xsd_parser']['phandler']), $moduleDisplay, true);	
		return $display->displayConfigurationElement($elementId, true);*/
		
		$display = unserialize($_SESSION['xsd_parser']['display']);
		$display -> update();
		
		
		
		//return $display->displayConfigurationElement($elementId, true);
		return $display->displayConfiguration($elementId);
		//return "\"tes|,\"";
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