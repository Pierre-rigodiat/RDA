<?php
/**
 * 
 */
abstract class Handler implements HandlerInterface {
	/**
	 * Contain all tuples <elementId, handlerData> where elementId is an integer and handlerData a mixed value.
	 * @var array
	 */
	private $handlerData;
	
	
	public function __construct()
	{
		$this -> handlerData = array();
	}
	
	public function setHandlerDataForId($elementId, $handlerData)
	{
		
	}
	
	public function removeHandlerDataForId($elementId)
	{
		
	}
	
	public function getHandlerDataForId($elementId)
	{
		
	}
	
	/**
	 * 
	 * @return array MongoDB structure for the handler
	 */
	public function __toArray()
	{
		
	}
	
	/**
	 * 
	 * @return string Description of the handler
	 */
	public function __toString()
	{
		
	}
}
