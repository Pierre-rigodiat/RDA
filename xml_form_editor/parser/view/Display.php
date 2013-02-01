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
	private $xsdManager; // A XsdManagerObject
	
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
			case 1 :
				// new Display(xsdManagerObject)
				if (is_object($argv[0]) && get_class($argv[0]) == 'XsdManager')
				{
					$this -> xsdManager = $argv[0];
					/*$this -> pageHandler = $argv[1];
					$this -> moduleHandler = $argv[2];*/
					
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

		try
		{
			$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);
		}
		catch (Exception $ex)
		{
			echo '<b>Impossible to build the Logger:</b><br/>' . $ex -> getMessage();
			return;
		}

		if ($this -> xsdManager == null /*&& $this -> pageHandler == null && $this -> moduleHandler == null*/)
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
			$this -> LOGGER -> log_debug('Display successfully built', 'Display::__construct');
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
		
		//$moduleList = $this -> moduleHandler -> getModuleList();
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
		
		$pageChooser = 'Split into <input type="number" min="1" value="'.$totalPage.'" class="text" id="page_number"/> page(s)';
		$this->LOGGER->log_debug('Page display returns a total of '.$totalPage.' page(s)', 'Display::displayPageChooser');
		
		return $pageChooser;
	}

	/**
	 * 
	 */
	public function displayPageNavigator()
	{		
		$pageChooser = '<div class="paginator">';
		
		$pageHandler = $this -> xsdManager -> getPageHandler();
		
		$totalPage = $pageHandler -> getNumberOfPage();
		
		if($totalPage > 1)
		{
			$currentPage = $pageHandler -> getCurrentPage();
			
			$pageChooser .= '<span class="ctx_menu"><span class="icon begin"></span></span><span class="ctx_menu"><span class="icon previous"></span></span>';
			
			for($i=0; $i<$totalPage; $i++)
			{
				$pageChooser .= '<span class="ctx_menu '.($currentPage==$i+1?'selected':'button').'">'.($i+1).'</span>';
			}
			
			$pageChooser .= '<span class="ctx_menu"><span class="icon next"></span></span><span class="ctx_menu"><span class="icon end"></span></span>';
		}
		
		$pageChooser .= '</div>';
		
		return $pageChooser;
	}
	 
	/**
	 *
	 */
	public function displayConfiguration()
	{
		$result = '';

		$result .= $this -> displayPopUp();
		$result .= '<div>';
		$result .= $this -> displayElement(0, self::$STEPS['config']);
		$result .= '</div>';

		return $result;
	}
	
	/**
	 * 
	 * 
	 * The PageHandler will know which element you have to Display
	 * The Tree will allow you to know if it is a module
	 * The ModuleHandler will know which page to display
	 */
	public function displayHTMLForm($elementId = 0, $partial = false)
	{
		$result = '';

		if (!$partial)
			$result .= '<div id="page_content">';
		$result .= $this -> displayElement($elementId, self::$STEPS['html_form']);
		if (!$partial)
			$result .= '</div>';

		return $result;
	}

	/**
	 *
	 */
	public function displayXMLTree()
	{
		/* Not yet implemented */
		// TODO Implement it
	}
	 
	/**
	 * Displays the jQueryUI pop-up for the configuration view
	 * @return {String} The pop-up code
	 */
	private function displayPopUp()
	{
		$popUp = '	<div id="dialog" title="">
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
		$pageHandler = $this -> xsdManager -> getPageHandler();
		$totalPage = $pageHandler->getNumberOfPage();
		
		$popUp .= '    <div class="dialog subpart" id="module-part">';
		
		if($totalPage > 1)
		{
			$popUp .= '<label for="page">In page</label>
					        <select id="page" name="page" class="ui-widget-content ui-corner-all">';
		
			for($i=1; $i<=$totalPage; $i++) $popUp .= '<option value="'.$i.'">'.$i.'</option>';
						        	
			$popUp .= '    </select>';
		}
					        
		$popUp .= '        <label for="module">As</label>							
					        <select id="module" name="module" class="ui-widget-content ui-corner-all">
					        	<option value="false">No module</option>';
					
		$moduleHandler = $this -> xsdManager -> getModuleHandler();
		$moduleList = $moduleHandler -> getModuleList('enable');
		foreach($moduleList as $module)
		{
			$popUp .= '			<option value="'.$module['name'].'">'.ucfirst($module['name']).'</option>';
		}
						
		$popUp .= '        </select>
				        </div>';
		
		$popUp .= '	</fieldset>
					    </form>
				    </div>';

		return $popUp;
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
				$children = $this -> xsdManager -> getXsdOrganizedTree() -> getChildren($elementId);
				break;
			case self::$STEPS['html_form'] :
				$result .= $this -> displayHTMLFormElement($elementId);
				$children = $this -> xsdManager -> getXsdCompleteTree() -> getChildren($elementId);
				break;
			default : // Unknown step ID
				$this -> LOGGER -> log_error('Step ID '.$stepId.' is unknown', 'Display::displayElement');
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
		$originalTreeId = $this -> xsdManager -> getXsdOrganizedTree() -> getObject($elementId);
		$element = $this -> xsdManager -> getXsdOriginalTree() -> getObject($originalTreeId);
		$elementAttr = $element -> getAttributes();
		$result = '';
		
		$this->LOGGER->log_debug('Display ID '.$elementId.'; Object: '.$element, 'Display::displayConfigurationElement');
		
		// The root element is displayed without being analyzed
		if($elementId == 0/*$this -> xsdManager -> getXsdOrganizedTree() -> getParent($elementId) == -1*/)
		{
			$result = '<h5>'.ucfirst($elementAttr['NAME']).'</h5>';
			return $result;
		}

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
		
		$pageHandler = $this->xsdManager->getPageHandler();
		if($pageHandler->getNumberOfPage() > 1)
		{
			$pages = $pageHandler -> getPageForId($elementId);
			if(count($pages)==0) $pageNumber = 1;
			else 
			{
				$pageNumber = '';
				foreach($pages as $page)
				{
					$pageNumber .= $page;
					if(end($pages)!=$page) $pageNumber .= ', '; 
				}	
			}
			
			$attrString .= ' | PAGE: '.$pageNumber;
		}

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
		$originalTreeId = $this -> xsdManager -> getXsdCompleteTree() -> getObject($elementId);
		
		// Check if the page contains the current element
		$pageHandler = $this -> xsdManager -> getPageHandler();
		$currentPage = $pageHandler -> getCurrentPage();
		$pages = $pageHandler -> getPageForId($elementId);
		if(count($pages)==0) $pages = array(1);
		
		if(!in_array($currentPage, $pages))
		{
			$this -> LOGGER -> log_debug('ID '.$elementId.' is not in the current page ('.$currentPage.')', 'Display::displayHTMLFormElement');
			return;
		}
		
		$element = $this -> xsdManager -> getXsdOriginalTree() -> getObject($originalTreeId);
		$elementAttr = $element -> getAttributes();
		$result = '';
		
		$this->LOGGER->log_debug('Display ID '.$elementId.'; Object: '.$element, 'Display::displayHTMLFormElement');

		// The root element is displayed without being analyzed
		if($elementId == 0/*$this -> xsdManager -> getXsdOrganizedTree() -> getParent($elementId) == -1*/)
		{
			$result = '<h5>'.ucfirst($elementAttr['NAME']).'</h5>';
			return $result;
		}

		$liClass = '';
		if (isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE'])
			$liClass = ' class="unavailable" ';

		$result .= '<li id="' . $elementId . '"' . $liClass . '><span class="elementName">' . $elementAttr['NAME'] . '</span> ';

		// todo study attributes

		if (isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], 'xsd')) // todo put xsd into a variable (could use the manager)
		{
			$result .= '<input type="text" class="text"/>';
			$this->LOGGER->log_debug('ID '.$elementId.' can be edited', 'Display::displayHTMLFormElement');
		}

		if (isset($elementAttr['RESTRICTION']))
		{
			$result .= '<select>';
			foreach ($elementAttr['RESTRICTION'] as $chooseElement)
				$result .= '<option value="' . $chooseElement . '">' . $chooseElement . '</value>';
			$result .= '</select>';
			$this->LOGGER->log_debug('ID '.$elementId.' is a restriction', 'Display::displayHTMLFormElement');
		}

		// Gather sibling information and create useful variable to count them
		$parentId = $this -> xsdManager -> getXsdCompleteTree() -> getParent($elementId);
		$siblingsIdArray = $this -> xsdManager -> getXsdCompleteTree() -> getId(/*$element*/$originalTreeId);
		
		$this->LOGGER->log_debug('ID '.$elementId.' has '.count($siblingsIdArray).' possible sibling(s)', 'Display::displayHTMLFormElement');
		/*$parentId = $this -> xsdManager -> getXsdOriginalTree() -> getParent($originalTreeId);
		$siblingsIdArray = $this -> xsdManager -> getXsdOriginalTree() -> getId($originalTreeId);*/
		$siblingsCount = 0;

		// Check the current number of siblings (to know if we need to display buttons)
		foreach ($siblingsIdArray as $siblingId)
		{
			$siblingParentId = $this -> xsdManager -> getXsdCompleteTree() -> getParent($siblingId);
			//$siblingParentId = $this -> xsdManager -> getXsdOriginalTree() -> getParent($originalTreeId);

			//$siblingObject = $this -> xsdManager -> getXsdCompleteTree() -> getObject($siblingId);
			$siblingOriginalTreeId = $this -> xsdManager -> getXsdCompleteTree() -> getObject($siblingId);
			$siblingObject = $this -> xsdManager -> getXsdOriginalTree() -> getObject($siblingOriginalTreeId);
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

		if (isset($elementAttr['MAXOCCURS'])) // Set up the icons if there is a maxOccurs defined
		{
			$this->LOGGER->log_debug('ID '.$elementId.' maxOccurs = '.$elementAttr['MAXOCCURS'].'', 'Display::displayHTMLFormElement');
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
