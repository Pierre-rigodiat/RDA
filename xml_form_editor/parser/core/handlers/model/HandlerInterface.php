<?php
/**
 * <HandlerInterface interface>
 */
/**
 * 
 * 
 * @package XsdMan\Handler\Model
 */
interface HandlerInterface
{	
	public function setHandlerDataForId($elementId, $handlerData);
	
	public function removeHandlerDataForId($elementId);
	
	public function clearHandlerData();
	
	public function getHandlerDataForId($elementId);
	
	public function __toArray();
	
	public function __toString();
}