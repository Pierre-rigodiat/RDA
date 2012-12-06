<?php

/**
 * The class managing the element data structure
 */
// TODO implement in a future version
/*
 * TODO define precisely an element
 * It has:
 * - A unique ID (automatically generated)
 * - A tagName
 * - Attributes
 * 
 * TODO define a function list
 * You can
 * - Get an Set the tagName
 * - 
 *  
 */
class XsdElement {
	private $elementType;
	private $elementAttributes;
	
	public function __construct()
	{
		$argc = func_num_args();
		$argv = func_get_args();
		
		/* Not yet implemented */
	}
	
	public function getType()
	{
		/* Not yet implemented */
		return null; // xxx return String
	}
	
	public function getAttributes()
	{
		/* Not yet implemented */
		return array();
	}
	
	public function setAttributes($attrArray)
	{
		/* Not yet implemented */
		return -1;
	}
	
	public function addAttribute()
	{
		/* Not yet implemented */
		return -1;
	}
	
	public function removeAttribute($attrName)
	{
		/* Not yet implemented */
		return -1;
	}
}

?>