<?php
// XXX Avoid infinite includes in lib
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/helpers/Logger.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/Tree.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/ModuleHandler.php';

require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/lib/XmlParserFunctions.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/lib/StringFunctions.php';

/**
 * An XSD Parser able to generate several element:
 *  - an XML form to fill in
 * 	- an XML file
 * TODO Clean the array from unused data (parent, SEQUENCE, COMPLEXTYPE, SCHEMA...)
 * TODO Handle several namespaces
 * TODO For getter and setter, verify the type of parameters
 *
 *
 *
 *
 */
class XsdManager
{
	private $xsdFile;

	// The tree as it is in the xsd file
	private $xsdOriginalTree; 
	// The tree reorganized as it should be shown in the configuration view
	private $xsdOrganizedTree;
	// The tree as it should be in the form (with proper occurence)
	private $xsdCompleteTree;
	
	// The array containing the values entered by the user
	private $dataArray;

	// Handlers
	private $pageHandler;
	private $moduleHandler;

	private $rootElements;
	private $namespaces;

	private static $XSD_NS = 'http://www.w3.org/2001/XMLSchema';
	private static $NS_DEFINE_PREFIX = 'XMLNS';
	
	/**
	 * Logging information
	 */
	private $LOGGER;
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	private static $LOG_FILE;
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

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 3 :
				// new XsdManager(fileName, pageHandler, moduleHandler)
				if (is_string($argv[0]) && is_object($argv[1]) && get_class($argv[1]) == 'PageHandler' && is_object($argv[2]) && get_class($argv[2]) == 'ModuleHandler')
				{
					$this -> xsdFile = $argv[0];

					$this -> xsdOriginalTree = new Tree();
					$this -> xsdOrganizedTree = new Tree();
					$this -> xsdCompleteTree = new Tree();
					$this -> dataArray = array();

					$this -> pageHandler = $argv[1];
					$this -> moduleHandler = $argv[2];
				}
				else
				{
					$this -> xsdFile = null;
				}

				$level = self::$LEVELS['NO_DBG'];

				break;
			case 4 :
				// new XsdManager(fileName, pageHandler, moduleHandler, booleanDebug)
				if (is_string($argv[0]) && is_object($argv[1]) && get_class($argv[1]) == 'PageHandler' && is_object($argv[2]) && get_class($argv[2]) == 'ModuleHandler' && is_bool($argv[3]))
				{
					$this -> xsdFile = $argv[0];

					$this -> pageHandler = $argv[1];
					$this -> moduleHandler = $argv[2];

					if ($argv[1])
					{
						$this -> xsdOriginalTree = new Tree(true);
						$this -> xsdOrganizedTree = new Tree(true);
						$this -> xsdCompleteTree = new Tree(true);
						$this -> dataArray = array();
						$level = self::$LEVELS['DBG'];
					}
					else
					{
						$this -> xsdOriginalTree = new Tree();
						$this -> xsdOrganizedTree = new Tree();
						$this -> xsdCompleteTree = new Tree();
						$this -> dataArray = array();
						$level = self::$LEVELS['NO_DBG'];
					}
				}
				else
				{
					$this -> xsdFile = null;
					$level = self::$LEVELS['NO_DBG'];
				}

				break;
			default :
				$this -> xsdFile = null;
				$level = self::$LEVELS['NO_DBG'];
				break;
		}

		try
		{
			$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);
		}
		catch (Exception $ex)
		{
			echo '<b>Impossible to build the Logger:</b><br/>' . $ex -> getMessage();
		}

		if ($this -> xsdFile == null)
		{
			$log_mess = '';

			switch($argc)
			{
				case 3 :
					if (is_object($argv[0]))
						$argv0 = get_class($argv[0]);
					else
						$argv0 = gettype($argv[0]);
					if (is_object($argv[1]))
						$argv1 = get_class($argv[1]);
					else
						$argv1 = gettype($argv[1]);
					if (is_object($argv[2]))
						$argv2 = get_class($argv[2]);
					else
						$argv2 = gettype($argv[2]);

					$log_mess .= 'Function accepts {string, PageHandler, ModuleHandler} ({' . $argv[0] . ', ' . $argv[1] . ', ' . $argv[2] . '} given)';
					break;
				case 4 :
					if (is_object($argv[0]))
						$argv0 = get_class($argv[0]);
					else
						$argv0 = gettype($argv[0]);
					if (is_object($argv[1]))
						$argv1 = get_class($argv[1]);
					else
						$argv1 = gettype($argv[1]);
					if (is_object($argv[2]))
						$argv2 = get_class($argv[2]);
					else
						$argv2 = gettype($argv[2]);
					if (is_object($argv[3]))
						$argv2 = get_class($argv[3]);
					else
						$argv2 = gettype($argv[3]);

					$log_mess .= 'Function accepts {string, PageHandler, ModuleHandler, boolean} ({' . $argv[0] . ', ' . $argv[1] . ', ' . $argv[2] . ', ' . $argv[3] . '} given)';
					break;
				default :
					$log_mess .= 'Incorrect number of args (3 or 4 needed, ' . $argc . ' given)';
					break;
			}

			$this -> LOGGER -> log_error($log_mess, 'XsdManager::__construct');
		}
		else
		{
			$this -> LOGGER -> log_debug('Manager created for file ' . $this -> xsdFile, 'XsdManager::__construct');
		}
	}

	/**
	 * Parse the schema as a regular XML document
	 * Store the tree into $this->xsdOriginalTree
	 *
	 */
	private function parse()
	{
		global $elementTree;

		// Initialize the XML parser
		$parser = xml_parser_create();

		// Set handlers (see /lib/XmlParserFunctions)
		xml_set_element_handler($parser, "start", "stop");
		xml_set_character_data_handler($parser, "char");

		$fp = fopen($this -> xsdFile, "r");

		// Read data
		while ($data = fread($fp, 4096))
		{
			xml_parse($parser, $data, feof($fp)) or die(sprintf("XML Error: %s at line %d", xml_error_string(xml_get_error_code($parser)), xml_get_current_line_number($parser)));
		}

		//Free the XML parser and close the file
		xml_parser_free($parser);
		fclose($fp);

		$this -> xsdOriginalTree = $elementTree;
		$this -> LOGGER -> log_debug($this -> xsdFile . ' has been parsed', 'XsdManager::parse');
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
		$schemaElement = $this -> xsdOriginalTree -> getObject(0);
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

		// Find the root element
		$this -> rootElements = array();
		foreach ($this->xsdOriginalTree->getChildren(0) as $child)
		{
			$childObject = $this -> xsdOriginalTree -> getObject($child);
			if ($childObject -> getType() == $this -> namespaces['default']['name'] . ':ELEMENT')
			{
				array_push($this -> rootElements, $child);
			}
		}

		// Returning the rootElement
		if (count($this -> rootElements) > 1)
		{
			$this -> LOGGER -> log_info('Several root element found ' . serialize($this -> rootElements), 'XsdManager::buildTree');
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
	 *
	 */
	public function buildOrganizedTree($rootElement)
	{
		$this -> LOGGER -> log_debug('Building $xsdOrganizedTree with root ' . $rootElement, 'XsdManager::buildOrganizedTree');

		if (in_array($rootElement, $this -> rootElements))
		{
			$this -> insertTreeElement($rootElement);
			$this -> optimizeTree();
		}
		else
		{
			$this -> LOGGER -> log_error('ID ' . $rootElement . ' is not one of the possible root element', 'XsdManager::buildOrganizedTree');
		}
	}

	/**
	 *
	 */
	// Computes minOccurs
	public function buildCompleteTree($elementId = 0)
	{
		if (!$this -> xsdCompleteTree -> hasElement())
			$this -> xsdCompleteTree = clone $this -> xsdOrganizedTree;

		$originalTreeId = $this -> xsdCompleteTree -> getObject($elementId);
		$elementObject = $this -> xsdOriginalTree -> getObject($originalTreeId);
		$elementAttr = $elementObject -> getAttributes();

		$elementChildren = $this -> xsdCompleteTree -> getChildren($elementId);

		foreach ($elementChildren as $childId)
		{
			$this -> buildCompleteTree($childId);
		}

		if (isset($elementAttr['MINOCCURS']) && $elementAttr['MINOCCURS'] > 1)
		{
			for ($i = 0; $i < $elementAttr['MINOCCURS'] - 1; $i++)
			{
				$this -> xsdCompleteTree -> copyTreeBranch($elementId);
			}
		}
	}

	/**
	 * NB: Recursive function
	 */
	private function insertTreeElement($elementId, $parentId = -1)
	{
		//$elementObject = clone $this->xsdOriginalTree->getObject($elementId);
		//$newParentId = $this->xsdOrganizedTree->insertElement($elementObject, $parentId);
		$newParentId = $this -> xsdOrganizedTree -> insertElement($elementId, $parentId);

		if ($newParentId < 0)
		{
			$this -> LOGGER -> log_error('Error ' . $newParentId . ' occured when inserting ID ' . $elementId . ' (parent ID ' . $parentId . ')', 'XsdManager::insertTreeElement');
			return;
		}
		else
		{
			$children = $this -> xsdOriginalTree -> getChildren($elementId);
			if (count($children) > 0)
			{
				foreach ($children as $child)
				{
					$this -> insertTreeElement($child, $newParentId);
				}
			}
			else
			{
				$elementObject = /*clone */$this -> xsdOriginalTree -> getObject($elementId);
				$elementAttributes = $elementObject -> getAttributes();
				$attributesNames = array_keys($elementAttributes);
				if (in_array("TYPE", $attributesNames))
				{
					$key_part = explode(':', $elementAttributes['TYPE']);
					
					$isNamespaceDeclared = false;
					foreach($this -> namespaces as $nsDefinition)
					{
						if($nsDefinition['name'] == strtoupper($key_part[0]))
						{
							$isNamespaceDeclared = true;
							break;
						}
					}

					if (!$isNamespaceDeclared) // FIXME Document this part
					{
						$comparisonElement = new XsdElement($this -> namespaces['default']['name'] . ':COMPLEXTYPE', array("NAME" => $elementAttributes["TYPE"]));
						$arrayID = $this -> xsdOriginalTree -> getId($comparisonElement);

						if (count($arrayID) == 1)
						{
							$this -> insertTreeElement($arrayID[0], $newParentId);
						}
						else
						{
							$this -> LOGGER -> log_error('The comparison found unusual number (!=1) of element like ' . $comparisonElement, 'XsdManager::insertTreeElement');
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
		$tree = $this -> xsdOrganizedTree -> getTree();

		foreach ($tree as $id => $element)
		{
			/*$this -> LOGGER -> log_debug(serialize($tree), 'XsdManager::optimizeTree');
			 $this -> LOGGER -> log_debug(serialize($this->xsdOrganizedTree->getTree()), 'XsdManager::optimizeTree');	*/

			$originalTreeId = $element['object'];
			$this -> LOGGER -> log_debug('Optimizing tree for ID ' . $id . ' (orig ID ' . $originalTreeId . ')', 'XsdManager::optimizeTree');

			if (in_array($id, array_keys($this -> xsdOrganizedTree -> getTree())))
			{
				$object = $this -> xsdOriginalTree -> getObject($originalTreeId);
				$this -> LOGGER -> log_debug('OriginalID ' . $originalTreeId . ' has object ' . $object, 'XsdManager::optimizeTree');

				if ($object -> getType() == $this -> namespaces['default']['name'] . ':COMPLEXTYPE' || $object -> getType() == $this -> namespaces['default']['name'] . ':SEQUENCE' || $object -> getType() == $this -> namespaces['default']['name'] . ':SIMPLETYPE')
				{
					$this -> xsdOrganizedTree -> removeElement($id);
					//$this->xsdOriginalTree->removeElement($originalTreeId);

					$this -> LOGGER -> log_debug('ID ' . $id . ' (orig) removed (unused type)', 'XsdManager::optimizeTree');
				}

				//XXX Does not work for all the restriction
				if ($object -> getType() == $this -> namespaces['default']['name'] . ':RESTRICTION')
				{
					/*$parentId = $this->xsdOrganizedTree->getParent($id);
					 $children = $this->xsdOrganizedTree->getChildren($id);*/

					//$parentId = $this->xsdOriginalTree->getParent($originalTreeId);
					$children = $this -> xsdOriginalTree -> getChildren($originalTreeId);

					$values = array();
					foreach ($children as $child)
					{
						$attributes = $this -> xsdOriginalTree -> getObject($child) -> getAttributes();
						array_push($values, $attributes['VALUE']);
					}

					$parentId = $this -> xsdOrganizedTree -> getParent($id);
					$originalParentId = $this -> xsdOrganizedTree -> getObject($parentId);

					$this -> xsdOriginalTree -> getObject($originalParentId) -> addAttributes(array('RESTRICTION' => $values));

					//$this->xsdOriginalTree->getObject($parentId)->addAttributes(array('RESTRICTION'=>$values));
					$this -> LOGGER -> log_debug('ID ' . $parentId . ' (orig) contains restriction values ' . $this -> xsdOriginalTree -> getObject($parentId), 'XsdManager::optimizeTree');

					//$this->xsdOriginalTree->removeElement($originalTreeId, true);
					//$this -> LOGGER -> log_debug('ID '.$originalTreeId.' (orig) removed (restriction)', 'XsdManager::optimizeTree');

					$this -> xsdOrganizedTree -> removeElement($id, true);
					$this -> LOGGER -> log_debug('ID ' . $id . ' (orga) removed (restriction)', 'XsdManager::optimizeTree');

				}
			}
			else
				$this -> LOGGER -> log_debug('ID ' . $id . ' not found', 'XsdManager::optimizeTree');

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
		if (in_array($elementId, array_keys($this -> xsdCompleteTree -> getTree())))
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
					$this -> LOGGER -> log_error('Function returned NULL data array ', 'TableModule::getDataForId');
					return null;
				}
				
				$elementId = 0; // FIXME Condition not good
				if(isset($dataArray[$elementId])) 
				{
					$this -> LOGGER -> log_debug('Data found for ID '.$elementId, 'TableModule::getDataForId');
					return $dataArray[$elementId];
				}
				else {
					$this -> LOGGER -> log_error('Data not inserted for ID '.$elementId, 'TableModule::getDataForId');
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
	public function getXsdOrganizedTree()
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::getXsdOrganizedTree');
		return $this -> xsdOrganizedTree;
	}

	/**
	 *
	 */
	public function setXsdOrganizedTree($newXsdOrganizedTree)
	{
		$this -> LOGGER -> log_notice('Function called', 'XsdManager::setXsdOrganizedTree');
		$this -> xsdOrganizedTree = $newXsdOrganizedTree;
	}

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