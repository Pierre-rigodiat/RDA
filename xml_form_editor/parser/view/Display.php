<?php
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/ModuleHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/parser/core/PageHandler.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/lib/StringFunctions.php';
// xxx what if the $_SESSION doesn't exist

/**
 * Display class allow to display element the way you want.
 * xxx Handle templates, etc...
 *
 */
class Display
{
	private $parser;
	private $moduleHandler; // A ModuleHandler object
	private $pageHandler; // A PageHandler object
	
	private static $STEPS = array(
		'config' => 0,
		'html_form' => 1,
		'xml_tree' => 2
	);
	private static $CONF_FILE; // The configuration file to handle the display elements 
	
	// Debug and logging variables
	private $LOGGER;
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	private static $LOG_FILE;
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
			case 3 :
				// new Display(parserObject, pageHandler, moduleHandler)
				if (is_object($argv[0]) && get_class($argv[0]) == 'XsdParser' 
					&& is_object($argv[1]) && get_class($argv[1]) == 'PageHandler' 
					&& is_object($argv[2]) && get_class($argv[2]) == 'ModuleHandler')
				{
					$this -> parser = $argv[0];
					$this -> pageHandler = $argv[1];
					$this -> moduleHandler = $argv[2];
					
					$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> parser = null;
					$this -> pageHandler = null;
					$this -> moduleHandler = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			case 4 :
				// new Display(parserObject, pageHandler, moduleHandler, debugBoolean)
				if (is_object($argv[0]) && get_class($argv[0]) == 'XsdParser' 
					&& is_object($argv[1]) && get_class($argv[1]) == 'PageHandler' 
					&& is_object($argv[2]) && get_class($argv[2]) == 'ModuleHandler'
					&& is_bool($argv[3]))
				{
					$this -> parser = $argv[0];
					$this -> pageHandler = $argv[1];
					$this -> moduleHandler = $argv[2];

					if ($argv[2])
						$level = self::$LEVELS['DBG'];
					else
						$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> parser = null;
					$this -> pageHandler = null;
					$this -> moduleHandler = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default :
				$this -> parser = null;
				$this -> pageHandler = null;
				$this -> moduleHandler = null;
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
			return;
		}

		if ($this -> parser == null && $this -> pageHandler == null && $this -> moduleHandler == null)
		{
			$log_mess = '';

			switch($argc)
			{
				case 3 :
					if(is_object($argv[0])) $argv0 = get_class($argv[0]);
					else $argv0 = gettype($argv[0]);
					if(is_object($argv[1])) $argv1 = get_class($argv[1]);
					else $argv1 = gettype($argv[1]);
					if(is_object($argv[2])) $argv2 = get_class($argv[2]);
					else $argv2 = gettype($argv[2]);
								
					$log_mess .= 'Supports {XsdParser,PageHandler,ModuleHandler} as parameter ({' . $argv0 . ',' . $argv1 . ',' . $argv2 . '} given)';
					break;
				case 4 :
					if(is_object($argv[0])) $argv0 = get_class($argv[0]);
					else $argv0 = gettype($argv[0]);
					if(is_object($argv[1])) $argv1 = get_class($argv[1]);
					else $argv1 = gettype($argv[1]);
					if(is_object($argv[2])) $argv2 = get_class($argv[2]);
					else $argv2 = gettype($argv[2]);
					if(is_object($argv[3])) $argv3 = get_class($argv[3]);
					else $argv3 = gettype($argv[3]);
					
					$log_mess .= 'Supports {XsdParser,PageHandler,ModuleHandler,boolean} as parameters ({' . $argv0 . ',' . $argv1 . ',' . $argv2 . ',' . $argv3 . '} given)';
					break;
				default :
					$log_mess .= 'Supports 3 or 4 parameter at input (' . $argc . 'given)';
					break;
			}

			$this -> LOGGER -> log_error($log_mess, 'Display::__construct');
		}
		else
			$this -> LOGGER -> log_debug('Display successfully built', 'Display::__construct');
	}
	
	/**
	 * 
	 */
	public function setParser($newParser)
	{
		if (is_object($newParser) && get_class($newParser) == 'XsdParser')
		{
			$this -> parser = $newParser;
			$this -> LOGGER -> log_debug('New parser set', 'Display::setParser');
		}
		else
			$this -> LOGGER -> log_error('First parameter is not an instance of XsdParser', 'Display::setParser');
	}
	
	/**
	 * 
	 */
	public function setModuleHandler($newModuleHandler)
	{
		if (is_object($newModuleHandler) && get_class($newModuleHandler) == 'ModuleHandler')
		{
			$this -> moduleHandler = $newModuleHandler;
			$this -> LOGGER -> log_debug('New ModuleHandler set', 'Display::setModuleHandler');
		}
		else
			$this -> LOGGER -> log_error('First parameter is not an instance of ModuleHandler', 'Display::setModuleHandler');
	}
	
	/**
	 * 
	 */
	public function setPageHandler($newPageHandler)
	{
		/* Not yet implemented */
	}
	
	/**
	 * 
	 */
	public function update()
	{
		$this -> updateParser();
		$this -> updateModuleHandler();
		$this -> updatePageHandler();
		
		// TODO add some logger stuff
		
		return;
	}
	
	/**
	 * 
	 */
	public function updateParser()
	{		
		if(isset($_SESSION['xsd_parser']['parser']))
		{
			$sessionParser = unserialize($_SESSION['xsd_parser']['parser']);
			$this -> setParser($sessionParser);
			
			$this -> LOGGER ->log_debug('Parser updated', 'Display::updateParser');
		}
		else
		{
			$this -> LOGGER ->log_info('No parser to update', 'Display::updateParser');
		}
	}
	
	/**
	 * 
	 */
	public function updateModuleHandler()
	{
		if(isset($_SESSION['xsd_parser']['mhandler']))
		{
			$sessionModuleHandler = unserialize($_SESSION['xsd_parser']['mhandler']);
			$this -> setModuleHandler($sessionModuleHandler);
			
			$this -> LOGGER ->log_debug('ModuleHandler updated', 'Display::updateModuleHandler');
		}
		else
		{
			$this -> LOGGER ->log_info('No ModuleHandler to update', 'Display::updateModuleHandler');
		}
	}
	
	/**
	 * 
	 */
	public function updatePageHandler()
	{
		/* Not yet implemented */
		//$sessionPageHandler = $_SESSION['xsd_parser']['phandler'];
	}
	
	/**
	 * 
	 */
	public function displayModuleChooser()
	{
		$moduleChooser = '';
		
		$moduleList = $this -> moduleHandler -> getModuleList();
		foreach($moduleList as $module)
		{
			$iconString = $this->moduleHandler->getModuleStatus($module['name'])==1?'on':'off';
			$moduleChooser .= '<div class="module"><span class="icon legend '.$iconString.'">'.ucfirst($module['name']).'</span></div>';
			
			$this->LOGGER->log_debug('Display module '.$module['name'], 'Display::displayModuleChooser');
		}
		
		return $moduleChooser;
	}
	 
	/**
	 *
	 */
	public function displayConfiguration()
	{
		$result = '';

		$result .= $this -> displayPopUp();
		$result .= '<ul>';
		$result .= $this -> displayElement(0, self::$STEPS['config']);
		$result .= '</ul>';

		return $result;
	}
	
	/**
	 * 
	 * 
	 * The PageHandler will know which element you have to Display
	 * The Tree will allow you to know if it is a module
	 * The ModuleHandler will know which page to display
	 */
	public function displayHTMLFormPage($page = 1)
	{
		// XXX Way to follow
		// pageHandler -> getElementsIdForPage($page)
		// foreach element
		//		if element -> hasAttributes('MODULE') 
		//			loadModuleView
		//			displayModuleView
		//			display moduleHandler -> displayPageForId(moduleName, id)
		//		else this->displayElement(id)
		
		
		/*$result = '';

		if (!$partial)
			$result .= '<ul>';
		$result .= $this -> displayElement($elementId, self::$STEPS['html_form']);
		if (!$partial)
			$result .= '</ul>';*/

		return 'page '.$page;
	}

	/**
	 *
	 */
	public function displayHTMLForm($elementId = 0, $partial = false)
	{
		$result = '';

		if (!$partial)
			$result .= '<ul>';
		$result .= $this -> displayElement($elementId, self::$STEPS['html_form']);
		if (!$partial)
			$result .= '</ul>';

		return $result;
	}

	/**
	 *
	 */
	public function displayXMLTree()
	{
		/* Not yet implemented */
	}

	/**
	 * 
	 */
	private function displayPopUpModuleSelect()
	{
		$popUpSelection = '';
		
		$moduleList = $this -> moduleHandler -> getModuleList('enable');
		foreach($moduleList as $module)
		{
			$popUpSelection .= '<option value="'.$module['name'].'">'.ucfirst($module['name']).'</option>';
		}
		
		return $popUpSelection;
	}
	 
	/**
	 * Displays the jQueryUI pop-up for the configuration view
	 * @return {String} The pop-up code
	 */
	private function displayPopUp()
	{
		$result = '	<div id="dialog" title="">
						<p class="elementId"></p>
					    <p class="tip"></p>
						
					    <form>
					    <fieldset class="dialog fieldset">
					    	<div class="dialog subpart" id="minoccurs-part">
						        <label for="minoccurs">MinOccurs</label>
						        <input type="number" name="minoccurs" id="minoccurs" min="0" class="popup-text ui-widget-content ui-corner-all" />
					        </div>
					        <div class="dialog subpart" id="maxoccurs-part">
						        <label for="maxoccurs">MaxOccurs</label>
						        <input type="number" name="maxoccurs" id="maxoccurs" min="0" class="popup-text ui-widget-content ui-corner-all" />
						        <span class="dialog subitem">
						        	<label for="unbounded">Unbounded ?</label>
						        	<input type="checkbox" id="unbounded" name="unbounded" />
						        </span>
					        </div>
					        <div class="dialog subpart" id="datatype-part">
						        <label for="datatype">Data-type</label>
						        <select id="datatype" name="datatype" class="ui-widget-content ui-corner-all">
						        	<option value="string">String</option>
						        	<option value="integer">Integer</option>
						        	<option value="double">Double</option>
						        </select>
					        </div>
					        <div class="dialog subpart" id="autogen-part">
						        <label for="autogen">Auto-generate</label>
						        <select id="autogen" name="autogen" class="ui-widget-content ui-corner-all">
						        	<option value="true">Enable</option>
						        	<option value="false">Disable</option>
						        </select>
						        <span class="dialog subitem">
						        	<label for="pattern">Pattern</label>
						        	<input type="text" name="pattern" id="pattern" value="Not yet implemented" class="popup-text ui-widget-content ui-corner-all" disabled="disabled"/>
						        </span>
					        </div>';
		
		// Module select display
		if($this->pageHandler && $this->moduleHandler) // If the ModuleDisplay object has been set
		{
			$maxPages = $this->pageHandler->getNumberOfPage();
			
			
			$result .= '    <div class="dialog subpart" id="module-part">';
			
			if($maxPages > 1)
			{
				$result .= '<label for="page">In page</label>
						        <select id="page" name="page" class="ui-widget-content ui-corner-all">';
		
			
				for($i=1; $i<=$maxPages; $i++) $result .= '<option value="'.$i.'">'.$i.'</option>';
							        	
				$result .= '    </select>';
			}
						        
			$result .= '        <label for="module">As</label>							
						        <select id="module" name="module" class="ui-widget-content ui-corner-all">
						        	<option value="false">No module</option>';
						
			$result .= $this->displayPopUpModuleSelect();
							
			$result .= '        </select>
					        </div>';
		}
		
		$result .= '	</fieldset>
					    </form>
				    </div>';

		return $result;
	}

	/**
	 *
	 */
	private function displayElement($elementId, $stepId)
	{
		$result = '';
		$children = array();

		switch($stepId)
		{
			case self::$STEPS['config'] :
				$result .= $this -> displayConfigurationElement($elementId);
				$children = $this -> parser -> getXsdOrganizedTree() -> getChildren($elementId);
				break;
			case self::$STEPS['html_form'] :
				$result .= $this -> displayHTMLFormElement($elementId);
				$children = $this -> parser -> getXsdCompleteTree() -> getChildren($elementId);
				break;
			default :
				//XXX provide a log error message
				exit ;
				break;
		}

		if (count($children) > 0)
		{
			$result .= '<ul>';
			foreach ($children as $child)
			{
				$result .= $this -> displayElement($child, $stepId);
			}
			$result .= '</ul>';
		}

		$result .= '</li>';

		return $result;
	}

	/**
	 *
	 */
	public function displayConfigurationElement($elementId, $withoutList = false)
	{
		//$element = $this -> tree -> getObject($elementId);
		$element = $this -> parser -> getXsdOrganizedTree() -> getObject($elementId);
		$elementAttr = $element -> getAttributes();
		$result = '';
		
		$this->LOGGER->log_debug('Display ID '.$elementId.'; Object: '.$element, 'Display::displayConfigurationElement');

		// TODO check that the element contains at least what we want...
		// TODO check the type of element
		// Function to filter attribute we do not want to display
		if (!defined("filter_attribute"))// Avoid to redefine the function (i.e. avoid the error)
		{
			define("filter_attribute", true);

			function filter_attribute($var)
			{
				$attr_not_disp = array(
					'NAME',
					'TYPE'
				);
				// TYPE is first removed but if needed it will be pushed into the array
				return !in_array($var, $attr_not_disp);
			}

		}

		$elementAttrName = array_filter(array_keys($elementAttr), "filter_attribute");

		if (!$withoutList)
			$result .= '<li id="' . $elementId . '">';
		$result .= '<span class="element_name">' . ucfirst($elementAttr['NAME']) . '</span>';

		// Displays all attributes we want to display
		$hasAttribute = false;
		$attrString = '';
		foreach ($elementAttrName as $attrName)
		{
			$hasAttribute = true;

			$attrString .= $attrName . ': ';
			// Display arrays nicely (as "item1, item2...")
			if (is_array($elementAttr[$attrName]))
			{
				foreach ($elementAttr[$attrName] as $attrElement)
				{
					$attrString .= $attrElement;

					if (end($elementAttr[$attrName]) != $attrElement)
						$attrString .= ', ';
				}
			}
			else
				$attrString .= $elementAttr[$attrName];

			if (end($elementAttrName) != $attrName)
				$attrString .= ' | ';
		}

		if (isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], 'xsd'))// todo put xsd into a variable
		{
			$type = explode(':', $elementAttr['TYPE']);
			if ($hasAttribute)
				$attrString .= ' | ';
			$attrString .= 'TYPE: ' . $type[1];
		}
		
		/*if(isset($this->pageHandler) && $this->pageHandler->getNumberOfPage() > 1)
		{
			$attrString .= ' | PAGE: '.$this->pageHandler->getPageForId($elementId);
		}*/

		if ($attrString != '')
			$result .= '<span class="attr">' . $attrString . '</span>';

		// The root element is the only one which cannot be edited
		if($elementId!=0) $result .= '<span class="icon edit"></span>'; 

		return $result;
	}

	/**
	 *
	 */
	private function displayHTMLFormElement($elementId)
	{
		$element = $this -> parser -> getXsdCompleteTree() -> getObject($elementId);
		$elementAttr = $element -> getAttributes();
		$result = '';
		
		$this->LOGGER->log_debug('Display ID '.$elementId.'; Object: '.$element, 'Display::displayHTMLFormElement');

		$liClass = '';
		if (isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE'])
			$liClass = ' class="unavailable" ';

		$result .= '<li id="' . $elementId . '"' . $liClass . '><span class="elementName">' . $elementAttr['NAME'] . '</span> ';

		// todo study attributes

		if (isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], 'xsd'))// todo put xsd into a variable
		{
			$result .= '<input type="text" class="text"/>';
		}

		if (isset($elementAttr['RESTRICTION']))
		{
			$result .= '<select>';
			foreach ($elementAttr['RESTRICTION'] as $chooseElement)
				$result .= '<option value="' . $chooseElement . '">' . $chooseElement . '</value>';
			$result .= '</select>';
		}

		// Gather sibling information and create useful variable to count them
		$parentId = $this -> parser -> getXsdCompleteTree() -> getParent($elementId);
		$siblingsIdArray = $this -> parser -> getXsdCompleteTree() -> getId($element);
		$siblingsCount = 0;

		// Check the current number of siblings (to know if we need to display buttons)
		foreach ($siblingsIdArray as $siblingId)
		{
			$siblingParentId = $this -> parser -> getXsdCompleteTree() -> getParent($siblingId);

			$siblingObject = $this -> parser -> getXsdCompleteTree() -> getObject($siblingId);
			$siblingAttr = $siblingObject -> getAttributes();

			// We compare the parent ID to know if this is a real sibling (and not just another similar element)
			// We also compare if the element is availabel
			if ($parentId == $siblingParentId && !(isset($siblingAttr['AVAILABLE']) && !$siblingAttr['AVAILABLE']))
				$siblingsCount = $siblingsCount + 1;
		}

		$minOccurs = 1;
		if (isset($elementAttr['MINOCCURS']))
			$minOccurs = $elementAttr['MINOCCURS'];

		if (isset($elementAttr['MAXOCCURS']))// Set up the icons if there is a maxOccurs defined
		{
			if ($elementAttr['MAXOCCURS'] == 'unbounded' || $siblingsCount < $elementAttr['MAXOCCURS'])
				$result .= '<span class="icon add"></span>';
		}

		/*if(($minOccurs>0 && $siblingsCount>$minOccurs) ||
		 ($minOccurs==0 && $siblingsCount>=1 && !(isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE'])))*/
		if ($siblingsCount > $minOccurs)
		{
			$result .= '<span class="icon remove"></span>';
		}

		return $result;
	}

	/**
	 *
	 */
	private function displayXMLElement($elementId, $elementAttr)
	{

	}

}
?>
