<?php

/**
 * Class used to map data between a schema and an ontology server (e.g. Neo4j)
 * 
 * @author pns3
 *
 */

class OntologyMapping {
	
	/**
	 * Array containing the gremlin queries
	 * 
	 * @var array
	 */
	private $queryId;
	
	/**
	 * Array containing the mapping information
	 * 
	 * @var array
	 */
	private $mappingTable;
	
	public function __construct() {
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch ($argc) {
			case 2:
				// new OntologyMapping($queryId, $mappingTable)
				$this->queryId = $argv[0];
				$this->mappingTable = $argv[1];
			case 1:
				// new OntologyMapping($queryId)
				$this->queryId = $argv[0];
				$this->mappingTable = array();
				break;
			default:
				$this->queryId = array();
				$this->mappingTable = array();
				break;
		}
	}
	
	public function getQueryId() {
		return $this->queryId;
	}
	
	public function setQueryId($queryId) {
		$this->queryId = array_values($queryId);
	}
	
	public function getMappingTable() {
		return $this->mappingTable;
	}
	
	public function setMappingTable($mappingTable) {
		$this->mappingTable = $mappingTable;
	}
	
	public function addQuery($query) {
		if ((array_search($query, $this->queryId)) === false) {
			$this->queryId[] = $query;
		}
		$id = array_search($query, $this->queryId);
		return $id;
	}
	
	public function removeQuery($query) {
		if(($queryKey = array_search($query, $this->queryId)) !== false) {
			//Remove the query from the queryId
   			unset($this->queryId[$queryKey]);
   			
   			if (($elementArray = array_keys($this->mappingTable, $queryKey)) !== array()) {
   				//Remove every element matching the query
   				foreach ($elementArray as $element)
   					unset($this->mappingTable[$element]);
   			}
   			
   			//Re-index the queryId and assign the new value in the mappingTable
   			$this->queryId = array_values($this->queryId);
   			foreach ($this->mappingTable as $element => $key) {
   				if ($key == $queryKey) {
   					unset($this->mappingTable[$element]);
   				}
   				elseif ($key > $queryKey) {
   					$this->mappingTable[$element] = $key-1;
   				}
   			}
   			
		}
	}
	
	/**
	 * You should use this to add elements to be queried in the ontology database
	 * 
	 * @param string $element
	 * @param string $query
	 */
	public function addElement($element, $query) {
		//Add the query in the queryId, if it doesn't exist yet, thus return the id
		$id = $this->addQuery($query);
		//Add the element to the mappingTable
		$this->mappingTable[$element] = $id;
	}
	
	public function removeElement($element) {
		if (isset($this->mappingTable[$element])) {
			unset($this->mappingTable[$element]);
		}
	}
	
	/**
	 * Get the Gremlin query for a given element
	 * 
	 * @param string $element
	 * @return string
	 */
	public function getQueryForElement($element) {
		if (array_key_exists($element, $this->mappingTable)) {
			return $this->queryId[$this->mappingTable[$element]];
		}
		else
			return '';
	}
	
}