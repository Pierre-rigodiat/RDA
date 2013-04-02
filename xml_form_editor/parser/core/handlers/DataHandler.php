<?php
/**
 * 
 */
class DataHandler extends Handler {
	/**
	 * 
	 * @var array
	 */
	private $dataArray;
	
	
	public function __construct() {
		
		$this -> dataArray = array();
		
	}
	
	public function setDataForId($elementId, $data)
	{
		$this -> dataArray [$elementId] = $data;
	}
	
	public function getDataForId($elementId)
	{
		return $this -> dataArray [$elementId];
	}
	
	public function saveData()
	{
		
		
		//$this -> dbConnection -> insertJson($this -> dataArray, 'exp-form');
	}
	
	public function retrieveData()
	{
		
	}
	
	/**
	 * 
	 */
	public function __toArray()
	{
		return $this -> dataArray;	
	}
	
	/**
	 * 
	 */
	public function __toString()
	{
		$dataHandlerString = '';
		
		foreach ($this -> dataArray as $elementId => $elementData) {
			$dataHandlerString .= $elementId.' | '.$elementData.'\n';
		}
		
		return $dataHandlerString;
	}
}
