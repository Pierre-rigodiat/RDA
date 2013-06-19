<?php

class QueryBuilder {
	
	/**
	 * Array containing query tree ids as keys and the value corresponding to the element
	 * @var array
	 */
	private $queryId;
	
	/**
	 * Tree related to the ids
	 * @var ReferenceTree
	 */
	private $queryTree;
	
	public function __construct() {
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc)
		{
			case 1 : //QueryBuilder($queryId)
				$this->queryId = $argv[0];
				break;
			case 2 : //Querybuilder($queryId, $queryTree)
				$this->queryId = $argv[0];
				$this->queryTree = $argv[1];
				break;
			default :
				break;
		}

	}
	
	public function getQueryId() {
		return $this->queryId;
	}
	
	public function setQueryId($queryId) {
		$this->queryId = $queryId;
	}
	
	public function getQueryTree() {
		return $this->queryTree;
	}
	
	public function setQueryTree($queryTree) {
		$this->queryTree = $queryTree;
	}
	

	public function buildQuery() {
		if (!isset($this->queryId)) {
			return null;
		}
		elseif ($this->queryId == array()) {
			return array();
		}
		if (!isset($this->queryTree)) {
			throw new Exception('Query Tree not referenced in the Query Builder');
		}
		else {
			$result = self::buildQueryPath(0);
			
			return $result;
		}
	}
	
	private function buildQueryPath($elementId) {
		$result = array();
		
		static $traited = array();
		
		$queryTree = $this->queryTree;
		
		$children = $queryTree->getChildren($elementId);
		
		$element = $queryTree->getElement($elementId);
		$attr = $element->getAttributes();
		
		$childrenArray = array();
		if ($children != array()) {
			foreach ($children as $childrenId) {
				if (!in_array($childrenId, $traited)) {
					$childrenPath = $this->buildElementPath($childrenId, $traited);
					if ($childrenPath != array())
						$childrenArray = array_merge($childrenArray, $childrenPath);
				}
			}
			if (isset($attr['MAXOCCURS']) && ($attr['MAXOCCURS'] == 'unbounded' || $attr['MAXOCCURS'] > 1) && count($childrenArray) > 1) {
				$childrenArray = array('$elemMatch' => $childrenArray);
			}
		}
		else {
			if (array_key_exists($elementId, $this->queryId) && ($this->queryId[$elementId] != '')) {
				if (!is_array($this->queryId[$elementId])) {
					$childrenArray = array('$' => $this->queryId[$elementId]);
				}
				else {
					$rangeArray = array();
					foreach ($this->queryId[$elementId] as $range) {
						$temp = preg_split('/ /', $range);
						$rangeArray = array_merge($rangeArray, array('$'.$temp[0] => (double) $temp[1]));
					}
					$childrenArray = array('$' => $rangeArray);
				}
			}
		}
		$result = $childrenArray;
		
		if (!$elementId) {
			$temp = array();
			$temp[] = $result;
			$result = $temp;
			$result = $this->buildLogicalPath($result, $elementId);
		}
		
		if ($result != array()) {
			//print_r($result);echo '<br/>';
		}
		
		return $result;
	}
	
	private function buildElementPath($elementId, $traited) {
		$result = array();
		
		$queryTree = $this->queryTree;
		$siblings = $queryTree->getSiblings($elementId);
		
		$siblingsArray = array();
		foreach ($siblings as $siblingsId) {
			$siblingPath = $this->buildQueryPath($siblingsId);
			if ($siblingPath != array()) {
				$siblingsArray[] = $siblingPath;
			}
			$traited[] = $siblingsId;
		}
		
		if ($siblingsArray != array()) {
		//print_r($siblingsArray);echo '<br/>';
		}
		
		$siblingsArray = $this->buildLogicalPath($siblingsArray, $elementId);
		
		return $siblingsArray;
		
	}
	
	private function buildLogicalPath($siblingsArray, $elementId) {
		
		$queryTree = $this->queryTree;
		$element = $queryTree->getElement($elementId);
		$attr = $element->getAttributes();
		$name = isset($attr['NAME']) ? lcfirst($attr['NAME']) : lcfirst($attr['REF']);
		
		if (!isset($attr['CHOICE']) && count($siblingsArray) > 0) {
			if (count($siblingsArray) == 1) {
				$childrenArray = $siblingsArray[0];
				$siblingsArray = array();
				
				foreach ($childrenArray as $childrenKey => $childrenValue) {
					if ($childrenKey == '$and') {
						$grandChildrenArray = array();
						foreach ($childrenValue as $grandChildren) {
							$temp = array();
							$temp[] = $grandChildren;
							$grandChildren = $temp;
							$grandChildrenArray[] = $this->buildLogicalPath($grandChildren, $elementId);
						}
						$siblingsArray = array_merge($siblingsArray, array($childrenKey => $grandChildrenArray));
					}
					elseif ($childrenKey != '$elemMatch') {
						$siblingsArray = array_merge($siblingsArray, array($name.'.'.$childrenKey => $childrenValue));
					}
					else {
						$siblingsArray = array_merge($siblingsArray, array($name => array($childrenKey => $childrenValue)));
					}
				}
				
			}
			elseif (count($siblingsArray) > 1) {
				$children = $queryTree->getChildren($elementId);
				if ($children == array()) {
					$siblingsArray = array($name => array('$all' => $siblingsArray));
				}
				else {
					//echo '1<br/>';print_r($siblingsArray);echo '<br/>';
					foreach ($siblingsArray as $siblingKey => $siblingValue) {
						//echo $siblingKey.' ';print_r($siblingValue); echo '<br/>';
						if (!in_array('$elemMatch', array_keys($siblingValue))) {
							$temp = array();
							foreach($siblingValue as $key => $value)
								$temp[$name.'.'.$key] = $value;
							$siblingsArray[$siblingKey] = $temp;
						}
						else {
							$siblingsArray[$siblingKey] = array($name => $siblingValue);
						}
					}
						
					$siblingsArray = array('$and' => $siblingsArray);
				}
			}
		}
		else {
			if ($siblingsArray != array()) {
				$childrenArray = $siblingsArray[0];
				$siblingsArray = $childrenArray;
			}
		}
		
		return $siblingsArray;
	}
	
}