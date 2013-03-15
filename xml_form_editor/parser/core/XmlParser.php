<?php
/**
 * <XmlParser class>
 */
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/ClosureTable.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
/**
 * 
 * 
 * 
 * 
 */
class XmlParser
{	
	private $tree;
	
	private $stack;
	private $level;
	private $objectId;
	
	// TODO Add a logger
	
	public function __construct()
	{	
		$this -> tree = new ClosureTable("xmlParserTree");
		
		$this -> stack = array();
		$this -> level = 0;
		$this -> objectId = 0;
	}
	
	
	/**
	 * Parse the schema as a regular XML document
	 * Store the tree into $this->xsdOriginalTree
	 *
	 * @param
	 */
	public function parse($fileName)
	{
		// Initialize the XML parser
		$parser = xml_parser_create();

		// Set handlers (see /lib/XmlParserFunctions)
		xml_set_element_handler($parser, array(&$this, "parseElementOpen"), array(&$this, "parseElementClose"));

		$fp = fopen($fileName, "r");

		// Read data
		while ($data = fread($fp, 4096))
		{
			xml_parse($parser, $data, feof($fp)) or die(sprintf("XML Error: %s at line %d", xml_error_string(xml_get_error_code($parser)), xml_get_current_line_number($parser)));
		}

		//Free the XML parser and close the file
		xml_parser_free($parser);
		fclose($fp);

		//$this -> LOGGER -> log_debug($this -> xsdFile . ' has been parsed', 'XsdManager::parse');
	}
	
	/**
	 * 
	 */
	private function parseElementOpen($parser, $elementName, $elementAttr)
	{
		/**
		 * Store the element into the elementList
		 */
		// Find the parent of the element
		$parent = -1;
		if($this -> level > 0) {
			$parent = $this -> stack[$this -> level-1];
		}
		
		// Create the element and insert it
		$element = new XsdElement($elementName, $elementAttr/*, true*/);
		$id = $this -> tree -> insertElement($element, $parent);
		
		$this -> objectId += 1;
		
		//$LOGGER->log_debug('New element '.$elementName.' inserted', 'start');
	
		/**
		 * Updating the stack
		 */
		// Add the element to the stack
		$this -> stack[$this -> level] = $id;
	
		// Increment the level
		$this -> level += 1;
	}

	/**
	 * 
	 */
	private function parseElementClose($parser, $elementName)
	{
		/**
		 * Updating the stack
		 */
	
		// Decrease the level
		$this -> level -= 1;
	
		// Remove the stack element
		$this -> stack[$this -> level] = null;
		
		//$LOGGER->log_debug('End reading '.$elementName, 'stop');
	}
	
	/**
	 * 
	 */
	public function getParsingData()
	{		
		return $this -> tree;
	}
	
	public function __toString()
	{
		$xmlParserString = '';
		
		/*foreach ($this -> elementList as $element) {
			$xmlParserString .= $element;
		}*/
		
		return $xmlParserString;
	}
}









