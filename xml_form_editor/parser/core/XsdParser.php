<?php
// XXX Avoid infinite includes in lib
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/lib/XmlParserFunctions.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/lib/StringFunctions.php';

/**
 * An XSD Parser able to generate several element:
 *  - an XML form to fill in
 * 	- an XML file
 * TODO Clean the array from unused data (parent, SEQUENCE, COMPLEXTYPE, SCHEMA...)
 * TODO Handle several namespaces
 */ 
class XsdParser {
	private $xsdFile;
	
	private $xsdOriginalTree; // The tree as it is in the xsd file
	private $xsdOrganizedTree; // The tree reorganized as it should be shown in the configuration view
	private $xsdCompleteTree; // The tree as it should be in the form (with proper occurence)
	
	private $rootElements;
	private $namespaces;
	
	private $LOGGER;
	
	private static $LEVELS = array('DBG'=>'notice', 'NO_DBG'=>'info');
	private static $LOG_FILE;
	private static $FILE_NAME = 'XsdParser.php';
	
	private static $XSD_NS = 'http://www.w3.org/2001/XMLSchema';
	private static $NS_DEFINE_PREFIX = 'XMLNS';

	/**
	 * Parser constructor...
	 * 
	 */
	public function __construct()
	{
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'].'/logs/parser.log';	
		
		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 1: // new XsdParser(fileName)
				if(is_string($argv[0]))
				{
					$this->xsdFile = $argv[0];
					$this->xsdOriginalTree = new Tree();
					$this->xsdOrganizedTree = new Tree();
					$this->xsdCompleteTree = new Tree();
				}
				else 
				{
					$this->xsdFile = null;
					$this->xsdOriginalTree = null;
					$this->xsdOrganizedTree = null;
					$this->xsdCompleteTree = null;
				}
				
				$level = self::$LEVELS['NO_DBG'];	
				
				break;
			case 2: // new XsdParser(fileName, booleanDebug)
				if(is_string($argv[0]) && is_bool($argv[1]))
				{
					$this->xsdFile = $argv[0];
					
					if($argv[1])
					{
						$this->xsdOriginalTree = new Tree(true);
						$this->xsdOrganizedTree = new Tree(true);
						$this->xsdCompleteTree = new Tree(true);
						$level = self::$LEVELS['DBG'];
					}
					else 
					{
						$this->xsdOriginalTree = new Tree();
						$this->xsdOrganizedTree = new Tree();
						$this->xsdCompleteTree = new Tree();
						$level = self::$LEVELS['NO_DBG'];
					}
				}
				else 
				{
					$this->xsdFile = null;
					$this->xsdOriginalTree = null;
					$this->xsdOrganizedTree = null;
					$this->xsdCompleteTree = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				
				break;
			default:
				$this->xsdFile = null;
				$this->xsdOriginalTree = null;
				$this->xsdOrganizedTree = null;
				$this->xsdCompleteTree = null;
				$level = self::$LEVELS['NO_DBG'];
				break;
		}
		
		try
		{
			$this->LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);
		}
		catch (Exception $ex)
		{
			echo '<b>Impossible to build the Logger:</b><br/>'.$ex->getMessage();
		}
		
		if($this->xsdFile==null && $this->xsdOriginalTree==null && $this->xsdOrganizedTree==null && $this->xsdCompleteTree = null)
		{
			$log_mess = '';
			
			switch($argc)
			{
				case 1:
					$log_mess .= 'The argument must be a string ('.gettype($argv[0]).' given)';
					break;
				case 2:
					$log_mess .= 'Arguments must be {string, boolean} ({'.gettype($argv[0]).','.gettype($argv[1]).'} given)';
					break;
				default:
					$log_mess .= 'Constructor must be called with 1 or 2 arguments ('.$argc.' given)';
					break;
			}
			
			$this->LOGGER->log_error($log_mess, 'XsdParser::__construct');
		}
		else 
		{
			$this->LOGGER->log_debug('Parser created for file '.$this->xsdFile, 'XsdParser::__construct');
		}
	}

	/**
	 * Parse the schema as a regular XML document
	 * Store the tree into $this->xsdOriginalTree
	 * 
	 */
	private function parse() {
		global $elementTree;
		
		

		// Initialize the XML parser
		$parser=xml_parser_create();

		// Set handlers (see /lib/XmlParserFunctions)
		xml_set_element_handler($parser,"start","stop");
		xml_set_character_data_handler($parser,"char");

		$fp=fopen($this->xsdFile,"r");

		// Read data
		while ($data=fread($fp,4096))
		{
			xml_parse($parser,$data,feof($fp)) or
			die (sprintf("XML Error: %s at line %d",
					xml_error_string(xml_get_error_code($parser)),
					xml_get_current_line_number($parser)));
		}

		//Free the XML parser and close the file
		xml_parser_free($parser);
		fclose($fp);
		
		$this->xsdOriginalTree = $elementTree;
		$this->LOGGER->log_debug($this->xsdFile.' has been parsed', 'XsdParser::parse');
	}

	/**
	 * 
	 * 
	 */
	public function parseXsdFile()
	{
		$this->LOGGER->log_debug('Reading '.$this->xsdFile.'...', 'XsdParser::parseXsdFile');
		
		// Parse xsd with the PHP DOM parser
		$this->parse();
		
		// Find all the namespaces and register them
		$this->namespaces = array();
		$schemaElement = $this->xsdOriginalTree->getObject(0);
		$schemaAttributes = $schemaElement->getAttributes();
		$attributesName = array_keys($schemaAttributes);
		
		foreach($attributesName as $key)
		{
			if(preg_match('/^'.self::$NS_DEFINE_PREFIX.'\:/', $key))
			{
				$key_part = explode(':', $key);
				
				if($schemaAttributes[$key]==self::$XSD_NS)
				{
					$this->namespaces['default'] = $key_part[1];
					$this->LOGGER->log_debug('Namespace '.$key_part[1].' registered as the default namespace', 'XsdParser::__construct');
				}
				else 
				{
					array_push($this->namespaces, $key_part[1]);
					$this->LOGGER->log_debug('Namespace '.$key_part[1].' registered', 'XsdParser::__construct');
				}
			}
		}
		
		// Find the root element
		$this->rootElements = array();
		foreach($this->xsdOriginalTree->getChildren(0) as $child)
		{
			$childObject = 	$this->xsdOriginalTree->getObject($child);
			if($childObject->getType()==$this->namespaces['default'].':ELEMENT')
			{
				array_push($this->rootElements, $child);
			}
		}
		
		// Returning the rootElement
		if(count($this->rootElements)>1)
		{
			$this->LOGGER->log_info('Several root element found '.serialize($this->rootElements), 'XsdParser::buildTree');
			return $this->rootElements;
		}
		else if(count($this->rootElements)==1)
		{
			$this->LOGGER->log_debug('One root element found with ID '.$this->rootElements[0], 'XsdParser::buildTree');
			return $this->rootElements;
		}
		else 
		{
			$this->LOGGER->log_error('No root element found. Be sure the file is validate before parsing it.', 'XsdParser::buildTree');
			return null;
		}		
	}
	
	/**
	 * 
	 */
	public function buildOrganizedTree($rootElement)
	{
		$this->LOGGER->log_debug('Building $xsdOrganizedTree with root '.$rootElement, 'XsdParser::buildOrganizedTree');
		
		if(in_array($rootElement, $this->rootElements))
		{
			$this->insertTreeElement($rootElement);
			$this->optimizeTree();
		}
		else
		{
			$this->LOGGER->log_error('ID '.$rootElement.' is not one of the possible root element', 'XsdParser::buildOrganizedTree');
		}
	}
	
	/**
	 * 
	 */
	 // Computes minOccurs
	public function buildCompleteTree($elementId = 0)
	{
		if(!$this -> xsdCompleteTree -> hasElement()) $this -> xsdCompleteTree = clone $this -> xsdOrganizedTree;
		
		$elementObject = $this->xsdCompleteTree->getObject($elementId);
		$elementChildren = $this->xsdCompleteTree->getChildren($elementId);
		$elementAttr = $elementObject->getAttributes();
		
		foreach($elementChildren as $childId)
		{
			$this->buildCompleteTree($childId);
		}
		
		if(isset($elementAttr['MINOCCURS']) && $elementAttr['MINOCCURS']>1)
		{
			for($i=0; $i<$elementAttr['MINOCCURS']-1; $i++)
			{
				$this->xsdCompleteTree->copyTreeBranch($elementId);
			}
		}
	}
	
	
	/**
	 * NB: Recursive function
	 */
	private function insertTreeElement($elementId, $parentId = -1)
	{
		$elementObject = clone $this->xsdOriginalTree->getObject($elementId);
		$newParentId = $this->xsdOrganizedTree->insertElement($elementObject, $parentId);
		
		if($newParentId<0)
		{
			$this->LOGGER->log_error('Error '.$newParentId.' occured during the insertion of the following object '.serialize($elementObject).' (parent ID '.$parentId.')', 'XsdParser::insertTreeElement');
			return;
		}
		else 
		{
			$children = $this->xsdOriginalTree->getChildren($elementId);
			if(count($children) > 0)
			{
				foreach($children as $child)
				{
					$this->insertTreeElement($child, $newParentId);
				}
			}
			else 
			{
				$elementAttributes = $elementObject->getAttributes();
				$attributesNames = array_keys($elementAttributes);
				if(in_array("TYPE", $attributesNames))
				{
					$key_part = explode(':', $elementAttributes['TYPE']);
					
					if(!in_array(strtoupper($key_part[0]), $this->namespaces))
					{
						$comparisonElement = new XsdElement($this->namespaces['default'].':COMPLEXTYPE', array("NAME"=>$elementAttributes["TYPE"]));
						$arrayID = $this->xsdOriginalTree->getId($comparisonElement);
						
						if(count($arrayID)==1)
						{
							$this->insertTreeElement($arrayID[0], $newParentId);
						}
						else 
						{
							$this->LOGGER->log_error('The comparison found unusual number (!=1) of element like '.serialize($comparisonElement), 'XsdParser::insertTreeElement');
							return;
						}
					}
				}
			}	
		}
	}

	/**
	 * 
	 */
	// TODO Write a better function
	// todo create an array of element to remove
	private function optimizeTree()
	{
		$tree = $this->xsdOrganizedTree->getTree();
		
		foreach ($tree as $id=>$element) 
		{
			$object = $element['object'];
			
			if($object->getType()==$this->namespaces['default'].':COMPLEXTYPE' || $object->getType()==$this->namespaces['default'].':SEQUENCE' || $object->getType()==$this->namespaces['default'].':SIMPLETYPE')
			{
				$this->xsdOrganizedTree->removeElement($id);
			}
			
			//XXX Does not work for all the restriction
			if($object->getType()==$this->namespaces['default'].':RESTRICTION')
			{
				$parentId = $this->xsdOrganizedTree->getParent($id);
				$children = $this->xsdOrganizedTree->getChildren($id);
				
				$values = array();
				foreach($children as $child)
				{
					$attributes = $this->xsdOrganizedTree->getObject($child)->getAttributes();
					array_push($values, $attributes['VALUE']);
				}
							
				$this->xsdOrganizedTree->getObject($parentId)->addAttributes(array('RESTRICTION'=>$values));
				$this->xsdOrganizedTree->removeElement($id, true);
			}
		}
	}
	
	/**
	 * Getter for the XSD file name
	 */
	public function getSchemaFileName()
	{
		$this->LOGGER->log_notice('Function called', 'XsdParser::getSchemaFileName');
		return $this->getSchemaFileName();
	}
	
	/**
	 * 
	 */
	public function getXsdOriginalTree()
	{
		$this->LOGGER->log_notice('Function called', 'XsdParser::getxsdOriginalTree');
		return $this->xsdOriginalTree;
	}
	
	
	/**
	 * 
	 */
	public function getXsdOrganizedTree()
	{
		$this->LOGGER->log_notice('Function called', 'XsdParser::getXsdOrganizedTree');
		return $this->xsdOrganizedTree;
	}

	/**
	 * 
	 */
	public function setXsdOrganizedTree($newXsdOrganizedTree)
	{
		$this->LOGGER->log_notice('Function called', 'XsdParser::setXsdOrganizedTree');
		$this->xsdOrganizedTree = $newXsdOrganizedTree;
	}
	
	/**
	 * 
	 */
	public function getXsdCompleteTree()
	{
		$this->LOGGER->log_notice('Function called', 'XsdParser::getXsdCompleteTree');
		return $this->xsdCompleteTree;
	}
	
	/**
	 * 
	 */
	public function setXsdCompleteTree($newXsdCompleteTree)
	{
		$this->LOGGER->log_notice('Function called', 'XsdParser::setXsdCompleteTree');
		$this->xsdCompleteTree = $newXsdCompleteTree;
	}
	
	/**
	 * 
	 */
	public function __toString()
	{
		return 'Parser string';
	}
}
?>