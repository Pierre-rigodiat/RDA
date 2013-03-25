<?php
/**
 * <XsdManager class>
 */
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/lib/XmlParserFunctions.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/lib/StringFunctions.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/helpers/Logger.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/XsdElement.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/PageHandler.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/ModuleHandler.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/SearchHandler.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/XmlParser.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/Tree.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/ReferenceTree.php';
/**
 * <b>Handle the schema configuration and value. It is the backbone of the software</b>
 * 
 * XsdManager object instantiate a lot of different objects to be able to have all the schema information and the filling values.
 * It deals with:
 * <ul>
 * 	<li>3 trees</li>
 * 	<li>PageHandler</li>
 * 	<li>ModuleHandler</li>
 * </ul>
 * 
 * 
 * 
 * --- REWRITE ----
 * An XSD Parser able to generate several element:
 *  - an XML form to fill in
 * 	- an XML file
 * 
 * --- END REWRITE --- 
 * 
 * 
 * @uses core\ModuleHandler
 * @TODO Clean the array from unused data (parent, SEQUENCE, COMPLEXTYPE, SCHEMA...)
 * @TODO Handle several namespaces
 * @TODO For getter and setter, verify the type of parameters
 *
 *
 * 
 * @author P. Dessauw <philippe.dessauw@nist.gov>
 * @copyright NIST 2013
 * 
 * @package XsdMan\Core
 */
class XsdManager
{
	/**
	 * 
	 * @var string
	 */
	private $xsdFile;

	/**
	 * The tree as it is in the xsd file
	 * 
	 * @var Tree
	 */
	private $xsdOriginalTree;
	
	/**
	 * The tree as it should be in the form (with proper occurence)
	 * @var ReferenceTree
	 */
	private $xsdCompleteTree;
	
	/**
	 * The tree as it should be in the query form (with proper occurence)
	 * @var ReferenceTree
	 */
	private $xsdQueryTree;
	
	// The array containing the values entered by the user
	/**
	 * 
	 * 
	 * @var array
	 */
	private $dataArray;

	// Handlers
	/**
	 * Page handler
	 * @var XsdMan\Core\PageHandler
	 */
	private $pageHandler;
	private $moduleHandler;
	private $searchHandler;

	private $rootElements;
	private $namespaces;

	private static $XSD_NS = 'http://www.w3.org/2001/XMLSchema';
	private static $NS_DEFINE_PREFIX = 'XMLNS';
	
	/**
	 * Logging information
	 */
	/** @ignore */
	private $LOGGER;
	/** @ignore */
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	/** @ignore */
	private static $LOG_FILE;
	/** @ignore */
	private static $FILE_NAME = 'XsdManager.php';

	/**
	 * Parser constructor...
	 * @param {string} Schema file name
	 * @param {PageHandler} An initialized PageHandler object
	 * @param {ModuleHandler} An initialized ModuleHandler object
	 * @param {boolean} Debug (optional)
	 *
	 */
	public function __construct()
	{
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'] . '/logs/parser.log';
		$level = self::$LEVELS['DBG'];
		$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 3 :
				// new XsdManager(fileName, pageHandler, moduleHandler)
				if (is_string($argv[0]) && is_object($argv[1]) && get_class($argv[1]) == 'PageHandler' && is_object($argv[2]) && get_class($argv[2]) == 'ModuleHandler')
				{
					$this -> xsdFile = $argv[0];

					$this -> xsdOriginalTree = new Tree("OriginalTree");
					$this -> xsdCompleteTree = new ReferenceTree($this->xsdOriginalTree);
					$this -> xsdQueryTree = new ReferenceTree($this->xsdOriginalTree);
					$this -> dataArray = array();

					$this -> pageHandler = $argv[1];
					$this -> moduleHandler = $argv[2];
					$this -> searchHandler = new SearchHandler();
				}
				else
				{
					//TODO Log
					throw new Exception('Invalid param');
				}

				break;
			case 4 :
				// new XsdManager(fileName, pageHandler, moduleHandler, booleanDebug)
				if (is_string($argv[0]) && is_object($argv[1]) && get_class($argv[1]) == 'PageHandler' && is_object($argv[2]) && get_class($argv[2]) == 'ModuleHandler' && is_bool($argv[3]))
				{
					$this -> xsdFile = $argv[0];

					$this -> pageHandler = $argv[1];
					$this -> moduleHandler = $argv[2];
					$this -> searchHandler = new SearchHandler();

					if ($argv[1])
					{
						//TODO Set debug
						$this -> xsdOriginalTree = new Tree("OriginalTree");
						$this -> xsdCompleteTree = new ReferenceTree($this->xsdOriginalTree);
						$this -> xsdQueryTree = new ReferenceTree($this->xsdOriginalTree);
						$this -> dataArray = array();
						$level = self::$LEVELS['DBG'];
					}
					else
					{
						$this -> xsdOriginalTree = new Tree("OriginalTree");
						$this -> xsdQueryTree = new ReferenceTree($this->xsdOriginalTree);
						$this -> xsdCompleteTree = new ReferenceTree($this->xsdOriginalTree);
						$this -> dataArray = array();
						$level = self::$LEVELS['NO_DBG'];
					}
				}
				else
				{
					//TODO Log
					throw new Exception('Invalid param');
					/*$this -> xsdFile = null;
					$level = self::$LEVELS['NO_DBG'];*/
				}

				break;
			default :
				//TODO Log
				throw new Exception('Invalid param');
				break;
		}

		$this -> LOGGER -> log_debug('Manager created for file ' . $this -> xsdFile, 'XsdManager::__construct');
	}

	/**
	 *
	 *
	 */
	public function parseXsdFile()
	{
		$this -> LOGGER -> log_debug('Reading ' . $this -> xsdFile . '...', 'XsdManager::parseXsdFile');

		// Parse xsd with the PHP DOM parser
		$this -> parse();

		// Find all the namespaces and register them
		$this -> namespaces = array();
		$schemaElement = $this -> xsdOriginalTree -> getElement(0);
		//$schemaElement = $this -> xsdElementList[$schemaElementId];
		
		$schemaAttributes = $schemaElement -> getAttributes();
		$attributesName = array_keys($schemaAttributes);

		foreach ($attributesName as $key)
		{
			if (preg_match('/^' . self::$NS_DEFINE_PREFIX . '\:/', $key))
			{
				$key_part = explode(':', $key);

				if ($schemaAttributes[$key] == self::$XSD_NS)
				{
					$this -> namespaces['default']['name'] = $key_part[1];
					$this -> namespaces['default']['url'] = $schemaAttributes[$key];
					
					$this -> LOGGER -> log_debug('Namespace ' . $key_part[1] . ' registered as the default namespace', 'XsdManager::__construct');
				}
				else
				{
					$nsEntry = array(
						'name' => $key_part[1],
						'url' => $schemaAttributes[$key]
					);
					
					array_push($this -> namespaces, $nsEntry);
					$this -> LOGGER -> log_debug('Namespace ' . $key_part[1] . ' registered', 'XsdManager::__construct');
				}
			}
		}
		
		$this -> cleanParsingData();

		// Find the root element
		$this -> rootElements = array();
		foreach ($this->xsdOriginalTree->getChildren(0) as $child)
		{
			$childObject = $this -> xsdOriginalTree -> getElement($child);
						
			if ($childObject -> getType() == $this -> namespaces['default']['name'] . ':ELEMENT')
			{
				array_push($this -> rootElements, $child);
			}
		}

		// Returning the rootElement
		if (count($this -> rootElements) > 1)
		{
			$this -> LOGGER -> log_info('Several root element found ' . arrayToString($this -> rootElements), 'XsdManager::buildTree');
			return $this -> rootElements;
		}
		else if (count($this -> rootElements) == 1)
		{
			$this -> LOGGER -> log_debug('One root element found with ID ' . $this -> rootElements[0], 'XsdManager::buildTree');
			return $this -> rootElements;
		}
		else
		{
			$this -> LOGGER -> log_error('No root element found. Be sure the file is validate before parsing it.', 'XsdManager::buildTree');
			return null;
		}
	}


	/**
	 * Parse the schema as a regular XML document
	 * Store the tree into $this->xsdOriginalTree
	 *
	 */
	private function parse()
	{
		$xmlParser = new XmlParser();
		$xmlParser -> parse($this -> xsdFile);
		
		$this -> xsdOriginalTree = $xmlParser -> getParsingData();
		
		$this -> LOGGER -> log_debug($this -> xsdFile . ' has been parsed', 'XsdManager::parse');
	}


	private function cleanParsingData()
	{
		$elementToDelete = array(
			"simply" => array(
				"SEQUENCE",
				"IMPORT",
				"INCLUDE"
			),
			"recursively" => array(
				"ANNOTATION"
			)
		);
		
		$elementList = $this -> xsdOriginalTree -> getElementList();
		$defaultNS = $this -> namespaces['default']['name'].':';
		$namespaceLength = strlen($defaultNS);
		
		
		foreach ($elementList as $elementId => $xsdElement)
		{
			$this -> LOGGER -> log_debug('Optimizing tree for ID ' . $elementId . '('.$xsdElement.')...', 'XsdManager::cleanParsingData');
			
			$xsdElementType = substr($xsdElement -> getType(), $namespaceLength);
			
			if(startsWith($xsdElement -> getType(), $defaultNS))
			{
				if(in_array($xsdElementType, $elementToDelete["simply"]))
				{
					// TODO logging
					$this -> xsdOriginalTree -> delete($elementId);
					$this -> LOGGER -> log_debug('ID '.$elementId.' deleted', 'XsdManager::cleanParsingData');
				}
				
				if(in_array($xsdElementType, $elementToDelete["recursively"]))
				{
					// TODO logging
					$this -> xsdOriginalTree -> delete($elementId, true);
					$this -> LOGGER -> log_debug('ID '.$elementId.' deleted', 'XsdManager::cleanParsingData');
				}
			}
		}
	}



	public function getRootElements()
	{
		return $this -> rootElements;
	}

	/**
	 *
	 * 
	 * TODO Rename this function
	 */
	public function buildOrganizedTree($rootElement)
	{
		$this -> LOGGER -> log_debug('Building $xsdOriginalTree...', 'XsdManager::buildOrganizedTree');

		if (in_array($rootElement, $this -> rootElements))
		{
			$tempTree = new Tree("TempTree");
			$this -> createOriginalTree($tempTree, $rootElement);
			
			$this -> xsdOriginalTree = clone $tempTree;
			$tempTree = null;
			
			$this -> cleanXsdTree();
			$this -> xsdCompleteTree -> setReferenceTree($this -> xsdOriginalTree);
			$this -> xsdQueryTree -> setReferenceTree($this -> xsdOriginalTree);
			
		}
		else
		{
			$this -> LOGGER -> log_error('ID ' . $rootElement . ' is not one of the possible root element', 'XsdManager::buildOrganizedTree');
		}
	}


	/**
	 * NB: Recursive function
	 * 
	 * 
	 * @param ClosureTable $tempTree The new tree we are building
	 * @param int $elementId Element ID to insert
	 * @param int $parentId Parent ID of the current element
	 */
	private function createOriginalTree($tempTree, $elementId = 0, $parentId = -1)
	{
		$xsdElement = $this -> xsdOriginalTree -> getElement($elementId);
		$newParentId = $tempTree -> insert($xsdElement, $parentId);

		if ($newParentId < 0)
		{
			$this -> LOGGER -> log_error('Error ' . $newParentId . ' occured when inserting ID ' . $elementId . ' (parent ID ' . $parentId . ')', 'XsdManager::insertTreeElement');
			return;
		}
		else
		{
			//$xsdElement = $this -> xsdElementList[$xsdElementId];
			$xsdElementAttr = $xsdElement -> getAttributes();
			
			$children = $this -> xsdOriginalTree -> getChildren($elementId);
			if (count($children) > 0)
			{
				foreach ($children as $child)
				{
					$this -> createOriginalTree($tempTree, $child, $newParentId);
				}
			}
			else
			{
				if(isset($xsdElementAttr['TYPE']))
				{
					$typePart = explode(':', $xsdElementAttr['TYPE']);
					
					/* Try to find out if the namespace is declared */
					$isNamespaceDeclared = false;
					foreach($this -> namespaces as $nsDefinition)
					{
						if($nsDefinition['name'] == strtoupper($typePart[0]))
						{
							$isNamespaceDeclared = true;
							break;
						}
					}
					
					/* Undeclared namespace means that the element has to be linked */
					// XXX An undeclared namespace will raise an error (element not found in the current tree)
					if (!$isNamespaceDeclared)
					{
						/* Build a complexType element as comparison */
						$comparisonElement = new XsdElement($this -> namespaces['default']['name'] . ':COMPLEXTYPE', array("NAME" => $xsdElementAttr["TYPE"]));
						$matchingIdArray = $this -> xsdOriginalTree -> find($comparisonElement);

						if (count($matchingIdArray) == 1)
						{
							$this -> createOriginalTree($tempTree, $matchingIdArray[0], $newParentId);
						}
						else
						{
							/* Build a simpleType element as comparison */
							$comparisonElement = new XsdElement($this -> namespaces['default']['name'] . ':SIMPLETYPE', array("NAME" => $xsdElementAttr["TYPE"]));
							$matchingIdArray = $this -> xsdOriginalTree -> find($comparisonElement);
							
							if (count($matchingIdArray) == 1)
							{
								$this -> createOriginalTree($tempTree, $matchingIdArray[0], $newParentId);
							}
							else
							{
								$this -> LOGGER -> log_error('The comparison found unusual number ('.count($matchingIdArray).'!=1) of element like ' . $comparisonElement, 'XsdManager::insertTreeElement');
								return;
							}
						}
					}
				}
			}
		}
	}
	
	/**
	 * 
	 */
	private function cleanXsdTree()
	{
		$elementToDelete = array(
			"simply" => array(
				"COMPLEXTYPE",
				"SIMPLETYPE",
				/*"SEQUENCE",
				"IMPORT",
				"INCLUDE"*/
			),
			"recursively" => array(
				//"ANNOTATION"
			)
		);
		
		$elementList = $this -> xsdOriginalTree -> getElementList();
		$defaultNS = $this -> namespaces['default']['name'].':';
		$namespaceLength = strlen($defaultNS);
		
		
		foreach ($elementList as $elementId => $xsdElement)
		{
			$this -> LOGGER -> log_debug('Optimizing tree for ID ' . $elementId . '...', 'XsdManager::cleanXsdTree');
			
			//$xsdElement = $this -> xsdElementList[$element['object']]; 
			$xsdElementType = substr($xsdElement -> getType(), $namespaceLength);
			
			if(startsWith($xsdElement -> getType(), $defaultNS))
			{
				if(in_array($xsdElementType, $elementToDelete["simply"]))
				{
					// TODO logging
					$this -> xsdOriginalTree -> delete($elementId);
				}
				
				if(in_array($xsdElementType, $elementToDelete["recursively"]))
				{
					// TODO logging
					$this -> xsdOriginalTree -> delete($elementId, true);
				}
			}
			
			/* Choice element optimization */
			if($xsdElement -> getType() == $defaultNS . 'CHOICE')
			{
				// Create a new XsdElement allowing choice between all elements
				$children = $this -> xsdOriginalTree -> getChildren($elementId);
				$xsdElement = new XsdElement($defaultNS . 'ELEMENT', array('NAME' => 'choose', 'CHOICE' => $children));
				$this -> xsdOriginalTree -> setElement($elementId, $xsdElement);
			}

			/* Restriction element configuration */
			//FIXME Does not work for all the restriction
			if ($xsdElement -> getType() == $defaultNS . 'RESTRICTION')
			{
				$children = $this -> xsdOriginalTree -> getChildren($elementId);

				$values = array();
				foreach ($children as $child)
				{
					$attributes = $this -> xsdOriginalTree -> getElement($child) -> getAttributes();
					array_push($values, $attributes['VALUE']);
				}
				
				$parentId = $this -> xsdOriginalTree -> getParent($elementId);
				$this -> xsdOriginalTree -> getElement($parentId) -> addAttributes(array('RESTRICTION' => $values));

				$this -> LOGGER -> log_debug('ID ' . $parentId . ' contains restriction values ' . $this -> xsdOriginalTree -> getElement($parentId), 'XsdManager::optimizeTree');

				$this -> xsdOriginalTree -> delete($elementId, true);
				$this -> LOGGER -> log_debug('ID ' . $elementId . ' (orga) removed (restriction)', 'XsdManager::optimizeTree');

			}
		}
	}

	/**
	 * Build the complete tree. Compute minOccurs
	 * 
	 * @param int $elementId Element index to build
	 */
	public function buildCompleteTree($elementId = 0, $parentId = -1)
	{
		$insertedId = $this -> xsdCompleteTree -> insert(
			$elementId, 
			$parentId
		);
		$this -> LOGGER -> log_debug('ID '.$insertedId.' (father: '.$parentId.') inserted into the tree', 'XsdManager::buildCompleteTree');

		$childrenId = $this -> xsdOriginalTree -> getChildren($elementId);
		foreach ($childrenId as $childId)
		{
			$this -> buildCompleteTree($childId, $insertedId);
		}

		/* Duplicate elements with minOccurs > 1 */
		$this -> LOGGER -> log_notice('Analyzing ID '.$insertedId.'...', 'XsdManager::buildCompleteTree');
		$elementObject = $this -> xsdCompleteTree -> getElement($insertedId);
		$elementAttr = $elementObject -> getAttributes();
		
		if (isset($elementAttr['MINOCCURS']) && $elementAttr['MINOCCURS'] > 1)
		{
			$parentId = $this -> xsdCompleteTree -> getParent($insertedId);
			
			for ($i = 0; $i < $elementAttr['MINOCCURS'] - 1; $i++)
			{
				$newElementId = $this -> xsdCompleteTree -> duplicate($insertedId, true);
				$this -> xsdCompleteTree -> setBrother($insertedId, $newElementId);
				
				$this -> copyPageArray($insertedId, $newElementId);
			}
		}
	}
	
	/**
	 * Build the query tree. Compute minOccurs
	 *
	 * @param int $elementId Element index to build
	 */
	public function buildQueryTree($elementId = 0, $parentId = -1)
	{
		$insertedId = $this -> xsdQueryTree -> insert(
				$elementId,
				$parentId
		);
		$this -> LOGGER -> log_debug('ID '.$insertedId.' (father: '.$parentId.') inserted into the query tree', 'XsdManager::buildQueryTree');
	
		$childrenId = $this -> xsdOriginalTree -> getChildren($elementId);
		foreach ($childrenId as $childId)
		{
			$this -> buildQueryTree($childId, $insertedId);
		}
	
		/* Duplicate elements with minOccurs > 1 */
		$this -> LOGGER -> log_notice('Analyzing ID '.$insertedId.'...', 'XsdManager::buildQueryTree');
		$elementObject = $this -> xsdQueryTree -> getElement($insertedId);
		$elementAttr = $elementObject -> getAttributes();
	
		if (isset($elementAttr['MINOCCURS']) && $elementAttr['MINOCCURS'] > 1)
		{
			$parentId = $this -> xsdQueryTree -> getParent($insertedId);
				
			for ($i = 0; $i < $elementAttr['MINOCCURS'] - 1; $i++)
			{
			$newElementId = $this -> xsdQueryTree -> duplicate($insertedId, true);
			$this -> xsdQueryTree -> setBrother($insertedId, $newElementId);
	
			}
		}
	}
	
	/**
	 * 
	 */
	private function copyPageArray($elementToCopy, $elementToModify)
	{
		$pageArray = $this -> pageHandler -> getPageForId($elementToCopy);
		
		foreach($pageArray as $pageNumber)
		{
			$this -> pageHandler -> setPageForId($pageNumber, $elementToModify);
		}
		
		// FIXME array_values should not be needed there is a problem elsewhere
		$childrenToCopy = array_values($this -> xsdCompleteTree -> getChildren($elementToCopy));
		$childrenToModify = array_values($this -> xsdCompleteTree -> getChildren($elementToModify));
		
		foreach($childrenToModify as $childId => $childToModify)
		{
			$childToCopy = $childrenToCopy[$childId];
			$this -> copyPageArray($childToCopy, $childToModify);
		}
		
	}

	/**
	 *
	 */
	public function assignIdToPage($elementId, $pageNumber)
	{
		/* Not yet implemented */
		// TODO Implement and use it
	}

	/**
	 *
	 */
	public function assignIdToModule($elementId, $moduleName)
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::assignIdToModule');
		$this -> moduleHandler -> setIdWithModule($elementId, $moduleName);
	}

	public function setDataForId($dataValue, $elementId)
	{
		if ($this -> xsdCompleteTree -> getElement($elementId) != null)
		{
			$this -> dataArray[$elementId] = $dataValue;
			$this -> LOGGER -> log_debug('Value '.$dataValue.' has been inserted for id '.$elementId, 'XsdManager::setDataForId');
		}
		else $this -> LOGGER -> log_info('Id '.$elementId.' not found', 'XsdManager::setDataForId');
	}
	
	public function clearData()
	{
		$this -> dataArray = array();
		$this -> LOGGER -> log_debug('Data cleared', 'XsdManager::clearData');
	}

	public function getDataForId($elementId)
	{
		if(isset($this -> dataArray[$elementId]))
		{
			$this -> LOGGER -> log_debug('Id '.$elementId.' has data '.$this -> dataArray[$elementId], 'XsdManager::getDataForId');
			return $this -> dataArray[$elementId];
		}
		else 
		{
			// We check if there is a module attached to this id
			if(($moduleName = $this -> moduleHandler -> getModuleForId($elementId))!='')
			{
				$dataArray = retrieveModuleDataForId($moduleName, $elementId);
				
				if($dataArray == null)
				{
					$this -> LOGGER -> log_error('Function returned NULL for ID '.$elementId, 'XsdManager::getDataForId');
					return null;
				}
				
				$elementId = 0; // FIXME Condition not good
				if(isset($dataArray[$elementId])) 
				{
					$this -> LOGGER -> log_debug('Data found for ID '.$elementId, 'XsdManager::getDataForId');
					return $dataArray[$elementId];
				}
				else {
					$this -> LOGGER -> log_error('Data not inserted for ID '.$elementId, 'XsdManager::getDataForId');
					return null;
				}
			}
			else 
			{
				$this -> LOGGER -> log_debug('No data for id '.$elementId, 'XsdManager::getDataForId');
				return null;
			}
			
		}
	}

	/**
	 * Getter for the XSD file name
	 */
	public function getSchemaFileName()
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::getSchemaFileName');
		return $this -> getSchemaFileName();
	}
	
	public function getNamespaces()
	{
		return $this -> namespaces;
	}

	/**
	 *
	 */
	public function getXsdOriginalTree()
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::getxsdOriginalTree');
		return $this -> xsdOriginalTree;
	}

	/**
	 *
	 */
	public function setXsdOriginalTree($newOriginalTree)
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::setXsdOriginalTree');
		$this -> xsdOriginalTree = $newOriginalTree;
	}

	/**
	 *
	 */
	/*public function getXsdOrganizedTree()
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::getXsdOrganizedTree');
		return $this -> xsdOrganizedTree;
	}*/

	/**
	 *
	 */
	/*public function setXsdOrganizedTree($newXsdOrganizedTree)
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::setXsdOrganizedTree');
		$this -> xsdOrganizedTree = $newXsdOrganizedTree;
	}*/

	/**
	 *
	 */
	public function getXsdCompleteTree()
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::getXsdCompleteTree');
		return $this -> xsdCompleteTree;
	}

	/**
	 *
	 */
	public function setXsdCompleteTree($newXsdCompleteTree)
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::setXsdCompleteTree');
		$this -> xsdCompleteTree = $newXsdCompleteTree;
	}
	
	/**
	 *
	 */
	public function getXsdQueryTree()
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::getXsdQueryTree');
		return $this -> xsdQueryTree;
	}
	
	/**
	 *
	 */
	public function setXsdQueryTree($newXsdQueryTree)
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::setXsdQueryTree');
		$this -> xsdQueryTree = $newXsdQueryTree;
	}
	
	/**
	 * 
	 */
	public function getSearchHandler()
	{
		return $this -> searchHandler;
	}
	
	/**
	 * 
	 * @param $newSearchHandler
	 */
	public function setSearchHandler($newSearchHandler)
	{
		$this -> searchHandler = $newSearchHandler;
	}

	/**
	 *
	 */
	public function getPageHandler()
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::getPageHandler');
		return $this -> pageHandler;
	}

	/**
	 *
	 */
	public function setPageHandler($newPageHandler)
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::setPageHandler');
		$this -> pageHandler = $newPageHandler;
	}

	/**
	 *
	 */
	public function getModuleHandler()
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::getPageHandler');
		return $this -> moduleHandler;
	}

	/**
	 *
	 */
	public function setModuleHandler($newModuleHandler)
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::setModuleHandler');
		$this -> moduleHandler = $newModuleHandler;
	}

	/**
	 *
	 */
	public function getPageForId($elementId)
	{
		/* Not yet implemented */
	}

	/**
	 *
	 */
	public function getModuleForId($elementId)
	{
		/* Not yet implemented */
	}

	/**
	 *
	 */
	public function __toString()
	{
		// TODO Implement it
		return 'Parser string';
	}

}
?>