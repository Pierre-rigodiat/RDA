<?php

class SearchHandler {
	
	private $idArray; //Array containing the element id available in the search page
	
	
	public function __construct(){

		$argc = func_num_args();
		$argv = func_get_args();
		
		switch ($argc) {
			case 1:
				// new SearchHandler($idArray)
				$this->idArray = $argv[0];
				break;
			default:
				$this->idArray = array();
		}
	}
	
	public function getIdArray() {
		return $this->idArray;
	}
	
	public function setIdArray($idArray) {
		$this->idArray = $idArray;
	}
	
	public function addId($id) {
		if (is_array($id)){
			$this->idArray = array_merge($this->idArray,$id);
		}
		else {
			$this->idArray[] = $id;
		}
		$this->idArray = array_values(array_unique($this->idArray));
	}
	
	public function removeId($id) {
		if (is_array($id)) {
			$this->idArray = array_diff($this->idArray, $id);
		}
		else {
			$this->idArray = array_diff($this->idArray, array($id));
		}
		$this->idArray = array_values($this->idArray);
	}
	
}