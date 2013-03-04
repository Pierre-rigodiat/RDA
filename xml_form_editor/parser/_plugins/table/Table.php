<?php
/**
 * Table module - Loading interface
 * Version: 
 * Date: 
 * Author: 
 * 
 */
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/_plugins/__model__/ModuleInterface.php';
require_once $_SESSION['xsd_parser']['conf']['modules_dirname'].'/table/core/TableModule.php';
require_once $_SESSION['xsd_parser']['conf']['modules_dirname'].'/table/view/TableDisplay.php';
 
class Table implements ModuleInterface {
	
	public static function initModule($tree)
	{
		if(!isset($_SESSION['xsd_parser']['modules']['table']['model']) || !isset($_SESSION['xsd_parser']['modules']['table']['view']))
		{
			// TODO Check the return codes
			$tableModule = new TableModule($tree, true);
			$tableDisplay = new TableDisplay($tableModule, true);
			
			$_SESSION['xsd_parser']['modules']['table']['model'] = serialize($tableModule);
			$_SESSION['xsd_parser']['modules']['table']['view'] = serialize($tableDisplay);
			
			return 0;
		}
		else return 1; // Module already loaded
	}
	
	public static function displayModule()
	{
		if(isset($_SESSION['xsd_parser']['modules']['table']['view']))
		{
			$moduleDisplay = unserialize($_SESSION['xsd_parser']['modules']['table']['view']);
			
			$module = '<div class="table_module">';
			$module .= $moduleDisplay->display();
			$module .= '</div>';
			
			return $module;
		}
		else
		{
			return 'Module not initialized';
		}
	}
	
	public static function getModuleData()
	{
		if(isset($_SESSION['xsd_parser']['modules']['table']['model']))
		{
			$tableModule = unserialize($_SESSION['xsd_parser']['modules']['table']['model']);
			return $tableModule -> getXmlData();
		}
		else
		{
			return null;
		}
	}
}



?>