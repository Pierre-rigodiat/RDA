<?php
/**
 * <Tree class>
 */
/**
 * Implement the "closure table" structure to represent the tree.
 * This class contains two arrays: 
 * <ul>
 * 		<li>List of elements</li>
 * 		<li>Ancestor table</li>
 * </ul>
 * 
 * 
 * 
 * @package XsdMan\Core
 */
class Tree {
	/**
	 * Array containing all elements
	 * @var array
	 */
	protected $elementList;
	
	/**
	 * Array linking all elements
	 * @var array
	 */
	protected $ancestorTable;
	
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
	 * Param ID is mandatory
	 * 
	 * 
	 * 
	 */
	public function __construct() 
	{
		// Initialize the logger (will throw an Exception if any problem occurs)
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'].'/logs/closure.log';
		$level = self::$LEVELS['DBG'];
		$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc)
		{
			case 1: // new Tree(idString)
				if(is_string($argv[0]))
				{
					$this->__ID = $argv[0];
					//$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					throw new Exception('Invalid parameters given to the object');
					//$level = self::$LEVELS['NO_DBG'];
				}
				
				break;
			/*case 2: // new Tree(idString, debug)
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
				throw new Exception('Invalid number of parameters given to the object');
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
	public function insert($element, $parentId = -1)
	{		
		// Add element in the element list
		$this -> elementList [ $this -> insertIndex ] = $element;
		
		// Insert into ancestor table
		$ancetorRow = array(
			"ancestor" => $parentId,
			"descendant" => $this -> insertIndex
		);
		
		array_push($this -> ancestorTable, $ancetorRow);
		
		$this -> insertIndex += 1;
		
		return ($this -> insertIndex - 1);
	}
	
	/**
	 * 
	 * 
	 * @param int $elementId Element index to delete
	 * @param boolean $recursively Says if it should delete recursively or not
	 */
	public function delete($elementId, $recursively = false)
	{
		// Delete element in list
		unset($this -> elementList [$elementId]);
		
		// Delete ancestorTable reference
		$children = $this -> getChildren($elementId);
		if(!$recursively)
		{
			$parent = $this -> getParent($elementId);
			
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
	 * @param mixed $element Element to match
	 * @return array Array of ID matching the given parameter
	 */
	public function find($element)
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
					if(method_exists($element, '__equalsTo') && $elementRow->__equalsTo($element)) array_push($matchingElement, $elementId);
				}
			}
		}
		
		return $matchingElement;
	}
	
	/**
	 * 
	 * 
	 * @param int $elementId Element index to change
	 * @param mixed $element Element to set
	 */
	public function setElement($elementId, $element)
	{
		$this -> elementList [ $elementId ] = $element;
	}
	
	/**
	 * 
	 * @param int Element index to return
	 * @return mixed Element stored at the given ID
	 */
	public function getElement($elementId)
	{
		return isset($this -> elementList [$elementId])?$this -> elementList [$elementId]:null;
	}
	
	/**
	 * 
	 * 
	 * @param int $elementId Element index to change
	 * @param int $parentId Parent to set
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
	 * @param int $elementId Element index of the child
	 * @return int Parent ID
	 */
	public function getParent($elementId)
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
	 * @param int $elementId Element index of the parent
	 * @return array Array containing id of the chidren
	 */
	public function getChildren($elementId)
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
	 * 
	 * @return array Element list
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
		$treeString = '';
		
		$treeString .= '<h2>Element list</h2>';
		$treeString .= '<table border="1">';
		foreach ($this -> elementList as $elementId => $element) {
			$treeString .= '<tr><td>'.$elementId.'</td><td>'.$element.'</td></tr>';
		}
		
		$treeString .= '<table>';
		
		$treeString .= '<h2>Ancestor table</h2>';
		$treeString .= '<table border="1">';
		foreach ($this -> ancestorTable as $ancestorRow) {
			$treeString .= '<tr><td>'.$ancestorRow["ancestor"].'</td><td>'.$ancestorRow["descendant"].'</td></tr>';
		}
		
		$treeString .= '<table>';
		
		return $treeString;
	}
}
