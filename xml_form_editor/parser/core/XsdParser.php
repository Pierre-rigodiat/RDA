<?php
// XXX Avoid infinite includes in lib
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
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
	private $xsdTree;
	private $xmlFormTree;
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
					$this->xsdTree = new Tree();
					$this->xmlFormTree = new Tree();
				}
				else 
				{
					$this->xsdFile = null;
					$this->xsdTree = null;
					$this->xmlFormTree = null;
				}
				
				$level = self::$LEVELS['NO_DBG'];	
				
				break;
			case 2: // new XsdParser(fileName, booleanDebug)
				if(is_string($argv[0]) && is_bool($argv[1]))
				{
					$this->xsdFile = $argv[0];
					
					if($argv[1])
					{
						$this->xsdTree = new Tree(true);
						$this->xmlFormTree = new Tree(true);
						$level = self::$LEVELS['DBG'];
					}
					else 
					{
						$this->xsdTree = new Tree();
						$this->xmlFormTree = new Tree();
						$level = self::$LEVELS['NO_DBG'];
					}
				}
				else 
				{
					$this->xsdFile = null;
					$this->xsdTree = null;
					$this->xmlFormTree = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				
				break;
			default:
				$this->xsdFile = null;
				$this->xsdTree = null;
				$this->xmlFormTree = null;
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
		
		if($this->xsdFile==null && $this->xsdTree==null && $this->xmlFormTree==null)
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
	 * 
	 * 
	 */
	public function parseXsdFile()
	{
		// Parse xsd with the PHP DOM parser
		$this->parse();
		
		// Find all the namespaces and register them
		$this->namespaces = array();
		$schemaElement = $this->xsdTree->getObject(0);
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
		foreach($this->xsdTree->getChildren(0) as $child)
		{
			$childObject = 	$this->xsdTree->getObject($child);
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
	public function buildTree($rootElement)
	{
		if(in_array($rootElement, $this->rootElements))
		{
			$this->insertTreeElement($rootElement);
			$this->optimizeTree();
			
			//$this->computeMinOccurs(0);
		}
		else
		{
			$this->LOGGER->log_error('ID '.$rootElement.' is not one of the possible root element', 'XsdParser::buildTree');
		}
	}
	
	/**
	 * 
	 */
	public function getXmlFormTree()
	{
		$this->LOGGER->log_notice('Function called', 'XsdParser::getXmlFormTree');
		return $this->xmlFormTree;
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
	 * Parse the schema as a regular XML document
	 * Store the tree into $this->xsdTree
	 * 
	 */
	private function parse() {
		global $elementTree;
		
		$this->LOGGER->log_debug($this->xsdFile.' will be read...', 'XsdParser::parse');

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
		
		$this->xsdTree = $elementTree;
		$this->LOGGER->log_debug($this->xsdFile.' has been read and its content is stored in the tree', 'XsdParser::parse');
	}
	
	/**
	 * 
	 */
	private function insertTreeElement($elementId, $parentId = -1)
	{
		$elementObject = clone $this->xsdTree->getObject($elementId);
		$newParentId = $this->xmlFormTree->insertElement($elementObject, $parentId);
		
		if($newParentId<0)
		{
			$this->LOGGER->log_error('Error '.$newParentId.' occured during the insertion of the following object '.serialize($elementObject).' (parent ID '.$parentId.')', 'XsdParser::insertTreeElement');
			return;
		}
		else 
		{
			$children = $this->xsdTree->getChildren($elementId);
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
						$arrayID = $this->xsdTree->getId($comparisonElement);
						
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
		$tree = $this->xmlFormTree->getTree();
		
		foreach ($tree as $id=>$element) 
		{
			$object = $element['object'];
			
			if($object->getType()==$this->namespaces['default'].':COMPLEXTYPE' || $object->getType()==$this->namespaces['default'].':SEQUENCE' || $object->getType()==$this->namespaces['default'].':SIMPLETYPE')
			{
				$this->xmlFormTree->removeElement($id);
			}
			
			//XXX Does not work for all the restriction
			if($object->getType()==$this->namespaces['default'].':RESTRICTION')
			{
				$parentId = $this->xmlFormTree->getParent($id);
				$children = $this->xmlFormTree->getChildren($id);
				
				$values = array();
				foreach($children as $child)
				{
					$attributes = $this->xmlFormTree->getObject($child)->getAttributes();
					array_push($values, $attributes['VALUE']);
				}
							
				$this->xmlFormTree->getObject($parentId)->addAttributes(array('RESTRICTION'=>$values));
				$this->xmlFormTree->removeElement($id, true);
			}
		}
	}

	/**
	 * 
	 */
	public function computeMinOccurs($elementId = 0)
	{
		$elementObject = $this->xmlFormTree->getObject($elementId);
		$elementChildren = $this->xmlFormTree->getChildren($elementId);
		$elementAttr = $elementObject->getAttributes();
		
		foreach($elementChildren as $childId)
		{
			$this->computeMinOccurs($childId);
		}
		
		if(isset($elementAttr['MINOCCURS']) && $elementAttr['MINOCCURS']>1)
		{
			for($i=0; $i<$elementAttr['MINOCCURS']-1; $i++)
			{
				$this->xmlFormTree->copyTreeBranch($elementId);
			}
		}
	}
}
?>