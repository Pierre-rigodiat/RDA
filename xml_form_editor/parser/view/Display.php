<?php
/**
 * <Display class>
 */
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/lib/StringFunctions.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/moduleLoader.php'; // XXX try to remove this one
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/ModuleHandler.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/PageHandler.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/SearchHandler.php';
/**
 * Display class allow to display element the way you want.
 * 
 * @todo Handle templates
 * 
 * @author P. Dessauw <philippe.dessauw@nist.gov>, P. Savonitto <pierre.savonitto@nist.gov>
 * @copyright NIST 2013
 * 
 * @package XsdMan\View
 */
class Display
{
	/**
	 * A XsdManager object, model of the application.
	 * @var XsdManager
	 */
	private $xsdManager;
	
	/**
	 * The configuration file with all tags, icons and labels
	 * @var string
	 */
	private static $CONF_FILE;
	
	/**
	 * Configuration array
	 * @todo Populate the array
	 * @todo Move this to a file
	 * @var array
	 */
	private static $_CONF = array(
		"CONFIG" => array(
			"popup_start_tag" => '<div id="dialog" title="">',
			"popup_end_tag" => '</div>',
			"view_start_tag" => '<div>',
			"view_end_tag" => '</div>',
			"root_start_name_tag" => '<h5>',
			"root_end_name_tag" => '</h5>',
			"elem_start_name_tag" => '<span class="element_name">',
			"elem_end_name_tag" => '</span>',
			"attr_separator" => ' | ',
			"attr_start" => '<span class="attr">',
			"attr_end" => '</span>',
			"edit_icon" => '<span class="icon edit"></span>'
		),
		"FORM" => array(
			"popup_start_tag" => '<div id="dialog" title="Load form">',
			"popup_end_tag" => '</div>',
			"view_start_tag" => '<div id="page_content">',
			"view_end_tag" => '</div>',
			"root_start_name_tag" => '<h5>',
			"root_end_name_tag" => '</h5>',
			"elem_start_name_tag" => '<span class="element_name">',
			"elem_end_name_tag" => '</span>',
			"add_icon" => '<span class="icon add"></span>',
			"remove_icon" => '<span class="icon remove"></span>',
			"refresh_icon" => '<span class="icon refresh"></span>',
			"edit_icon" => '<a class="btn btn-mini edit" href="#"><i class="icon-edit"></i></a>'
		),
		"XML" => array(),
		"QUERY" => array(
		"view_start_tag" => '<div id="page_content">',
		"view_end_tag" => '</div>',
		"root_start_name_tag" => '<h5>',
		"root_end_name_tag" => '</h5>',
		"elem_start_name_tag" => '<span class="element_name">',
		"elem_end_name_tag" => '</span>',
		"add_icon" => '<span class="icon add"></span>',
		"remove_icon" => '<span class="icon remove"></span>',
		"empty_option_tag" => '<option value ="empty"></option>'
		)
	);
	
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
	 * Build an instance of Display.
	 * 
	 * <u>Parameters:</u>
	 * <ul>
	 * 		<li><var>XsdManager</var> <b>manager</b></li>
	 * </ul>
	 *
	 * <u>Sample code:</u>
	 * <code>
	 * $display = new Display($xsdManagerInstance);
	 * </code>
	 *
	 * @throws Exception Argument count or type of argument not good
	 */
	public function __construct()
	{
		// Initialize the logger (will throw an Exception if any problem occurs)
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['logs_dirname'].'/'.$_SESSION['xsd_parser']['conf']['log_file'];
		$level = self::$LEVELS['DBG'];
		$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);

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
					$this -> LOGGER -> log_error('First parameter is not an XsdManager', 'Display::__construct');
					throw new Exception('Invalid type of parameters given to the object');
				}
				break;
			default :
				$this -> LOGGER -> log_error('Wrong number of parameters', 'Display::__construct');
				throw new Exception('Invalid number of parameters given to the object');
				break;
		}

		$this -> LOGGER -> log_notice('Display set up', 'Display::__construct');
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
		
		$pageChooser = 'Split into <input type="number" min="1" value="'.$totalPage.'" class="text small"/> page(s) <div class="icon" id="page_number"></div>';
		$this->LOGGER->log_notice('Page chooser displayed w/ '.$totalPage.' page(s)', 'Display::displayPageChooser');
		
		return $pageChooser;
	}

	/**
	 * 
	 */
	public function displayPageNavigator()
	{		
		//$pageNavigator = '<div class="paginator">';
		$pageNavigator = '<ul>';
		
		$pageHandler = $this -> xsdManager -> getPageHandler();
		
		$totalPage = $pageHandler -> getNumberOfPage();
		
		if($totalPage > 1)
		{
			$currentPage = $pageHandler -> getCurrentPage();
			
			//$pageNavigator .= '<span class="ctx_menu"><span class="icon begin"></span></span><span class="ctx_menu"><span class="icon previous"></span></span>';
			$pageNavigator .= '<li'.($currentPage==1?' class="disabled"':'').'><a href="">Prev</a></li>';
			
			for($i=0; $i<$totalPage; $i++)
			{
				//$pageNavigator .= '<span class="ctx_menu '.($currentPage==$i+1?'selected':'button').'">'.($i+1).'</span>';
				$pageNavigator .= '<li'.($currentPage==$i+1?' class="active"':'').'><a href="">'.($i+1).'</a></li>';
			}
			
			//$pageNavigator .= '<span class="ctx_menu"><span class="icon next"></span></span><span class="ctx_menu"><span class="icon end"></span></span>';
			$pageNavigator .= '<li'.($currentPage==$totalPage?' class="disabled"':'').'><a href="">Next</a></li>';
		}
		
		//$pageNavigator .= '</div>';
		$pageNavigator .= '</ul>';
		
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
	 * @param int $elementId Element index
	 * @param boolean $fromCompleteTree Define the source tree to reach the element
	 * @return array Description of the element
	 */
	private function getElementDescription($elementId, $fromCompleteTree = false)
	{
		$elementDesc = array();
		
		/* Retrieve the XsdElement */
		if($fromCompleteTree)
		{
			$elementList = $this -> xsdManager -> getXsdCompleteTree() -> getElementList();
			$elementId = $elementList[$elementId];
		}
		
		$xsdElement = $this -> xsdManager -> getXsdOriginalTree() -> getElement($elementId);
		
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
	
	//TODO Merge with the getElementDescription
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
	 * @param int $elementId Element index
	 * @param boolean $fromQueryTree Define the source tree to reach the element
	 * @return array Description of the element
	 */
	private function getQueryElementDescription($elementId, $fromQueryTree = false)
	{
		$elementDesc = array();
	
		/* Retrieve the XsdElement */
		if($fromQueryTree)
		{
			$elementList = $this -> xsdManager -> getXsdQueryTree() -> getElementList();
			$elementId = $elementList[$elementId];
		}
	
		$xsdElement = $this -> xsdManager -> getXsdOriginalTree() -> getElement($elementId);
	
		$elementDesc['xsdElement'] = $xsdElement;
	
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
	 * 
	 * FIXME Change the function parameter into a boolean
	 */
	public function displayConfiguration($elementId = 0)
	{
		$configView = '';

		if($elementId == 0) // Display the whole tree
		{
			$configView .= self::$_CONF['CONFIG']['popup_start_tag'];		
			$configView .= $this -> displayConfigurationPopUp();
			$configView .= self::$_CONF['CONFIG']['popup_end_tag'];
			$configView .= self::$_CONF['CONFIG']['view_start_tag'];
			$configView .= $this -> displayConfigurationElement(0);
			$configView .= self::$_CONF['CONFIG']['view_end_tag'];
		}
		else // Display an element
		{
			$configView .= $this -> displayConfigurationElement($elementId, true);
		}
		
		return $configView;
	}
	
	/**
	 * Displays the jQueryUI pop-up for the configuration view
	 * 
	 * @return string The pop-up code
	 */
	private function displayConfigurationPopUp()
	{
		$popUp = '<p class="elementId"></p><p class="tip"></p>';
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
		$popUp .= '<label for="pattern">Pattern</label>';
		$popUp .= '<select id="pattern" name="pattern" class="ui-widget-content ui-corner-all">';
		$popUp .= '<option value="uid">Document UID</option>';
		//$popUp .= '<option value="oth">Other</option>';
		$popUp .= '</select>';
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
		
		$popUp .= '</fieldset></form>';

		return $popUp;
	}
	
	/**
	 * Display the configuration view of a single element.
	 * 
	 * @param int $elementId
	 * @param boolean $onlyElement
	 * @return string Configuration view of the element (HTML code)
	 */
	private function displayConfigurationElement($elementId, $onlyElement = false)
	{				
		/* Get element attributes */
		$elementDesc = $this -> getElementDescription($elementId);		
		$elementAttr = $elementDesc['xsdElement'] -> getAttributes();
		
		$this->LOGGER->log_notice('Display ID '.$elementId.'; Object: '.$elementDesc['xsdElement'], 'Display::displayConfigurationElement');
		
		$configElement = '';
		$children = array();
		
		// Display the start li tag for everyone but the root
		if (!$onlyElement && $elementId!=0) $configElement .= '<li id="' . $elementId . '">';
		
		// XXX See if this condition work for multi root schemas
		if($elementId == 0/*$this -> xsdManager -> getXsdOrganizedTree() -> getParent($elementId) == -1*/) // For root element, only the name is important
		{
			$configElement .= self::$_CONF['CONFIG']['root_start_name_tag'] . ucfirst($elementAttr['NAME']) . self::$_CONF['CONFIG']['root_end_name_tag'];
		}
		else {
			// Display element name and attributes
			$configElement .= self::$_CONF['CONFIG']["elem_start_name_tag"] . ucfirst($elementAttr['NAME']) . self::$_CONF['CONFIG']["elem_end_name_tag"];
			$configElement .= $this -> displayConfigurationAttributes($elementAttr, $elementDesc['pages'], $elementDesc['module']);	
		}

		// No module assigned implies to display children
		if($elementDesc['module'] == '') $children = $this -> xsdManager -> getXsdOriginalTree() -> getChildren($elementId);
		
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
	 * Display the list of interesting attributes.
	 * 
	 * @param array $elementAttr Array of element attributes
	 * @param array $pageArray Pages attached to the element
	 * @param string $moduleName Module attached to the element
	 * @return string Attributes HTML description
	 */
	private function displayConfigurationAttributes($elementAttr, $pageArray, $moduleName)
	{
		$attributeString = '';
		
		/* Filter attributes */
		/** @ignore */
		/*if (!defined("filter_attribute")) 
		{
			/**
			 * Avoid to redefine the function (i.e. avoid the error)
			 */
			/**
			 * @ignore
			 */
			/*define("filter_attribute", true);

			/** @ignore */
			/*function filter_attribute($var)
			{
				$attr_not_disp = array(
					'NAME',
					'TYPE'
				);
				
				return !in_array($var, $attr_not_disp);
			}
		}*/

		$elementAttrName = array_filter(array_keys($elementAttr), array($this, "filterAttribute"));
		
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
					else // $isChoiceElement == true
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
				$attributeString .= self::$_CONF['CONFIG']["attr_separator"];
		}

		$namespaces = $this -> xsdManager -> getNamespaces();		
		if (isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], strtolower($namespaces['default']['name'])))
		{
			$type = explode(':', $elementAttr['TYPE']);
			if ($hasAttribute)
				$attributeString .= self::$_CONF['CONFIG']["attr_separator"];
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
			
			if($attributeString != '') $attributeString .= self::$_CONF['CONFIG']["attr_separator"];
			$attributeString .= 'PAGE: '.$pageNumberString;
		}
		
		/* Display the module name */
		if($moduleName != '')
		{
			if($attributeString != '') $attributeString .= self::$_CONF['CONFIG']["attr_separator"];
			$attributeString .= 'MODULE: '.ucfirst($moduleName);
		}

		/* Add the style to the element list */
		if ($attributeString != '')
			$attributeString = self::$_CONF['CONFIG']["attr_start"] . $attributeString . self::$_CONF['CONFIG']["attr_end"];

		/* Add the edit button */
		$attributeString .= self::$_CONF['CONFIG']["edit_icon"];
		
		return $attributeString;
	}

	/**
	 * Avoid to display useless attributes
	 * @ignore
	 */
	private function filterAttribute($var)
	{
		$attr_not_disp = array(
			'AVAILABLE',
			'NAME',
			'TYPE'
		);
		
		return !in_array($var, $attr_not_disp);
	}
	
	/**
	 * The PageHandler will know which element you have to Display
	 * The Tree will allow you to know if it is a module
	 * The ModuleHandler will know which page to display
	 * 
	 * @param int $elementId Element index
	 * @param bool $partial Set to TRUE to just print one element an not the tree
	 * @return string HTML code of the view
	 */
	public function displayHTMLForm($elementId = 0, $partial = false)
	{
		$this -> LOGGER -> log_notice(($partial?'Partially d':'D').'isplaying form for ID '.$elementId.' ', 'Display::displayHTMLForm');
		
		$htmlForm = '';

		if (!$partial)
		{
			$htmlForm .= self::$_CONF['FORM']['popup_start_tag'];		
			$htmlForm .= $this -> displayHTMLFormPopUp();
			$htmlForm .= self::$_CONF['FORM']['popup_end_tag'];
			$htmlForm .= self::$_CONF['FORM']['view_start_tag'];
		}
		$htmlForm .= $this -> displayHTMLFormElement($elementId);
		if (!$partial)
			$htmlForm .= self::$_CONF['FORM']['view_end_tag'];

		return $htmlForm;
	}
	
	/**
	 * 
	 */
	private function displayHTMLFormPopUp()
	{
		$popUp = '<form><fieldset class="dialog fieldset">';
		
		$popUp .= '<div class="dialog subpart" id="form-part">';
		$popUp .= '<label for="form-id">Form </label>';
		$popUp .= '<select id="form-id" name="form-id" class="ui-widget-content ui-corner-all">';
		
		$formList = $this -> xsdManager -> retrieveForms();
		
		foreach ($formList as $formId) {
			$popUp .= '<option value="'.$formId["_id"].'">'.$formId["_id"].'</option>';
		}
		
		$popUp .= '</select>';
		$popUp .= '</div>';
		
		$popUp .= '</fieldset></form>';
		
		return $popUp;
	}
	
	/**
	 * 
	 * 
	 * @param int $elementId Element index
	 * @return string HTML code of the element
	 */
	private function displayHTMLFormElement($elementId)
	{
		$htmlFormElement = '';
		
		/* Get element info */
		$elementDesc = $this -> getElementDescription($elementId, true);
		$currentPage = $this -> xsdManager -> getPageHandler() -> getCurrentPage();
		
		$this->LOGGER->log_notice('Displaying ID '.$elementId.'; Object: '.$elementDesc['xsdElement'].'...', 'Display::displayHTMLFormElement');
		
		/* Check that the element should be display in this page */
		if($elementDesc['pages'] != null && !in_array($currentPage, $elementDesc['pages']))
		{
			$this -> LOGGER -> log_debug('ID '.$elementId.' is not in page '.$currentPage, 'Display::displayHTMLFormElement');
			return $htmlFormElement;
		}
		
		/* Displaying a module implies that children will not be displayed */
		if($elementDesc['module'] != '')
		{
			$this -> LOGGER -> log_debug('ID '.$elementId.' is not in page '.$currentPage, 'Display::displayHTMLFormElement');
			// TODO Find a better way to call the module view
			// XXX Use the XsdManager
			return displayModule($elementDesc['module']);
		}
		
		$elementAttr = $elementDesc['xsdElement'] -> getAttributes();
		
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
			$htmlFormElement .= self::$_CONF['FORM']['root_start_name_tag'] . ucfirst($elementAttr['NAME']) . self::$_CONF['FORM']['root_end_name_tag'];
		}
		else
		{
			$htmlFormElement .= self::$_CONF['FORM']['elem_start_name_tag'] . ucfirst($elementAttr['NAME']) . self::$_CONF['FORM']['elem_end_name_tag']. ' ';
			
			/* Auto-generation configuration */
			if(isset($elementAttr['AUTO_GENERATE']) && $elementAttr['AUTO_GENERATE']!='uid')
				$htmlFormElement .= self::$_CONF['FORM']['refresh_icon'];
			
			
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
					
					if(isset($elementAttr['AUTO_GENERATE']) && $elementAttr['AUTO_GENERATE']=='uid')
					{
						$htmlFormElement .= ' value="'.$this -> xsdManager -> getXsdManagerId().'" disabled="disabled"';
					}
					
				}
				
				$htmlFormElement .= '/>';
				
				if(isset($elementAttr['AUTO_GENERATE']) && $elementAttr['AUTO_GENERATE']=='uid')
				{
					$htmlFormElement .= ' '.self::$_CONF['FORM']['edit_icon'];
				}
				
				$this->LOGGER->log_notice('ID '.$elementId.' can be edited', 'Display::displayHTMLFormElement');
			}
			
			/* Display RESTRICTION element */
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
	
			/* CHOICE allow the user to choose which element they want to display using a <select> */
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
			// Gather sibling information and create useful variable to count them
			$siblingsIdArray = $this -> xsdManager -> getXsdCompleteTree() -> getSiblings($elementId);
			
			$this->LOGGER->log_notice('ID '.$elementId.' has '.count($siblingsIdArray).' possible sibling(s)', 'Display::displayHTMLFormElement');
			$siblingsCount = 0;
	
			// Check the current number of siblings (to know if we need to display buttons)
			foreach ($siblingsIdArray as $siblingId)
			{
				$siblingObject = $this -> xsdManager -> getXsdCompleteTree() -> getElement($siblingId);
				$siblingAttr = $siblingObject -> getAttributes();
	
				// We compare the parent ID to know if this is a real sibling (and not just another similar element)
				// We also compare if the element is available
				if (!(isset($siblingAttr['AVAILABLE']) && !$siblingAttr['AVAILABLE']))
					$siblingsCount = $siblingsCount + 1;
			}
			
			$this->LOGGER->log_debug('ID '.$elementId.' has '.$siblingsCount.' sibling(s)', 'Display::displayHTMLFormElement');
	
			$minOccurs = 1;
			if (isset($elementAttr['MINOCCURS']))
				$minOccurs = $elementAttr['MINOCCURS'];
			
			$this->LOGGER->log_notice('ID '.$elementId.' minOccurs = '.$minOccurs, 'Display::displayHTMLFormElement');

			$addIconDisplayed = false;

			/* Set up the add button for element with maxOccurs defined*/
			if (isset($elementAttr['MAXOCCURS']))
			{
				$this->LOGGER->log_notice('ID '.$elementId.' maxOccurs = '.$elementAttr['MAXOCCURS'], 'Display::displayHTMLFormElement');
				if ($elementAttr['MAXOCCURS'] == 'unbounded' || $siblingsCount < $elementAttr['MAXOCCURS'])
				{
					$htmlFormElement .= self::$_CONF['FORM']['add_icon'];
					$addIconDisplayed = true; // Avoid to have 2 add icon written for a same element
					$this->LOGGER->log_debug('ID '.$elementId.' has add button', 'Display::displayHTMLFormElement');
				}
			}
			
			/* Set up the add button for unavailable elements */
			if(isset($elementAttr['AVAILABLE']) && $elementAttr['AVAILABLE']==false) // Set up add icon if an element is disabled (minOccurs = 0 reached)
			{
				$this->LOGGER->log_notice('ID '.$elementId.' is unavailable', 'Display::displayHTMLFormElement');
				if(!$addIconDisplayed) // Avoid to have 2 add icon written for a same element
				{
					$htmlFormElement .= self::$_CONF['FORM']['add_icon'];
					$this->LOGGER->log_debug('ID '.$elementId.' has add button', 'Display::displayHTMLFormElement');
				}
			}
			
			/* Set up remove button for elements */
			if ($siblingsCount > $minOccurs)
			{
				$htmlFormElement .= self::$_CONF['FORM']['remove_icon'];
				$this->LOGGER->log_debug('ID '.$elementId.' has remove button', 'Display::displayHTMLFormElement');
			}
		}
		
		if($elementDesc['module'] == '')
		{
			$children = $this -> xsdManager -> getXsdCompleteTree() -> getChildren($elementId);
			
			// TODO "choose" should be a variable
			if($elementAttr['NAME'] == 'choose')
			{
				$completeElementList = $this -> xsdManager -> getXsdCompleteTree() -> getElementList();
										
				foreach ($children as $child) 
				{
					
					if($completeElementList[$child] == $elementAttr['CHOICE'][0])
					{
						$children = array($child);
						break;
					}
				}						
			}
		}
		
		/* Display children */
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
		
		return $htmlFormElement;
	}

	/**
	 *
	 * @return string The XML tree
	 */
	public function displayXMLTree()
	{
		return $this -> displayXmlElement(0);
	}

	/**
	 *
	 * @param int $elementId Element index
	 * @return string XML view of the element
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
			$children = $this -> xsdManager -> getXsdCompleteTree() -> getChildren($elementId);
				
			if($xmlElement=='') // Case of choice element
			{
				// Avoid the case where there is no data entered ($elementDisplay will be equal to '')
				if(isset($elementAttr['CHOICE']))
				{
					$xsdCompleteTreeElementList = $this -> xsdManager -> getXsdCompleteTree() -> getElementList();
					
					foreach ($children as $child)
					{
						$childOriginalId = $xsdCompleteTreeElementList[$child];
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
	
	/**
	 * 
	 */
	public function displayQuery() {
		$queryTree = self::$_CONF['QUERY']['view_start_tag'];
		$queryTree .= $this->displayQueryChild();
		$queryTree .= self::$_CONF['QUERY']['view_end_tag'];
		
		return $queryTree;
	}
	
	/**
	 * 
	 * @param integer $elementID
	 * @return string
	 */
	private function displayQueryFirstChild($elementID) {
		$manager = $this->xsdManager;
		$queryTree = $manager -> getXsdQueryTree();

		$xmlElement = '<ul>';	
		
		$xmlElement .= $this->displayQueryElement($elementID);
		
		return $xmlElement.'</ul>';
	}
	
	/**
	 * 
	 * @param integer $elementID
	 * @return string
	 */
	public function displayQueryChild($elementID = 0) {
		$manager = $this->xsdManager;
		$queryTree = $manager -> getXsdQueryTree();

		$recElement = $queryTree->getChildren($elementID);
		//var_dump($recElement);
		
		$xmlElement = '';
		
		if (!$elementID) {
			$mainElement = $queryTree->getElement($elementID)->getAttributes();
			$xmlElement .= self::$_CONF['QUERY']['root_start_name_tag'].ucfirst($mainElement['NAME']).self::$_CONF['QUERY']['root_end_name_tag'];
		}
		
		$xmlElement .= '<ul>';
		foreach ($recElement as $childID) {
			$xmlElement .= $this->displayQueryElement($childID);
		}
		
		return $xmlElement.'</ul>';
	}
	
	/**
	 * 
	 * @param $elementID
	 */
	private function displayQueryIcons($elementID) {
		$manager = $this->xsdManager;
		$queryTree = $manager -> getXsdQueryTree();
		$attr = $queryTree->getElement($elementID)->getAttributes();
		$xmlElement = '';
		/* Print the add / remove buttons */
		// Gather sibling information and create useful variable to count them
		$siblingsIdArray = $this -> xsdManager -> getXsdQueryTree() -> getSiblings($elementID);
			
		$this->LOGGER->log_notice('ID '.$elementID.' has '.count($siblingsIdArray).' possible sibling(s)', 'Display::displayQueryChild');
		$siblingsCount = 0;
		// Check the current number of siblings (to know if we need to display buttons)
		foreach ($siblingsIdArray as $siblingId)
		{
			$siblingObject = $this -> xsdManager -> getXsdQueryTree() -> getElement($siblingId);
			$siblingAttr = $siblingObject -> getAttributes();
			// We compare the parent ID to know if this is a real sibling (and not just another similar element)
			// We also compare if the element is available
			if (!(isset($siblingAttr['AVAILABLE']) && !$siblingAttr['AVAILABLE']))
				$siblingsCount = $siblingsCount + 1;
		}
			
		$this->LOGGER->log_debug('ID '.$elementID.' has '.$siblingsCount.' sibling(s)', 'Display::displayQueryChild');
		$minOccurs = 1;
		if (isset($attr['MINOCCURS']))
			$minOccurs = $attr['MINOCCURS'];
			
		$this->LOGGER->log_notice('ID '.$elementID.' minOccurs = '.$minOccurs, 'Display::displayQueryChild');
		$addIconDisplayed = false;
		// Set up the add button for element with maxOccurs defined
		if (isset($attr['MAXOCCURS']))
		{
			$this->LOGGER->log_notice('ID '.$elementID.' maxOccurs = '.$attr['MAXOCCURS'], 'Display::displayQueryChild');
			if ($attr['MAXOCCURS'] == 'unbounded' || $siblingsCount < $attr['MAXOCCURS'])
			{
				$xmlElement .= self::$_CONF['QUERY']['add_icon'];
				$addIconDisplayed = true; // Avoid to have 2 add icon written for a same element
				$this->LOGGER->log_debug('ID '.$elementID.' has add button', 'Display::displayQueryChild');
			}
		}
			
		// Set up the add button for unavailable elements
		if(isset($attr['AVAILABLE']) && $attr['AVAILABLE']==false) // Set up add icon if an element is disabled (minOccurs = 0 reached)
		{
			$this->LOGGER->log_notice('ID '.$elementID.' is unavailable', 'Display::displayQueryChild');
			if(!$addIconDisplayed) // Avoid to have 2 add icon written for a same element
			{
				$xmlElement .= self::$_CONF['QUERY']['add_icon'];
				$this->LOGGER->log_debug('ID '.$elementID.' has add button', 'Display::displayQueryChild');
			}
		}
			
		// Set up remove button for elements
		if ($siblingsCount > $minOccurs)
		{
			$xmlElement .= self::$_CONF['QUERY']['remove_icon'];
			$this->LOGGER->log_debug('ID '.$elementID.' has remove button', 'Display::displayQueryChild');
		}
		
		return $xmlElement;
	}
	
	
	/**
	 * 
	 * @param integer $elementID
	 * @return string
	 */
	public function displayQueryElement($elementID) {
		$manager = $this->xsdManager;
		$queryTree = $manager -> getXsdQueryTree();
		//var_dump($organizedTree);
		$displayedIdArray = $this->xsdManager->getSearchHandler()->getIdArray();

		$xmlElement = '';
	
		$elementChild = $queryTree->getElement($elementID);
		//var_dump($elementChild);
		
		$attr = $elementChild->getAttributes();
		$liClass = '';
		$disabled = '';
		if (isset($attr['AVAILABLE']) && !$attr['AVAILABLE']) {
			$liClass = ' class="unavailable" ';
			$disabled = ' disabled="disabled" ';
		}
		
		if (in_array($elementID, $displayedIdArray)) {
			
			$xmlElement .= '<li id="'.$elementID.'"'.$liClass.'>'.self::$_CONF['QUERY']['elem_start_name_tag'].ucfirst($attr['NAME']).self::$_CONF['QUERY']['elem_end_name_tag'];
			
			if (isset($attr['RESTRICTION']))
			{
				$xmlElement .= '<select class="xsdman restriction query_element"'.$disabled.'>';
				
				$xmlElement .= self::$_CONF['QUERY']['empty_option_tag'];
				foreach($attr['RESTRICTION'] as $restrictionElem) {
					$xmlElement .= '<option value ="'.$restrictionElem.'">'.$restrictionElem.'</option>';
				}
				$xmlElement .= '</select>';
			}
			else {
				$xmlElement .= '<input class="text query_element" type="text"'.$disabled.'>';
			}
		
			$xmlElement .= $this->displayQueryIcons($elementID).'</li>';
		}
		
		$children = $queryTree->getChildren($elementID);
		if ($children != array())
		{
			$xmlChild = $this->displayQueryChild($elementID);
			if ($xmlChild != '<ul></ul>')
			{
				if (isset($attr['CHOICE']))
				{
					$xmlElement .= '<li id="'.$elementID.'"'.$liClass.'>'.self::$_CONF['QUERY']['elem_start_name_tag'].'Choose'.self::$_CONF['QUERY']['elem_end_name_tag'].'<select class="xsdman choice">';
					foreach ($attr['CHOICE'] as $choiceID) {
						$choiceChild = $manager->getXsdOriginalTree()->getElement($choiceID);
						$choiceAttr = $choiceChild->getAttributes();
						$xmlElement .= '<option value="'.$choiceID.'">'.ucfirst($choiceAttr['NAME']).'</option>';
					}
					$xmlElement .= '</select>'.$this->displayQueryFirstChild($children[0]);
					$xmlElement .= $this->displayQueryIcons($elementID);
				}
				else {
					$xmlElement .= '<li id="'.$elementID.'"'.$liClass.'>'.self::$_CONF['QUERY']['elem_start_name_tag'].ucfirst($attr['NAME']).self::$_CONF['QUERY']['elem_end_name_tag'];
					$xmlElement .= $this->displayQueryIcons($elementID).$xmlChild;
				}
				
				$xmlElement .= '</li>';
			}
		}
	
		return $xmlElement;	
	}
	
	/**
	 *
	 *
	 * @param int $elementId Element index
	 * @return string HTML code of the element
	 */
	private function displayAdminQueryElement($elementId = 0)
	{
		$adminQueryElement = '';
	
		/* Get element info */
		$elementDesc = $this -> getQueryElementDescription($elementId, true);
		$displayedIdArray = $this->xsdManager->getSearchHandler()->getIdArray();
		
		$elementChecked = '';
		if (in_array($elementId, $displayedIdArray))
		{
			$elementChecked = 'checked="checked"';
		}
	
		$this->LOGGER->log_notice('Displaying ID '.$elementId.'; Object: '.$elementDesc['xsdElement'].'...', 'Display::displayAdminQueryElement');
	
		/* Displaying a module implies that children will not be displayed */
		if($elementDesc['module'] != '')
		{
			$this -> LOGGER -> log_debug('ID '.$elementId.' is not in page '.$currentPage, 'Display::displayAdminQueryElement');
			// TODO Find a better way to call the module view
			// XXX Use the XsdManager
			return displayModule($elementDesc['module']);
		}
	
		$elementAttr = $elementDesc['xsdElement'] -> getAttributes();
	
		/* Display the start li tag for non root element */
		if($elementId != 0 && $elementAttr['NAME'] != 'choose')
		{		
			$adminQueryElement .= '<li id="' . $elementId . '"' . '>';
		}
	
		if($elementId == 0/*$this -> xsdManager -> getXsdOrganizedTree() -> getParent($elementId) == -1*/)
		{
			$adminQueryElement .= self::$_CONF['FORM']['root_start_name_tag'] . ucfirst($elementAttr['NAME']) . self::$_CONF['FORM']['root_end_name_tag'];
		}
		elseif ($elementAttr['NAME'] != "choose")
		{
			$adminQueryElement .= self::$_CONF['FORM']['elem_start_name_tag'] . ucfirst($elementAttr['NAME']) . self::$_CONF['FORM']['elem_end_name_tag'];
				
			if (isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], 'xsd')) // todo put xsd into a variable (could use the manager)
			{
				$adminQueryElement .= '<input type="checkbox" class="checkbox" '.$elementChecked;
	
				if(($data = $this -> xsdManager -> getDataForId($elementId)) != null) // Element has data
				{
					$adminQueryElement .= ' value="'.$data.'"';
				}
	
				$adminQueryElement .= '/>';
	
				$this->LOGGER->log_notice('ID '.$elementId.' can be edited', 'Display::displayAdminQueryElement');
				
			}	
				
			/* Display RESTRICTION element */
			// TODO Implement other types of restriction
			if (isset($elementAttr['RESTRICTION']))
			{
				$data = $this->xsdManager->getDataForId($elementId);
					
				$adminQueryElement .= '<input type="checkbox" class="checkbox" '.$elementChecked;
				
				if(($data = $this -> xsdManager -> getDataForId($elementId)) != null) // Element has data
				{
					$adminQueryElement .= ' value="'.$data.'"';
				}
				
				$adminQueryElement .= '/>';
				
				$this->LOGGER->log_debug('ID '.$elementId.' is a restriction', 'Display::displayAdminQueryElement');
			}

		}
	
		/* Display children */
		$children = $this -> xsdManager -> getXsdQueryTree() -> getChildren($elementId);
		
		if (count($children) > 0)
		{
			if($elementAttr['NAME'] != 'choose')
			{
				$adminQueryElement .= '<ul>';
			}
			
			foreach ($children as $child)
			{
				$adminQueryElement .= $this -> displayAdminQueryElement($child);
			}
			
			if($elementAttr['NAME'] != 'choose')
			{
				$adminQueryElement .= '</ul>';
			}
		}
	
		if($elementId != 0 && $elementAttr['NAME'] != 'choose') $adminQueryElement .= '</li>';
	
		return $adminQueryElement;
	}
	
	/**
	 *
	 * @return String which contains the admin query tree
	 */
	public function displayAdminQueryTree()
	{
		$queryTree = self::$_CONF['QUERY']['view_start_tag'];
		$queryTree .= $this -> displayAdminQueryElement();
		$queryTree .= self::$_CONF['QUERY']['view_end_tag'];
		
		return $queryTree;
	}
	
}
?>
