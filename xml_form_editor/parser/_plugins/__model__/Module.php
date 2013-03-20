<?php
/**
 * <Module class>
 */
/**
 * Module abstract class. Describe mandatory element for all the module classes.
 * Version:
 * Date:
 * Author:
 * 
 * @package Plugins\Model\Core
 * 
 */
abstract class Module {
	private $moduleTree; // The tree which implement the module
	private $moduleReferenceTree; // The model the tree should mandatory follow
	
	/**
	 * Comparison between $moduleTree and $moduleReferenceTree
	 * @return {boolean} TRUE if the module is valid regarding the reference
	 */
	private function isValid()
	{
		// TODO Implement it
		return false;
	}
	
	public function getXml()
	{
		
	}
}



?>