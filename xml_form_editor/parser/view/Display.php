<?php
/**
 * <Display class>
 */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/lib/StringFunctions.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/moduleLoader.php'; // XXX try to remove this one
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/ModuleHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/PageHandler.php';
/**
 * Display class allow to display element the way you want.
 * xxx Handle templates, etc...
 * xxx what if the $_SESSION doesn't exist
 * 
 * 
 * @package XsdMan\View
 */
class Display
{
	private $xsdManager; // A XsdManager object
	
	private static $CONF_FILE; // The configuration file to handle the display elements 
	
	// Debug and logging variables
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
	private static $FILE_NAME = 'Display.php';

	/**
	 *
	 */
	public function __construct()
	{
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['logs_dirname'].'/'.$_SESSION['xsd_parser']['conf']['log_file'];

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 1 :
				// new Display(xsdManagerObject)
				if (is_object($argv[0]) && get_class($argv[0]) == 'XsdManager')
				{
					$this -> xsdManager = $argv[0];					
					$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> xsdManager = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			case 2 :
				// new Display(xsdManagerObject, debugBoolean)
				if (is_object($argv[0]) && get_class($argv[0]) == 'XsdManager' 
					&& is_bool($argv[1]))
				{
					$this -> xsdManager = $argv[0];

					if ($argv[1])
						$level = self::$LEVELS['DBG'];
					else
						$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> xsdManager = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default :
				$this -> xsdManager = null;
				$level = self::$LEVELS['NO_DBG'];
				break;
		}
		
		// Initialize the logger (will throw an Exception if any problem occurs)
		$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);

		if ($this -> xsdManager == null)
		{
			$log_mess = '';

			switch($argc)
			{
				case 1 :
					if(is_object($argv[0])) $argv0 = get_class($argv[0]);
					else $argv0 = gettype($argv[0]);
								
					$log_mess .= 'Function accepts {XsdManager} ({' . $argv0 . '} given)';
					break;
				case 2 :
					if(is_object($argv[0])) $argv0 = get_class($argv[0]);
					else $argv0 = gettype($argv[0]);
					if(is_object($argv[1])) $argv1 = get_class($argv[1]);
					else $argv1 = gettype($argv[1]);
					
					$log_mess .= 'Function accepts  {XsdManager, boolean} ({' . $argv0 . ', ' . $argv1 . '} given)';
					break;
				default :
					$log_mess .= 'Invalid number of args (1 or 2 needed, ' . $argc . 'given)';
					break;
			}

			$this -> LOGGER -> log_error($log_mess, 'Display::__construct');
		}
		else
			$this -> LOGGER -> log_notice('Display successfully built', 'Display::__construct');
	}
	
	/**
	 * 
	 */
	public function setXsdManager($newXsdManager)
	{
		if (is_object($newXsdManager) && get_class($newXsdManager) == 'XsdManager')
		{
			$this -> xsdManager = $newXsdManager;
			$this -> LOGGER -> log_debug('New XsdManager', 'Display::setXsdManager');
		}
		else
			$this -> LOGGER -> log_error('$newXsdManager is not a XsdManager', 'Display::setXsdManager');
	}
	
	/**
	 * 
	 */
	public function update()
	{
		$this -> LOGGER -> log_debug('Updating display...', 'Display::update');
		
		if(isset($_SESSION['xsd_parser']['parser']))
		{
			$sessionXsdManager = unserialize($_SESSION['xsd_parser']['parser']);
			$this -> setXsdManager($sessionXsdManager);
			
			$this -> LOGGER -> log_debug('Display updated', 'Display::update');
		}
		else $this -> LOGGER ->log_info('No XsdManager to update', 'Display::update');
		
		return;
	}
	
	/**
	 * 
	 */
	public function displayModuleChooser()
	{
		$moduleChooser = '';
		
		$moduleHandler = $this -> xsdManager -> getModuleHandler();
		$moduleList = $moduleHandler -> getModuleList();
		
		foreach($moduleList as $module)
		{
			$iconString = $moduleHandler->getModuleStatus($module['name'])==1?'on':'off';
			$moduleChooser .= '<div class="module"><span class="icon legend '.$iconString.'">'.ucfirst($module['name']).'</span></div>';
			
			$this->LOGGER->log_debug('Display module '.$module['name'], 'Display::displayModuleChooser');
		}
		
		return $moduleChooser;
	}
	
	/**
	 * 
	 */
	public function displayPageChooser()
	{
		$pageHandler = $this -> xsdManager -> getPageHandler();
		$totalPage = $pageHandler -> getNumberOfPage();
		
		$pageChooser = 'Split into <input type="number" min="1" value="'.$totalPage.'" class="text small"/> page(s) <div class="icon next" id="page_number"></div>';
		$this->LOGGER->log_notice('Page chooser displayed w/ '.$totalPage.' page(s)', 'Display::displayPageChooser');
		
		return $pageChooser;
	}

	/**
	 * 
	 */
	public function displayPageNavigator()
	{		
		$pageNavigator = '<div class="paginator">';
		
		$pageHandler = $this -> xsdManager -> getPageHandler();
		
		$totalPage = $pageHandler -> getNumberOfPage();
		
		if($totalPage > 1)
		{
			$currentPage = $pageHandler -> getCurrentPage();
			
			$pageNavigator .= '<span class="ctx_menu"><span class="icon begin"></span></span><span class="ctx_menu"><span class="icon previous"></span></span>';
			
			for($i=0; $i<$totalPage; $i++)
			{
				$pageNavigator .= '<span class="ctx_menu '.($currentPage==$i+1?'selected':'button').'">'.($i+1).'</span>';
			}
			
			$pageNavigator .= '<span class="ctx_menu"><span class="icon next"></span></span><span class="ctx_menu"><span class="icon end"></span></span>';
		}
		
		$pageNavigator .= '</div>';
		
		return $pageNavigator;
	}
	
	/**
	 * Return a basic description of the element
	 * 
	 * Return the following array
	 * array(
	 * 		"$element" => XsdElement
	 * 		"page" => pageArray
	 * 		"module" => moduleName
	 * 
	 * )
	 * 
	 * 
	 * @return array Description of the element
	 */
	private function getElementDescription($elementId, $fromCompleteTree = false)
	{
		$elementDesc = array();
		
		/* Retrieve the XsdElement */
		if($fromCompleteTree) $xsdElement = $this -> xsdManager -> getXsdCompleteTree() -> getElement($elementId);
		else $xsdElement = $this -> xsdManager -> getXsdOriginalTree() -> getElement($elementId);
		
		$elementDesc['xsdElement'] = $xsdElement;
		
		/* Retrieve the page number */
		$pageHandler = $this -> xsdManager -> getPageHandler();
		if($pageHandler -> getNumberOfPage() > 1)
		{
			$pages = $pageHandler -> getPageForId($elementId);
			if(count($pages) == 0)
				$pages = array(1);
		}
		else $pages = null;
		
		$elementDesc['pages'] = $pages;
		
		/* Retrieve the module name */
		$moduleHandler = $this -> xsdManager -> getModuleHandler();
		$moduleName = $moduleHandler -> getModuleForId($elementId);
		
		$elementDesc['module'] = $moduleName;
		
		return $elementDesc;
	}
	 
	/**
	 * Display the configuration view
	 * 
	 * @param int $elementId Id of the element
	 * @return string Configuration view (HTML code)
	 */
	public function displayConfiguration($elementId = 0)
	{
		$configView = '';

		if($elementId == 0) // Display the whole tree
		{
			// FIXME Change the parameter in the function
			//$rootElements = $this -> xsdManager -> getRootElements();
				
			
			$configView .= $this -> displayPopUp();
			$configView .= '<div>';
			$configView .= $this -> displayConfigurationElement(/*$rootElements[0]*/0);
			$configView .= '</div>';
		}
		else // Display an element
		{
			$configView .= $this -> displayConfigurationElement($elementId, true);
		}
		
		return $configView;
	}
	
	/**
	 * Displays the jQueryUI pop-up for the configuration view
	 * @return string The pop-up code
	 */
	private function displayPopUp()
	{
		$popUp = '<div id="dialog" title=""><p class="elementId"></p><p class="tip"></p>';
		$popUp .= '<form><fieldset class="dialog fieldset">';
		
		$popUp .= '<div class="dialog subpart" id="minoccurs-part">';
		$popUp .= '<label for="minoccurs">MinOccurs</label><input type="number" name="minoccurs" id="minoccurs" min="0" class="popup-text ui-widget-content ui-corner-all" />';
		$popUp .= '</div>';
		
		$popUp .= '<div class="dialog subpart" id="maxoccurs-part">';
		$popUp .= '<label for="maxoccurs">MaxOccurs</label><input type="number" name="maxoccurs" id="maxoccurs" min="0" class="popup-text ui-widget-content ui-corner-all" />';
		$popUp .= '<span class="dialog subitem"><label for="unbounded">Unbounded ?</label><input type="checkbox" id="unbounded" name="unbounded" /></span>';
		$popUp .= '</div>';
		
		$popUp .= '<div class="dialog subpart" id="datatype-part">';
		$popUp .= '<label for="datatype">Data-type</label>';
		$popUp .= '<select id="datatype" name="datatype" class="ui-widget-content ui-corner-all">';
		$popUp .= '<option value="string">String</option>';
		$popUp .= '<option value="integer">Integer</option>';
		$popUp .= '<option value="double">Double</option>';
		$popUp .= '</select>';
		$popUp .= '</div>';
		
		$popUp .= '<div class="dialog subpart" id="autogen-part">';
		$popUp .= '<label for="autogen">Auto-generate</label>';
		$popUp .= '<select id="autogen" name="autogen" class="ui-widget-content ui-corner-all">';
		$popUp .= '<option value="true">Enable</option><option value="false">Disable</option>';
		$popUp .= '</select>';
		$popUp .= '<span class="dialog subitem">';
		$popUp .= '<label for="pattern">Pattern</label><input type="text" name="pattern" id="pattern" value="Not yet implemented" class="popup-text ui-widget-content ui-corner-all" disabled="disabled"/>';
		$popUp .= '</span>';
		$popUp .= '</div>';

		$pageHandler = $this -> xsdManager -> getPageHandler();
		$totalPage = $pageHandler->getNumberOfPage();
				
		$popUp .= '<div class="dialog subpart" id="module-part">';
		
		/* Page chooser */
		if($totalPage > 1)
		{
			$popUp .= '<label for="page">In page</label>';
			$popUp .= '<select id="page" name="page" class="ui-widget-content ui-corner-all">';
		
			for($i=1; $i<=$totalPage; $i++) $popUp .= '<option value="'.$i.'">'.$i.'</option>';
						        	
			$popUp .= '</select>';
		}
		
		/* Module chooser */			        
		$popUp .= '<label for="module">As</label>';
		$popUp .= '<select id="module" name="module" class="ui-widget-content ui-corner-all">';
		$popUp .= '<option value="false">No module</option>';
					
		$moduleHandler = $this -> xsdManager -> getModuleHandler();
		$moduleList = $moduleHandler -> getModuleList('enable');
		foreach($moduleList as $module)
		{
			$popUp .= '<option value="'.$module['name'].'">'.ucfirst($module['name']).'</option>';
		}
			
		$popUp .= '</select>';
				        
		$popUp .= '</div>';
		
		$popUp .= '</fieldset></form></div>';

		return $popUp;
	}
	
	/**
	 * Display the configuration view of a single element.
	 * 
	 * @param int $elementId
	 * @param PageHandler $pageHandler
	 * @param ModuleHandler $moduleHandler
	 * @param boolean $onlyElement
	 * @return string Configuration view of the element (HTML code)
	 */
	private function displayConfigurationElement($elementId, $onlyElement = false)
	{
		/* Configuration element */
		// TODO Populate the array
		// TODO Move this to a file
		$ELEMENT_NAME_TAG = array(
			"root_start" => '<h5>',
			"root_end" => '</h5>',
			"elem_start" => '<span class="element_name">',
			"elem_end" => '</span>'
		);
		
		/* Get element attributes */
		$elementDesc = $this -> getElementDescription($elementId);		
		$elementAttr = $elementDesc['xsdElement'] -> getAttributes();
		
		$configElement = '';
		$children = array();
		
		$this->LOGGER->log_debug('Display ID '.$elementId.'; Object: '.$elementDesc['xsdElement'], 'Display::displayConfigurationElement');
		
		// Display the start li tag for everyone but the root
		if (!$onlyElement && $elementId!=0) $configElement .= '<li id="' . $elementId . '">';
		
		// FIXME See if this condition work for multi root schemas
		if($elementId == 0/*$this -> xsdManager -> getXsdOrganizedTree() -> getParent($elementId) == -1*/) // For root element, only the name is important
		{
			$configElement .= $ELEMENT_NAME_TAG["root_start"] . ucfirst($elementAttr['NAME']) . $ELEMENT_NAME_TAG["root_end"];
		}
		else {
			// Display element name and attributes
			$configElement .= $ELEMENT_NAME_TAG["elem_start"] . ucfirst($elementAttr['NAME']) . $ELEMENT_NAME_TAG["elem_end"];
			$configElement .= $this -> displayConfigurationAttributes($elementAttr, $elementDesc['pages'], $elementDesc['module']);	
		}

		// No module assigned implies to display children
		if($elementDesc['module'] == '') $children = $this -> xsdManager -> getXsdOriginalTree() -> getChildrenId($elementId);
		
		/* Display children (if it is not the only element to display) */
		if (count($children) > 0 && !$onlyElement)
		{
			$configElement .= '<ul>';
			foreach ($children as $child)
			{
				$configElement .= $this -> displayConfigurationElement($child);
			}
			$configElement .= '</ul>';
		}

		// Display the end li tag for everyone but the root
		if (!$onlyElement && $elementId!=0) $configElement .= '</li>';
		
		return $configElement;
	}

	/**
	 * 
	 */
	private function displayConfigurationAttributes($elementAttr, $pageArray, $moduleName)
	{
		$attributeString = '';
		
		// TODO check that the element contains at least what we want...
		// TODO check the type of element
		
		/* Filter attributes */
		if (!defined("filter_attribute")) // Avoid to redefine the function (i.e. avoid the error)
		{
			define("filter_attribute", true);

			function filter_attribute($var)
			{
				$attr_not_disp = array(
					'NAME',
					'TYPE'
				);
				
				return !in_array($var, $attr_not_disp);
			}
		}

		$elementAttrName = array_filter(array_keys($elementAttr), "filter_attribute");
		
		// Special display for choice element
		$isChoiceElement = false;
		if($elementAttr['NAME'] == 'choose') $isChoiceElement = true;

		// Displays all attributes
		$hasAttribute = false;
		foreach ($elementAttrName as $attrName)
		{
			$hasAttribute = true;

			$attributeString .= $attrName . ': ';
			
			if (is_array($elementAttr[$attrName]))
			{
				// Display arrays nicely (as "item1, item2...")
				foreach ($elementAttr[$attrName] as $attrElement)
				{
					if(!$isChoiceElement) $attributeString .= $attrElement;
					else
					{
						// FIXME doing that assumes that you just have one attribute in choices (or at least one array)
						$childXsdElement = $this -> xsdManager -> getXsdOriginalTree() -> getElement($attrElement);
						$childAttributes = $childXsdElement -> getAttributes();
						
						$attributeString .= ucfirst($childAttributes['NAME']);
					}

					if (end($elementAttr[$attrName]) != $attrElement)
						$attributeString .= ', ';
				}
			}
			else
				$attributeString .= $elementAttr[$attrName];

			if (end($elementAttrName) != $attrName)
				$attributeString .= ' | ';
		}

		// todo put xsd into a variable
		if (isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], 'xsd'))
		{
			$type = explode(':', $elementAttr['TYPE']);
			if ($hasAttribute)
				$attributeString .= ' | ';
			$attributeString .= 'TYPE: ' . $type[1];
		}
		
		/* Display the page number */
		if(count($pageArray)!=0)
		{
			$pageNumberString = '';
			foreach($pageArray as $page) // Go through the page array
			{
				$pageNumberString .= $page;
				if(end($pageArray)!=$page) $pageNumberString .= ', ';
			}
			
			if($attributeString != '') $attributeString .= ' | ';
			$attributeString .= 'PAGE: '.$pageNumberString;
		}
		
		/* Display the module name */
		if($moduleName != '')
		{
			if($attributeString != '') $attributeString .= ' | ';
			$attributeString .= 'MODULE: '.ucfirst($moduleName);
		}

		/* Add the style to the element list */
		if ($attributeString != '')
			$attributeString = '<span class="attr">' . $attributeString . '</span>';

		/* Add the edit button */
		$attributeString .= '<span class="icon edit"></span>';
		
		return $attributeString;
	}
	
	/**
	 * 
	 * The PageHandler will know which element you have to Display
	 * The Tree will allow you to know if it is a module
	 * The ModuleHandler will know which page to display
	 */
	public function displayHTMLForm($elementId = 0, $partial = false)
	{
		$result = '';
		
		// FIXME Change the parameter in the function
		//$rootElements = $this -> xsdManager -> getRootElements();

		if (!$partial)
			$result .= '<div id="page_content">';
		$result .= $this -> displayHTMLFormElement(/*$rootElements[0]*/$elementId);
		if (!$partial)
			$result .= '</div>';

		$this -> LOGGER -> log_debug('$result = '.$result, 'Display::displayHTMLForm');

		return $result;
	}
	
	/**
	 * 
	 */
	private function displayHTMLFormElement($elementId)
	{
		$htmlFormElement = '';
		
		$elementDesc = $this -> getElementDescription($elementId, true);
		$currentPage = $this -> xsdManager -> getPageHandler() -> getCurrentPage();
		
		/* Check that the element should be display in this page */
		if($elementDesc['pages'] == null || in_array($currentPage, $elementDesc['pages']))
		{
			/* Displaying a module implies that children will not be displayed */
			if($elementDesc['module'] != '')
			{				
				// TODO Find a better way to call the module view
				// XXX Use the XsdManager
				$htmlFormElement .= displayModule($elementDesc['module']);
			}
			else {
				$elementAttr = $elementDesc['xsdElement'] -> getAttributes(); // TODO Do something if the element doesn't exist
			
				$this->LOGGER->log_debug('Display ID '.$elementId.'; Object: '.$elementDesc['xsdElement'], 'Display::displayHTMLFormElement');
				
				/* Display the start li tag for non root element */ 
				if($elementId != 0)
				{
					$liClass = '';
					if (isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE'])
						$liClass = ' class="unavailable" ';
					
					$htmlFormElement .= '<li id="' . $elementId . '"' . $liClass . '>';
				}
				
				
				if($elementId == 0/*$this -> xsdManager -> getXsdOrganizedTree() -> getParent($elementId) == -1*/)
				{
					$htmlFormElement .= '<h5>'.ucfirst($elementAttr['NAME']).'</h5>';
				}
				else
				{
					$htmlFormElement .= '<span class="elementName">' . ucfirst($elementAttr['NAME']) . '</span> ';
					
					if (isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], 'xsd')) // todo put xsd into a variable (could use the manager)
					{			
						$htmlFormElement .= '<input type="text" class="text"';
						
						if(isset($elementAttr['AVAILABLE']) && $elementAttr['AVAILABLE']==false) // Element not available => No value + Input disabled
						{
							$htmlFormElement .= ' disabled="disabled"';
						}
						else // Element available
						{
							if(($data = $this -> xsdManager -> getDataForId($elementId)) != null) // Element has data
							{
								$htmlFormElement .= ' value="'.$data.'"';
							}
							
						}
						
						$htmlFormElement .= '/>';
						
						$this->LOGGER->log_debug('ID '.$elementId.' can be edited', 'Display::displayHTMLFormElement');
					}
					
					// RESTRICTION are select
					// TODO Implement other types of restriction
					if (isset($elementAttr['RESTRICTION']))
					{
						$data = $this->xsdManager->getDataForId($elementId);				
							
						$htmlFormElement .= '<select class="xsdman restriction">';			
						
						foreach ($elementAttr['RESTRICTION'] as $chooseElement)
							$htmlFormElement .= '<option value="' . $chooseElement . '" '.($data==$chooseElement?'selected="selected"':'').'>' . $chooseElement . '</value>';
						$htmlFormElement .= '</select>';
						$this->LOGGER->log_debug('ID '.$elementId.' is a restriction', 'Display::displayHTMLFormElement');
					}
			
					// CHOICE allow the user to choose which element they want to display using a <select>
					if (isset($elementAttr['CHOICE']))
					{
						$htmlFormElement .= '<select class="xsdman choice">';
						foreach ($elementAttr['CHOICE'] as $chooseElement)
						{
							$childXsdElement = $this -> xsdManager -> getXsdOriginalTree() -> getElement($chooseElement);
							$childAttributes = $childXsdElement -> getAttributes();
							
							$htmlFormElement .= '<option value="' . $chooseElement . '">' . ucfirst($childAttributes['NAME']) . '</value>';
						}
						$htmlFormElement .= '</select>';
						$this->LOGGER->log_debug('ID '.$elementId.' is a choice', 'Display::displayHTMLFormElement');
					}

					/* Print the add / remove buttons */
					// TODO Improve this part
					// XXX START XXX
					// Gather sibling information and create useful variable to count them
					$parentId = $this -> xsdManager -> getXsdCompleteTree() -> getParentId($elementId);
					$originalTreeId = $this -> xsdManager -> getXsdCompleteTree() -> getElement($elementId);
					$siblingsIdArray = $this -> xsdManager -> getXsdCompleteTree() -> getIds($originalTreeId);
					
					$this->LOGGER->log_debug('ID '.$elementId.' has '.count($siblingsIdArray).' possible sibling(s)', 'Display::displayHTMLFormElement');
					$siblingsCount = 0;
			
					// Check the current number of siblings (to know if we need to display buttons)
					foreach ($siblingsIdArray as $siblingId)
					{
						$siblingParentId = $this -> xsdManager -> getXsdCompleteTree() -> getParentId($siblingId);

						$siblingObject = $this -> xsdManager -> getXsdCompleteTree() -> getElement($siblingId);
						//$siblingObject = $this -> xsdManager -> getXsdOriginalTree() -> getObject($siblingOriginalTreeId);
						$siblingAttr = $siblingObject -> getAttributes();
			
						// We compare the parent ID to know if this is a real sibling (and not just another similar element)
						// We also compare if the element is availabel
						if ($parentId == $siblingParentId && !(isset($siblingAttr['AVAILABLE']) && !$siblingAttr['AVAILABLE']))
							$siblingsCount = $siblingsCount + 1;
					}
					
					$this->LOGGER->log_debug('ID '.$elementId.' has '.$siblingsCount.' sibling(s)', 'Display::displayHTMLFormElement');
			
					$minOccurs = 1;
					if (isset($elementAttr['MINOCCURS']))
						$minOccurs = $elementAttr['MINOCCURS'];
					
					$this->LOGGER->log_debug('ID '.$elementId.' minOccurs = '.$minOccurs.'', 'Display::displayHTMLFormElement');
			
					$addIconDisplayed = false;
			
					if (isset($elementAttr['MAXOCCURS'])) // Set up the icons if there is a maxOccurs defined
					{
						$this->LOGGER->log_debug('ID '.$elementId.' maxOccurs = '.$elementAttr['MAXOCCURS'].'', 'Display::displayHTMLFormElement');
						if ($elementAttr['MAXOCCURS'] == 'unbounded' || $siblingsCount < $elementAttr['MAXOCCURS'])
						{
							$htmlFormElement .= '<span class="icon add"></span>';
							$addIconDisplayed = true;
						}
					}
					
					if(isset($elementAttr['AVAILABLE']) && $elementAttr['AVAILABLE']==false) // Set up add icon if an element is disabled (minOccurs = 0 reached)
					{
						$this->LOGGER->log_debug('ID '.$elementId.' is unavailable', 'Display::displayHTMLFormElement');
						if(!$addIconDisplayed) 
							$htmlFormElement .= '<span class="icon add"></span>';
					}
					
					if ($siblingsCount > $minOccurs)
					{
						$htmlFormElement .= '<span class="icon remove"></span>';
					}
					
					// XXX END XXX
				}
				
				
				if($elementDesc['module'] == '')
				{
					$children = $this -> xsdManager -> getXsdCompleteTree() -> getChildrenId($elementId);
					
					// TODO choose should be a variable
					if($elementAttr['NAME'] == 'choose')
					{
						/*$choiceElement = $this -> xsdManager -> getXsdCompleteTree() -> getElement($elementId);	
						/*$originalTree = $this -> xsdManager -> getXsdOriginalTree();
						
						$choiceElement = $originalTree -> getObject($originalElementId);*/
						//$choiceElementAttributes = $choiceElement -> getAttributes();
						
						foreach ($children as $child) 
						{
							//$childOriginalId = $this -> xsdManager -> getXsdCompleteTree() -> getObject($child);
							if($child/*OriginalId*/ == /*$choiceElementAttributes*/$elementAttr['CHOICE'][0])
							{
								$children = array($child);
								break;
							}
						}						
					}
				}
				
						
				if (count($children) > 0)
				{
					$htmlFormElement .= '<ul>';
					foreach ($children as $child)
					{
						$htmlFormElement .= $this -> displayHTMLFormElement($child);
					}
					$htmlFormElement .= '</ul>';
				}
		
				if($elementId != 0) $htmlFormElement .= '</li>';
				
				
			}
		}
		else
		{
			$this -> LOGGER -> log_debug('ID '.$elementId.' is not in the current page ('.$currentPage.')', 'Display::displayHTMLFormElement');
		}
		
		return $htmlFormElement;
	}

	/**
	 *
	 * 
	 */
	public function displayXMLTree()
	{
		$result = $this -> displayXmlElement(0);
		return $result;
	}

	/**
	 * 
	 */
	private function displayXmlElement($elementId)
	{
		$xmlElement = '';
		$children = array();
		
		$elementDesc = $this -> getElementDescription($elementId, true);
		$elementAttr = $elementDesc['xsdElement'] -> getAttributes();		
		
		// Unavailable elements are not displayed
		if(isset($elementAttr['AVAILABLE']) && $elementAttr['AVAILABLE']==false)
		{
			return $xmlElement;
		}
		
		// Element CHOICE are not displayed (element created to be able to make the choice in the form)
		// Disabled element are not displayed
		if(!isset($elementAttr['CHOICE']))
		{
			$xmlElement .= '<'.$elementAttr['NAME'];
		
			if($elementId == 0) // If it is the root element
			{
				$nsArray = $this -> xsdManager -> getNamespaces();
				$this -> LOGGER -> log_notice('Including namespaces to element '.$elementAttr['NAME'].'...', 'Display::displayXMLElement');
				
				foreach ($nsArray as $nsName => $nsValue) {					
					if(!is_string($nsName) || $nsName!='default')
					{
						$this -> LOGGER -> log_debug($nsValue['name'].' will be included', 'Display::displayXMLElement');
						
						$xmlElement .= ' xmlns:'.strtolower($nsValue['name']).'="'.$nsValue['url'].'"';
					}
				}
	
				$this -> LOGGER -> log_notice('Namespaces included to element '.$elementAttr['NAME'], 'Display::displayXMLElement');
			}
			
			$xmlElement .= '>';
			
			if(($data = $this -> xsdManager -> getDataForId($elementId))!=null)
			{
				$xmlElement .= $data;
			}
		}
		
		// Case where no module is displayed
		// TODO Find a better way to store module data
		if($this -> xsdManager -> getModuleHandler() -> getModuleForId($elementId) == '')
		{
			$children = $this -> xsdManager -> getXsdCompleteTree() -> getChildrenId($elementId);
			
			if($xmlElement=='') // Case of choice element 
			{				
				// Avoid the case where there is no data entered ($elementDisplay will be equal to '')
				if(isset($elementAttr['CHOICE']))
				{
					foreach ($children as $child) 
					{
						$childOriginalId = $this -> xsdManager -> getXsdCompleteTree() -> getElement($child);
						if($childOriginalId == $elementAttr['CHOICE'][0])
						{
							$children = array($child);
							break;
						}
					}
				}
			}
		}
		
		/* Displaying children if possible */
		if (count($children) > 0)
		{
			foreach ($children as $child)
			{
				$xmlElement .= $this -> displayXmlElement($child);
			}
		}
		
		if(!isset($elementAttr['CHOICE'])) $xmlElement .= '</'.$elementAttr['NAME'].'>';
		
		return $xmlElement;
	}
}
?>
