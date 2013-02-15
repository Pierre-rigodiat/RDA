<?php
/**
 * Table module - Loading interface
 * Version: 
 * Date: 
 * Author: 
 * 
 */
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/__ModuleInterface.php';
require_once $_SESSION['xsd_parser']['conf']['modules_dirname'].'/table/core/TableModule.php';
require_once $_SESSION['xsd_parser']['conf']['modules_dirname'].'/table/view/TableDisplay.php';
 
class Table implements __ModuleInterface {
	
	public static function initModule($tree)
	{
		// TODO Check the return codes
		$tableModule = new TableModule($tree);
		$tableDisplay = new TableDisplay($tableModule);
		
		$_SESSION['xsd_parser']['modules']['table'] = serialize($tableDisplay);
		
		return 0;
	}
	
	public static function displayModule()
	{
		if(isset($_SESSION['xsd_parser']['modules']['table']))
		{
			$moduleDisplay = unserialize($_SESSION['xsd_parser']['modules']['table']);
			
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
}



?>