<?php
/**
 * <ClosureTable class>
 */
/**
 * Stores a tree in a closure table structure.
 * 
 * Closure tables are the better way to store trees if performances are at stake.
 * 
 * 
 */
class ClosureTable {
	/**
	 * Array containing all elements
	 * @var array
	 */
	private $elementList;
	
	/**
	 * Array linking all elements
	 * @var array
	 */
	private $ancestorTable;
	
	/**
	 * Id of the next element
	 * @var int
	 */
	private $insertIndex;
	
	/**
	 * An identifier for the tree (useful for logging purposes)
	 * @var string
	 */
	private $__ID;
	
	
	private $LOGGER;
	private static $LEVELS = array('DBG'=>'notice', 'NO_DBG'=>'info');
	private static $LOG_FILE;
	private static $FILE_NAME = 'Tree.php';
	
	/**
	 * 
	 * 
	 * Param ID is mandatory
	 * 
	 * 
	 */
	public function __construct() {
		// Initialize the logger (will throw an Exception if any problem occurs)
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'].'/logs/closure.log';
		$level = self::$LEVELS['DBG'];
		$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc)
		{
			case 1: // new ClosureTable(idString)
				if(is_string($argv[0]))
				{
					$this->__ID = $argv[0];
					//$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					throw new Exception('Invalid parameters given to ClosureTable');
					//$level = self::$LEVELS['NO_DBG'];
				}
				
				break;
			/*case 2: // new ClosureTable(idString, debug)
				if(is_string($argv[0]) && is_bool($argv[1]))
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
					
				break;*/
			default:
				throw new Exception('Invalid parameters given to ClosureTable');
				//$level = self::$LEVELS['NO_DBG'];
				break;
		}
		
		$this -> elementList = array();
		$this -> ancestorTable = array();
		$this -> insertIndex = 0;
	}
	
	/**
	 * 
	 * 
	 * 
	 * @return integer Created element id
	 */
	public function insertElement($element, $parentId = -1)
	{
		$elementIndex = $this -> insertIndex;
		
		// Add element in the element list
		$this -> insertIntoElementList($element, $elementIndex);
		
		// Insert into ancestor table
		$this -> insertIntoAncestorTable($parentId, $elementIndex);
		
		$this -> insertIndex += 1;
		
		return $elementIndex;
	}
	
	/**
	 * 
	 */
	private function insertIntoElementList($element, $elementId)
	{
		$this -> elementList [ $elementId ] = $element;
	}
	
	/**
	 * 
	 * 
	 * 
	 * 
	 */
	private function insertIntoAncestorTable($ancestor, $descendant)
	{
		$ancetorRow = array(
			"ancestor" => $ancestor,
			"descendant" => $descendant
		);
		
		array_push($this -> ancestorTable, $ancetorRow);
	}
	
	/**
	 * 
	 * The parent ID of this element is automatically set to -1
	 * 
	 * 
	 * @return integer Created element id
	 */
	public function duplicateElement($elementId, $recursively = false)
	{
		$elementToDuplicate = $this -> elementList [$elementId];
		if(is_object($elementToDuplicate)) $elementToDuplicate = clone $elementToDuplicate;
				
		$createdElementId = $this -> insertElement($elementToDuplicate);
		
		if($recursively)
		{
			foreach($this -> getChildrenId($elementId) as $childId)
			{
				$createdChildId = $this -> duplicateElement($childId, true);
				$this -> setParent($createdChildId, $createdElementId);
			}
		}
		
		return $createdElementId;
	}
	
	public function delete($elementId, $recursively = false)
	{
		// Delete element in list
		unset($this -> elementList [$elementId]);
		
		// Delete ancestorTable reference
		$children = $this -> getChildrenId($elementId);
		if(!$recursively)
		{
			$parent = $this -> getParentId($elementId);
			
			foreach($children as $child)
			{
				$this -> setParent($child, $parent);
			}
		}
		else {
			foreach($children as $child)
			{
				$this -> delete($child, true);
			}
		}
		
		foreach ($this -> ancestorTable as $rowId => $ancestorRow) 
		{
			if(in_array($elementId, $ancestorRow))
				unset($this -> ancestorTable[$rowId]);
		}
	}
	
	/**
	 * 
	 * 
	 */
	public function setParent($elementId, $parentId)
	{
		$ancestorRowToAdd = array(
			"ancestor" => $parentId,
			"descendant" => $elementId
		);	
		
			
		foreach($this -> ancestorTable as $rowId => $ancestorRow)
		{
			if($ancestorRow["descendant"] == $elementId)
			{
				unset($this -> ancestorTable[ $rowId ]);
				break;
			}
		}
		
		array_push($this -> ancestorTable, $ancestorRowToAdd);
	}
	
	
	/**
	 * 
	 * @param int $baseElementId
	 * @param int $brotherElementId 
	 */
	public function setBrother($baseElementId, $brotherElementId)
	{
		// TODO avoid the case elements are undefined		
		$baseElementIndex = -1;
		$brotherElementIndex = -1;
		
		$this -> ancestorTable = array_values($this -> ancestorTable);
		
		foreach($this -> ancestorTable as $rowId => $ancestorRow)
		{
			if($ancestorRow["descendant"] == $baseElementId)
			{
				$baseElementIndex = $rowId;
			}
			
			if($ancestorRow["descendant"] == $brotherElementId)
			{
				$brotherElementIndex = $rowId;
			}
		}
		
		unset($this -> ancestorTable [$brotherElementIndex]);
		
		$ancestorTableEnd = array_splice($this -> ancestorTable, $baseElementIndex+1);
		array_push($this -> ancestorTable, array("ancestor" => $this -> getParentId($baseElementId), "descendant" => $brotherElementId));
		
		$this -> ancestorTable = array_merge($this -> ancestorTable, $ancestorTableEnd);
	}
	
	public function setElement($elementId, $element)
	{
		$this -> elementList [ $elementId ] = $element;
		
	}
	
	/**
	 * 
	 * 
	 * @return mixed Element stored at the given ID
	 */
	public function getElement($elementId)
	{
		return isset($this -> elementList [$elementId])?$this -> elementList [$elementId]:null;
	}
	
	/**
	 * 
	 * 
	 * @return array Array of element IDs
	 */
	public function getIds($element)
	{
		$matchingElement = array();
		$elementType = gettype($element);
		
		$simpleComparison = array(
			'boolean',
			'integer',
			'double',
			'string',
			'resource',
			'NULL'
		);
		
		foreach ($this -> elementList as $elementId => $elementRow) {
			if($elementType==gettype($elementRow))
			{
				if(in_array($elementType, $simpleComparison))
				{
					if($element===$elementRow) array_push($matchingElement, $elementId);
				}
				else if($elementType=='array') 
				{
					if(count(array_diff($element, $elementRow))==0) array_push($matchingElement, $elementId);
				}
				else if($elementType=='object')
				{
					if(method_exists($element, '__equalsTo') && $element->__equalsTo($elementRow)) array_push($matchingElement, $elementId);
				}
			}
		}
		
		return $matchingElement;
	}
	
	/**
	 * 
	 * 
	 * @return int Parent ID
	 */
	public function getParentId($elementId)
	{
		// TODO If the element is not found ??
		foreach ($this -> ancestorTable as $ancestorRow) {
			if($ancestorRow["descendant"] == $elementId)
			{
				return $ancestorRow["ancestor"];
			}
		}
	}
	
	/**
	 * 
	 * 
	 * @return array Array containing id of the chidren
	 */
	public function getChildrenId($elementId)
	{
		$children = array();
		foreach ($this -> ancestorTable as $ancestorRow) {
			if($ancestorRow["ancestor"] == $elementId)
			{
				array_push($children, $ancestorRow["descendant"]);
			}
		}
		
		return $children;
	}
	
	/**
	 * 
	 */
	public function getElementList()
	{
		return $this -> elementList;
	}
	
	/**
	 * 
	 * 
	 * 
	 * 
	 * @return string A string (html) representing the ClosureTable class
	 */
	public function __toString()
	{
		$closureTableString = '';
		
		$closureTableString .= '<h2>Element list</h2>';
		$closureTableString .= '<table border="1">';
		foreach ($this -> elementList as $elementId => $element) {
			$closureTableString .= '<tr><td>'.$elementId.'</td><td>'.$element.'</td></tr>';
		}
		
		$closureTableString .= '<table>';
		
		$closureTableString .= '<h2>Ancestor table</h2>';
		$closureTableString .= '<table border="1">';
		foreach ($this -> ancestorTable as $ancestorRow) {
			$closureTableString .= '<tr><td>'.$ancestorRow["ancestor"].'</td><td>'.$ancestorRow["descendant"].'</td></tr>';
		}
		
		$closureTableString .= '<table>';
		
		
		return $closureTableString;
	}
}

