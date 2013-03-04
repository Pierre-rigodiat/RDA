<?php
/**
 * Class managing the tree structure
 * 
 * @uses core\XsdElement.php
 * 
 * @package XsdMan\Core
 */


require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';





/*
 * 
 * 
 * 
 * 
 * <v0.2b 12/04/2012
 * 
 * Changelog
 * ** 0.1b **
 * removeElement updated to handle root suppression
 * ** 0.2a **
 * getId function added (left the resource part to implement)
 * ** 0.2b **
 * clone object in copyTreeBranch to differentiate object
 * copyTreeBranch copies the object near his brother
 * ** 0.2c **
 * add a hasElement function
 * improve copyTreeBranch in case the tree does not contain objects>
 * 
 */
class Tree {
	private $tree;
	private $lastObjectId;
	
	private $LOGGER;
	
	private static $LEVELS = array('DBG'=>'notice', 'NO_DBG'=>'info');
	private static $LOG_FILE;
	private static $FILE_NAME = 'Tree.php';
	
	public function __construct()
	{
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'].'/logs/parser.log';
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		$this->lastObjectId = -1;
		
		switch($argc)
		{
			case 0: // new Tree()
				$this->tree = array();
				$level = self::$LEVELS['NO_DBG'];
				
				break;
			case 1: // new Tree(boolean) || new Tree(treeObject)
				if(is_array($argv[0])) // new Tree(treeObject)
				{
					$this->tree = $argv[0];
					$level = self::$LEVELS['NO_DBG'];
				}
				else if(is_bool($argv[0]))// new Tree(boolean)
				{
					if($argv[0]) // new Tree(true)
					{
						$this->tree = array();
						$level = self::$LEVELS['DBG'];
					}
					else // new Tree(false)
					{
						$this->tree = array();												
						$level = self::$LEVELS['NO_DBG'];
					}
				}
				else // new Tree(whateverItIs)
				{
					$this->tree = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				
				break;
			case 2: // new Tree(treeObject, boolean)
				if(is_array($argv[0]) && is_bool($argv[1]))
				{
					$this->tree = $argv[0];
				
					if($argv[1])
					{
						$level = self::$LEVELS['DBG'];
					}
					else
					{
						$level = self::$LEVELS['NO_DBG'];
					}
				}
				else 
				{
					$this->tree = null;
					$level = self::$LEVELS['NO_DBG'];
				}	
					
				break;
			default:
				$this->tree = null;
				$level = self::$LEVELS['NO_DBG'];
				break;
		}
		
		try
		{
			$this->LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME); // xxx what if the $_SESSION doesn't exist
		}
		catch (Exception $ex)
		{
			echo '<b>Impossible to build the Logger:</b><br/>'.$ex->getMessage();
		}
		
		if(!is_array($this->tree)) 
		{
			$log_mess = '';
			switch($argc)
			{
				case 1: // new Tree(boolean) || new Tree(treeObject)
					$log_mess .= 'Constructor with 1 parameter should be used with an array or a boolean ('.gettype($argv[0]).' given)';
					break;
				case 2: // new Tree(treeObject, boolean)
					$log_mess .= 'Constructor with 1 parameter should be used as {array,boolean} ({'.gettype($argv[0]).','.gettype($argv[1]).'} given)';	
					break;
				default:
					$log_mess .= '2 parameter max. must be entered ('.$argc.' given)';
					break;
			}
			
			$this->LOGGER->log_error($log_mess, 'Tree::__construct');
		}
		else $this->LOGGER->log_debug('Tree has been created', 'Tree::__construct');
	}
	
	/**
	 * 
	 */
	public function getTree()
	{
		$this->LOGGER->log_notice('Function called', 'Tree::getTree');
		return $this->tree;
	}
	
	public function getParent($elementId)
	{
		if(isset($this->tree[$elementId]))
		{
			$parentId = $this->tree[$elementId]['parent'];
			
			$this->LOGGER->log_debug('ID '.$elementId.' has ID '.$parentId.' as a parent', 'Tree::getParent');
			return $parentId;
		} 
		else 
		{
			$this->LOGGER->log_error('ID '.$elementId.' is not in the current tree', 'Tree::getParent');
			return -2; // -1 value identifies the father of the root element
		}
	}
	
	public function getChildren($elementId)
	{
		if (!defined("print_array"))// Avoid to redefine the function (i.e. avoid the error)
		{
			define("print_array", true);

			function print_array($array)
			{
				$result = '';
				foreach($array as $item)
				{
					$result.=$item;
					if(end($array)!=$item) $result.=', ';
				}
				
				return $result;
			}
		}
		
		if(isset($this->tree[$elementId]))
		{
			$children = $this->tree[$elementId]['children'];
			
			if(count($children)>0) $this->LOGGER->log_debug('Chidren of ID '.$elementId.' are '.print_array($children), 'Tree::getChildren');
			else $this->LOGGER->log_debug('ID '.$elementId.' has no child', 'Tree::getChildren');
				
			return $children;
		} 
		else 
		{
			$this->LOGGER->log_error('ID '.$elementId.' is not in the current tree', 'Tree::getChildren');
			return null;
		}
	}

	public function setObject($elementId, $object)
	{
		if(isset($this->tree[$elementId]))
		{
			$this->tree[$elementId]['object'] = $object;
			
			$this->LOGGER->log_debug('ID '.$elementId.' is now set with '.$object, 'Tree::setObject');
			return 0;
		} 
		else 
		{
			$this->LOGGER->log_error('ID '.$elementId.' is not in the current tree', 'Tree::getParent');
			return -1;
		}
	}
	
	public function getObject($elementId)
	{
		if(isset($this->tree[$elementId]))
		{
			$object = $this->tree[$elementId]['object'];
			
			$this->LOGGER->log_debug('ID '.$elementId.' contains '.$object, 'Tree::getObject');
			return $object;
		} 
		else 
		{
			$this->LOGGER->log_error('ID '.$elementId.' is not in the current tree', 'Tree::getObject');
			return null;
		}
	}
	
	/**
	 * 
	 */
	public function getId($elementObject)
	{
		$result = array();
		$ids = array_keys($this->tree);
		
		foreach($ids as $id)
		{
			$treeObject = $this->tree[$id]['object'];
			$objectType = gettype($treeObject);
			
			if($objectType==gettype($elementObject))
			{
				if($objectType=='boolean' || $objectType=='integer' || $objectType=='double' || $objectType=='string' || $objectType=='NULL')
				{
					if($treeObject==$elementObject) array_push($result, $id); 
				}
				else if($objectType=='array') 
				{
					if(count(array_diff($treeObject, $elementObject))==0) array_push($result, $id);
				}
				else if($objectType=='object')
				{
					if(method_exists($treeObject, '__equalsTo') && $treeObject->__equalsTo($elementObject)==true) array_push($result, $id);
				}
				else if($objectType=='resource')
				{
					// TODO Implement the resource comparison
				}
			}
		}
		
		$this->LOGGER->log_debug('Function returns the following ids: '.serialize($result), 'Tree::getId');
		return $result;
	}
	
	public function insertElement($elementObject, $parentElementId = -1)
	{
		$this->LOGGER->log_debug('insertElement('.$elementObject.', '.$parentElementId.')', 'Tree::insertElement');
		
		if(is_integer($parentElementId) && $elementObject!==null)
		{
			$elementString="";
			$elementType = gettype($elementObject);
			
			if(($elementType=='object' && !in_array("__toString", get_class_methods(get_class($elementObject))))
				|| $elementType=='array') $elementString = '{'.serialize($elementObject).'}';
			else $elementString = $elementObject;
			
			if($this->lastObjectId==-1) // Insert the root element
			{
				$this->lastObjectId += 1;
				$this->tree[$this->lastObjectId] = array('object'=>$elementObject, 'parent'=>$parentElementId, 'children'=>array());
				
				
				$this->LOGGER->log_debug($elementString.' (type: '.$elementType.') is inserted as the root element (id = 0)', 'Tree::insertElement');
				
				return $this->lastObjectId;
			}
			else
			{
				if($parentElementId>=0) // Insert a normal element
				{
					$this->lastObjectId += 1;
					$this->tree[$this->lastObjectId] = array('id'=>$this->lastObjectId, 'object'=>$elementObject, 'parent'=>$parentElementId, 'children'=>array());
					array_push($this->tree[$parentElementId]['children'], $this->lastObjectId);
					
					$this->LOGGER->log_debug($elementString.' (type: '.$elementType.') is inserted with ID '.$this->lastObjectId, 'Tree::insertElement');
					
					return $this->lastObjectId;
				}
				else 
				{
					$this->LOGGER->log_error('$parentElementId (2nd parameter) must be positive ('.$parentElementId.'<0)', 'Tree::insertElement');
					return -3;
				}
			}
		}
		else if(!is_integer($parentElementId))
		{
			$this->LOGGER->log_error('$parentElementId (2nd parameter) must be an integer ('.gettype($parentElementId).' given)', 'Tree::insertElement');
			return -1;
		}
		else // $elementObject==null
		{
			$this->LOGGER->log_error('$elementObject (first parameter) cannot be null', 'Tree::insertElement');
			return -2;
		}
	}
	
	public function removeElement($elementId, $isRecursive = false)
	{
		if(isset($this->tree[$elementId]) && is_bool($isRecursive))
		{
			$parentId = $this->tree[$elementId]['parent'];
			
			if($parentId!=-1)
			{
				$this->tree[$parentId]['children'] = array_diff($this->tree[$parentId]['children'], array($elementId)); // The current element is deleted from the father (in the array 'children')
				if(count($this->tree[$elementId]['children'])>0)
				{
					if($isRecursive)
					{
						foreach($this->tree[$elementId]['children'] as $child)
						{
							$this->removeElement($child, true);
						}
					}
					else
					{
						foreach($this->tree[$elementId]['children'] as $child)
						{
							$this->tree[$child]['parent'] = $parentId;
							array_push($this->tree[$parentId]['children'], $child);
						}
					}
		
				}
			}
			else 
			{
				if(count($this->tree[$elementId]['children'])<=1)
				{
					foreach($this->tree[$elementId]['children'] as $child)
					{
						$this->tree[$child]['parent']=-1;
					}
				}
				else
				{
					$this->LOGGER->log_error('Impossible to suppress the root element (ID '.$elementId.') if it has more than 1 child', 'Tree::removeElement');
					return -3;
				}
			}
			
			unset($this->tree[$elementId]);
			
			$this->LOGGER->log_debug('ID '.$elementId.' removed from the tree', 'Tree::removeElement');
			return 0;
		}
		else if(!is_bool($isRecursive))
		{
			$this->LOGGER->log_error('2nd parameter must be a boolean ('.gettype($isRecursive).' given)', 'Tree::removeElement');
			return -1;
		}
		else // !isset($this->tree[elementId])
		{
			$this->LOGGER->log_error('ID '.$elementId.' is not in the current tree', 'Tree::removeElement');
			return -2;
		}
	}

	/**
	 * 
	 */
	public function hasElement()
	{
		$this -> LOGGER -> log_debug('Function called for a tree with '.count($this->tree).' element(s)', 'Tree::hasElement');
		return count($this->tree)>0?true:false;
	}
	
	/**
	 * 
	 */
	public function copyTreeBranch($baseElementId, $destinationId = -1)
	{
		$this -> LOGGER -> log_debug('Copying tree branch from '.$baseElementId.'...', 'Tree::copyTreeBranch');
		
		if(isset($this->tree[$baseElementId]) && $this->tree[$baseElementId]['parent']!=-1) // Check the existence of the element + the element is not the root (copy impossible)
		{
			// Gathering useful information (to simplify the writing)
			$treeElement = $this->tree[$baseElementId];
			$elementObject = $treeElement['object'];
			$children = $treeElement['children'];
			
			$parentId = -1;
			if($destinationId == -1) // When the destination ID has not been set (=initial call)
			{
				$parentId = $treeElement['parent'];
			}
			else {
				if(isset($this->tree[$destinationId])) $parentId = $destinationId;
				else 
				{
					$this->LOGGER->log_error('ID '.$destinationId.' (set as $destinationId) is not in the current tree', 'Tree::copyTreeBranch');
					return -3;
				}
			}
			
			// If the tree stores objects, we need to clone those to avoid multi-edition
			if(is_object($elementObject)) $newElementObject = clone $elementObject;
			else $newElementObject = $elementObject;
			
			$newElementId = $this->insertElement($newElementObject, $parentId);
			
			// Change the children list to set the new element next to his brother in the children list
			// This feature is only applied at initial call (i.e for the parent element)
			if($destinationId == -1)
			{
				// FIXME Problem with invalid ids (array_values should not be used)
				$parentChildrenList = array_values($this->tree[$parentId]['children']);
				$index = -1;
				
				foreach($parentChildrenList as $id=>$parentChildrenId)
				{
					if($parentChildrenId==$baseElementId)
					{
						$index = $id;
						break;
					}
				}
				
				if($index>=0)
				{
					$this -> LOGGER -> log_debug('Putting '.$baseElementId.' at '.($index+1), 'Tree::copyTreeBranch');
					array_pop($this->tree[$parentId]['children']); // Delete the new element in the children list
					
					$newElementIdArray = array($newElementId);
					array_splice($this->tree[$parentId]['children'], $index+1, 0, $newElementIdArray); // Add the element at the right index
				}
				else 
				{
					$this->LOGGER->log_error('Impossible to retrieve ID '.$baseElementId.' as a child of ID '.$parentId, 'Tree::copyTreeBranch');
					return -3;
				}
			}
			
			foreach($children as $child)
			{
				$this->copyTreeBranch($child, $newElementId);
			}
			
			$this->LOGGER->log_debug('ID '.$baseElementId.' has been copied as a child of ID '.$parentId.' (new ID: '.$newElementId.')', 'Tree::copyTreeBranch');
			return $newElementId;
		}
		else if($this->tree[$baseElementId]['parent']==-1)
		{
			$this->LOGGER->log_error('Impossible to copy the root element', 'Tree::copyTreeBranch');
			return -1;
		}
		else  // !isset($this->tree[$baseElementId])
		{
			$this->LOGGER->log_error('ID '.$elementId.' (set as $baseElementId) is not in the current tree', 'Tree::copyTreeBranch');
			return -2;
		}
	}

	public function __toString()
	{
		// TODO Implement it
	}	
}

?>