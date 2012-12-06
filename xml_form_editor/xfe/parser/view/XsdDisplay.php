<?php
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/lib/StringFunctions.php';

/**
 * XsdDisplay class allow to display element the way you want.
 * todo build the class
 * xxx Handle templates, etc...
 * 
 */
class XsdDisplay { 		
	private $originalTree;
	private $userTree;
	
	private $LOGGER;
	
	private static $LEVELS = array('DBG'=>'notice', 'NO_DBG'=>'info');
	private static $LOG_FILE;
	private static $FILE_NAME = 'XsdDisplay.php';
	private static $STEPS = array('config'=>0, 'html_form'=>1, 'xml_tree'=>2);
	
	/**
	 * 
	 */
	public function __construct()
	{
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'].'/logs/display.log';
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc)
		{
			case 1: // new XsdDisplay(treeObject)
				if(is_object($argv[0]) && get_class($argv[0])=='Tree')
				{
					$this->originalTree = $argv[0];
					$this->userTree = $argv[0];
					$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this->originalTree = null;
					$this->userTree = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			case 2: // new XsdDisplay(treeObject, debugBoolean)
				if(is_object($argv[0]) && get_class($argv[0])=='Tree' && is_bool($argv[1]))
				{
					$this->originalTree = $argv[0];
					$this->userTree = $argv[0];
					
					if($argv[1]) $level = self::$LEVELS['DBG'];
					else $level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this->originalTree = null;
					$this->userTree = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default:
				$this->originalTree = null;
				$this->userTree = null;
				$level = self::$LEVELS['NO_DBG'];
				break;
		}
		
		try
		{
			$this->LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME); // xxx what if the $_SESSION doesn't exist
		}
		catch (Exception $ex)
		{
			echo '<b>Impossible to build the Logger:</b><br/>'.$ex->getMessage();
			return;
		}
		
		if($this->originalTree==null && $this->userTree == null)
		{
			$log_mess = '';
			
			switch($argc)
			{
				case 1: 
					$log_mess .= 'Supports Tree (object) as parameter ('.gettype($argv[0]).' given)';
					break;
				case 2: 
					$log_mess .= 'Supports {Tree(object), boolean} as parameters ({'.gettype($argv[0]).','.gettype($argv[1]).'} given)';
					break;
				default:
					$log_mess .= '1 or 2 parameters must be entered ('.$argc.'given)';
					break;
			}
			
			$this->LOGGER->log_error($log_mess, 'XsdDisplay::__construct');
		}
		else $this->LOGGER->log_debug('Display element successfully built', 'XsdDisplay::__construct');
	}
	
	/**
	 * 
	 */
	public function displayConfiguration()
	{
		$result = '';
		
		$result .= '<ul>';
		$result .= $this->displayElement(0, self::$STEPS['config']);
		$result .= '</ul>';
		
		return $result;
	}
	
	/**
	 * 
	 */
	public function displayHTMLForm($elementId = 0, $partial = false)
	{
		$result = '';
		
		if(!$partial) $result .= '<ul>';
		$result .= $this->displayElement($elementId, self::$STEPS['html_form']);
		if(!$partial) $result .= '</ul>';
		
		return $result;
	}
	
	public function displayXMLTree()
	{
		/* Not yet implemented */
	}
	
	private function displayElement($elementId, $stepId)
	{		
		$result = '';
		
		switch($stepId)
		{
			case self::$STEPS['config']:
				$result .= $this->displayConfigurationElement($elementId);
				break;
			case self::$STEPS['html_form']:
				$result .= $this->displayHTMLFormElement($elementId);
				break;
			default:
				//XXX provide a log error message
				exit;
				break;
		}
		
		$children = $this->originalTree->getChildren($elementId);
		
		if(count($children) > 0)
		{
			$result .= '<ul>';
			foreach($children as $child)
			{
				$result .= $this->displayElement($child, $stepId);
			}
			$result .= '</ul>';
		}
		
		// todo change it to be more modular
		/*if($stepId==self::$STEPS['config'])*/ $result .= '</li>';
		//else if($stepId==self::$STEPS['html_form']) $result .= '</div></li>';
		
		return $result;
	}

	/**
	 * 
	 */
	private function displayConfigurationElement($elementId)
	{
		$element = $this->originalTree->getObject($elementId);
		$elementAttr = $element->getAttributes();
		$result = '';
		
		// TODO check that the element contains at least what we want...
		// TODO check the type of element
		
		
		// Function to filter attribute we do not want to display
		if(!defined("filter_attribute")) // Avoid to redefine the function (i.e. avoid the error)
		{
			define("filter_attribute", true);
			
			function filter_attribute($var)
			{
				$attr_not_disp = array('NAME', 'TYPE'); // TYPE is first removed but if needed it will be pushed into the array			
				return !in_array($var, $attr_not_disp);
			}
		}

		$elementAttrName = array_filter(array_keys($elementAttr), "filter_attribute");		

		$result .= '<li>'.$elementAttr['NAME'].' ';
		
		// Displays all attributes we want to display
		$hasAttribute = false;
		foreach($elementAttrName as $attrName)
		{
			$hasAttribute = true;
			
			$result .=  $attrName.': ';
			// Display arrays nicely (as "item1, item2...")
			if(is_array($elementAttr[$attrName])) 
			{
				foreach($elementAttr[$attrName] as $attrElement)
				{
					$result .=  $attrElement;
					
					if(end($elementAttr[$attrName])!=$attrElement) $result .=  ', ';
				}
			}
			else $result .=  $elementAttr[$attrName];
			
			if(end($elementAttrName)!=$attrName) $result .=  ' | ';
		}
		
		if(isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], 'xsd')) // todo put xsd into a variable
		{
				$type = explode(':', $elementAttr['TYPE']);
				if($hasAttribute) $result .=  ' | ';
				$result .= 'TYPE: '.$type[1];
		}
		
		$result .=  '<span class="icon edit"></span>';
		
		return $result;		
	}
	
	/**
	 * 
	 */
	private function displayHTMLFormElement($elementId)
	{
		$element = $this->originalTree->getObject($elementId);
		$elementAttr = $element->getAttributes();
		$result = '';
		
		$liClass = '';
		if(isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE']) $liClass = ' class="unavailable" ';
		
		$result .= '<li id="'.$elementId.'"'.$liClass.'><span class="elementName">'.$elementAttr['NAME'].'</span> ';
		
		// todo study attributes
		
		if(isset($elementAttr['TYPE']) && startsWith($elementAttr['TYPE'], 'xsd')) // todo put xsd into a variable
		{
			$result .= '<input type="text" />';
		}
		
		if(isset($elementAttr['RESTRICTION']))
		{
			$result .= '<select>';
			foreach($elementAttr['RESTRICTION'] as $chooseElement) $result .= '<option value="'.$chooseElement.'">'.$chooseElement.'</value>';
			$result .= '</select>';
		}
		
		// Gather sibling information and create useful variable to count them
		$parentId = $this->originalTree->getParent($elementId);
		$siblingsIdArray = $this->originalTree->getId($element);				
		$siblingsCount = 0;
		
		//$removeButtonSet = false;
		
		// Check the current number of siblings (to know if we need to display buttons)
		foreach($siblingsIdArray as $siblingId)
		{
			$siblingParentId = $this->originalTree->getParent($siblingId);
			
			$siblingObject = $this->originalTree->getObject($siblingId);
			$siblingAttr = $siblingObject->getAttributes();
			
			// We compare the parent ID to know if this is a real sibling (and not just another similar element)
			// We also compare if the element is availabel
			if($parentId == $siblingParentId && !(isset($siblingAttr['AVAILABLE']) && !$siblingAttr['AVAILABLE'])) 
				$siblingsCount = $siblingsCount + 1;
		}
		
		$minOccurs = 1;
		if(isset($elementAttr['MINOCCURS'])) $minOccurs = $elementAttr['MINOCCURS'];
		
		
		if(isset($elementAttr['MAXOCCURS'])) // Set up the icons if there is a maxOccurs defined
		{
			if($elementAttr['MAXOCCURS']=='unbounded' || $siblingsCount<$elementAttr['MAXOCCURS']) $result .= '<span class="icon add"></span>';
		}
		
		/*if(($minOccurs>0 && $siblingsCount>$minOccurs) || 
			($minOccurs==0 && $siblingsCount>=1 && !(isset($elementAttr['AVAILABLE']) && !$elementAttr['AVAILABLE'])))*/
		if($siblingsCount>$minOccurs)
		{
			$result .= '<span class="icon remove"></span>';
		}
		
		
		return $result;
	}
	
	private function displayXMLElement($elementId, $elementAttr)
	{
		
	}
}
?>
	