<?php
require_once '../parser/core/XsdElement.php';

class XsdElementUnitTest extends UnitTestCase 
{	
	private $validNames = array(
		'xs:element'
	);
	
	private $invalidNames = array(
		null,
		10000,
		TRUE,
		array(),
		array('test', TRUE),
		array('name' => 'value')
	);
	
	/**
	 * Test the building of elements with invalid names
	 */
	function testCreateElementWithInvalidName()
	{
		foreach($this -> invalidNames as $index => $invalidName)
		{
			try {
				$xsdElement = new XsdElement($invalidName, array());
				$this -> fail('Exception should be thrown for name at index '.$index);
			} 
			catch(Exception $e){}
		}
		
		$this -> pass();
	}
	
	/**
	 * Test the building of elements with valid names
	 */
	function testCreateElementWithValidName()
	{
		foreach($this -> validNames as $index => $validName)
		{
			try {
				$xsdElement = new XsdElement($validName, array());
			} 
			catch(Exception $e){
				$this -> fail('Unexpected exception thrown for name at index '.$index);
			}
		}
		
		$this -> pass();
	}
	
	/**
	 * 
	 */
	function testCreateElementWithInvalidAttributes()
	{
		
	}
	
	/**
	 * 
	 */
	function testCreateElementWithValidAttributes()
	{
		
	}
	
	/**
	 * 
	 */
	function testAddAttributeFunction()
	{
		
	}
	
	/**
	 * 
	 */
	function testRemoveAttributeFunction()
	{
		
	}
	
	/**
	 * 
	 */
	function testGetTypeFunction()
	{
		
	}
	
	/**
	 * 
	 */
	function testGetAttributesFunction()
	{
		
	}	
}

