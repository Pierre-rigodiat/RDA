<?php
/**
 * <ReferenceTree class>
 */
/**
 * A ReferenceTree is a Tree with another Tree object as reference.
 * 
 * 
 * @package XsdMan\Core
 */
class ReferenceTree extends Tree {
	/**
	 * Tree containing the real data
	 * @var Tree
	 */
	private $referenceTree;	
	
	private $LOGGER;
	private static $LEVELS = array('DBG'=>'notice', 'NO_DBG'=>'info');
	private static $LOG_FILE;
	private static $FILE_NAME = 'Tree.php';
	
	/**
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
			case 1: // new ReferenceTree(refTree)
				if(is_object($argv[0]) && get_class($argv[0]) == 'Tree')
				{
					parent::__construct("ReferenceTree");
					$this -> referenceTree = &$argv[0];
					
					
					//$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					throw new Exception('Invalid parameters given to the object');
					//$level = self::$LEVELS['NO_DBG'];
				}
				
				break;
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
	 */
	public function setReferenceTree($referenceTree)
	{
		$this -> referenceTree = &$referenceTree;
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
		array_push($this -> ancestorTable, array("ancestor" => $this -> getParent($baseElementId), "descendant" => $brotherElementId));
		
		$this -> ancestorTable = array_merge($this -> ancestorTable, $ancestorTableEnd);
	}
	
	/**
	 * 
	 */
	public function getSiblings($elementId)
	{
		$parentId = $this -> getParent($elementId);
		
		$brotherArray = array();
		foreach($this -> ancestorTable as $ancestorRow)
		{
			if($ancestorRow["ancestor"] == $parentId/* && $ancestorRow["descendant"] != $elementId*/)
			{
				array_push($brotherArray, $ancestorRow["descendant"]);
			}
		}
		
		$element = $this -> elementList [$elementId];
		
		foreach($brotherArray as $brotherId => $brother)
		{
			if($this -> elementList [$brother] != $element) unset($brotherArray[$brotherId]);
		}
		
		return $brotherArray;
	}
	
	/**
	 * 
	 * The parent ID of this element is automatically set to -1
	 * 
	 * 
	 * @return integer Created element id
	 */
	public function duplicate($elementId, $recursively = false)
	{		
		$elementToDuplicate = $this -> elementList [$elementId];
		if(is_object($elementToDuplicate)) $elementToDuplicate = clone $elementToDuplicate;
				
		$createdElementId = $this -> insert($elementToDuplicate);
		
		if($recursively)
		{
			foreach($this -> getChildren($elementId) as $childId)
			{
				$createdChildId = $this -> duplicate($childId, true);
				$this -> setParent($createdChildId, $createdElementId);
			}
		}
		
		return $createdElementId;
	}
	
	/**
	 * 
	 * @param int Element index to return
	 * @return mixed Element stored at the given ID
	 */
	public function getElement($elementId)
	{
		$this -> LOGGER -> log_notice('Getting ID '.$elementId.'...', 'ReferenceTree::getElement');
		if(isset($this -> elementList [$elementId]))
		{
			$this -> LOGGER -> log_notice('ID found. Getting original one...', 'ReferenceTree::getElement');
			return $this -> referenceTree -> getElement(
				$this -> elementList [$elementId]
			);
		}
		
		// $elementId has not been found in the element list
		$this -> LOGGER -> log_info('ID '.$elementId.' not found', 'ReferenceTree::getElement');
		return null;
	}
	
	public function getElementReferenceId($elementId)
	{
		return isset($this -> elementList [$elementId])?$this->elementList[$elementId]:null;
	}
}
