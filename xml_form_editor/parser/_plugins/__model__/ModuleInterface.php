<?php
/**
 * The basic interface to load a module
 * Version:
 * Date:
 * Author: 
 * 
 */
interface ModuleInterface
{
	/**
	 * This function should register the core of your module in $_SESSION['']['modules']['moduleFolderName']
	 * @param {Tree} The tree object applying to the module
	 * @return {integer} 0 if no error occured, <0 if an error occured 
	 */
	public static function initModule($tree);
	
	/**
	 * This function will display the module by initialize a the display class with the core of the module
	 * @return {string} HTML code of the module
	 */
	public static function displayModule();
	
	public static function getModuleData();
}
?>