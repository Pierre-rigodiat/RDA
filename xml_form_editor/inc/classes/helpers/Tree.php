<?php

/**
 * The class managing the tree data structure
 */
// TODO implement in a future version
class Tree {
	/*
	 * xxx The tree is an array
	 *  - Element ID (Here it is an xsd element but it could be anything else)
	 *  - Father ID
	 *  - Children ID (an array)
	 */
	 /* TODO Function list
	 * 
	 * add element
	 * remove element
	 * skip element (link a grand father to children)
	 * display path
	 * getFather
	 * getChildren
	 * 
	 * 
	 */
	
	private $tree;
	// todo find out what kind of variable we do need
	
	public function __construct()
	{
		// TODO use a logger to register errors
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc)
		{
			case 0:
				$tree = array();
				break;
			case 1:
				// TODO configure the case where a tree is given in parameter
				break;
			default:
				break;
		}
		
		/* Not yet implemented */
	}
	
	public function getTree()
	{
		/* Not yet implemented */
		return array();
	}
	
	public function getParent($elementId)
	{
		/* Not yet implemented */
		return -1;
	}
	
	public function getChildren($elementId)
	{
		/* Not yet implemented */
		return array();
	}
	
	public function insertElement($elementObject, $parentElementId)
	{
		/* Not yet implemented */
		return -1;
	}
	
	public function removeElement($elementId, $isRecursive)
	{
		/* Not yet implemented */
		return -1;
	}
	
	public function copyTreeBranch($baseElementId)
	{
		/* Not yet implemented */
		return -1;
	}
	
}

?>