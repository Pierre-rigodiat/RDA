<?php
/**
 * <XsdElement class>
 */
/**
 * <b>Class managing any schema tag parsed</b>
 * 
 * XsdElement object regroups tag name and attributes in the same structure. The code below explains how to use it
 * <code>
 * // Let's say we want to store the following schema element as an XsdElement
 * // &lt;xs:element name="root" type="Root"/&gt;
 * $xsdElement = new XsdElement(
 * 		'xs:element', 
 * 		array(
 * 			'name'=>'root',
 * 			'type'=>'Root'
 * 		)
 * );
 * 
 * // Then we want to add a new attribute
 * 
 * // Remove an attribute
 * 
 * // Compare to an attribute
 * 
 * // Display the
 * echo $xsdElement; // Will return xs:element{ name = root | type = Root }
 * 
 * </code>
 *  
 * @todo Change some function names (about attributes)
 * @todo Improve the debugging
 * 
 * @author P. Dessauw <philippe.dessauw@nist.gov>
 * @copyright NIST 2013
 * @example debug/UnitTest/XsdElementUnitTest.php Unit tests for an XsdElement
 * 
 * @package XsdMan\Core
 */
class XsdElement {	
	/** 
	 * Name of the element tag 
	 * @var string 
	 */
	private $elementType;
	
	/**
	 * Every attributes of the tag stored as $attributeName => $attributeValue
	 * @var array
	 */
	private $elementAttributes;
	
	/**
	 * Logging information
	 * TODO Improve the logging management
	 */
	/** @ignore */
	private $LOGGER;
	/** @ignore */
	private static $LEVELS = array('DBG'=>'notice', 'NO_DBG'=>'info');
	/** @ignore */
	private static $LOG_FILE;
	/** @ignore */
	private static $FILE_NAME = 'XsdElement.php';
	
	/**
	 * Build a new XsdElement
	 * 
	 * <u>Parameters:</u>
	 * <ul>
	 * 		<li><var>string</var> <b>tagName</b></li>
	 * 		<li><var>array</var> <b>tagAttributes</b></li>
	 * 		<li>[<var>boolean</var> <b>enableDebugging</b> = false]</li>
	 * </ul>
	 * 
	 * <u>Sample code:</u>
	 * <code>
	 * $xsdElement= new XsdElement('XSD:ELEMENT', array('attrName_1' => 'attrValue_1', ..., 'attrName_n' => 'attrValue_n'));
	 * </code>
	 * 
	 * @throws Exception Argument count not good or type of argument is not good
	 */
	public function __construct()
	{
		// Require the logger and configure the log file
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'].'/logs/xsd_element.log';
		
		// Get args and the number of them
		$argc = func_num_args();
		$argv = func_get_args();
		
		// Initialize the object regarding the parameters given
		switch($argc)
		{
			case 2: // new XsdElement(elementTypeString, attributesArray)
				if(is_string($argv[0]) && is_array($argv[1]))
				{
					$this->elementType = $argv[0];
					$this->elementAttributes = $argv[1];
				}
				else
				{
					$this->elementType = null;
				}
				
				$level = self::$LEVELS['NO_DBG'];
				
				break;
			case 3: // new XsdElement(elementTypeString, attributesArray, debugBoolean)
				if(is_string($argv[0]) && is_array($argv[1]) && is_bool($argv[2])) // Check data type
				{
					$this->elementType = $argv[0];
					$this->elementAttributes = $argv[1];
					if($argv[2]) $level = self::$LEVELS['DBG'];
					else $level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this->elementType = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default: // Number of args != 2 or 3
				$this->elementType = null;
				$level = self::$LEVELS['NO_DBG'];
				break;
		}
		
		// Initialize the logger (will throw an Exception if any problem occured)
		$this->LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);
		
		if($this->elementType==null) // If an error occured during the initalization of the object
		{
			$log_mess = '';
			
			// Build the log message according to the number of args
			switch($argc)
			{
				case 2: 
					$log_mess .= 'Supports {string, array} as parameters ({'.gettype($argv[0]).','.gettype($argv[1]).'} given)';
					break;
				case 3: 
					$log_mess .= 'Supports {string, array, boolean} as parameters ({'.gettype($argv[0]).','.gettype($argv[1]).','.gettype($argv[2]).'} given)';
					break;
				default:
					$log_mess .= '2 or 3 parameters must be entered ('.$argc.' given)';
					break;
			}
			
			$this->LOGGER->log_error($log_mess, 'XsdElement::__construct');			
			throw new Exception('Invalid parameters given to XsdElement');
		}
		else
		{
			$this->LOGGER->log_debug('Element set '.$this, 'XsdElement::__construct');
		}
	}
	
	/**
	 * Return the name of an element
	 * @return string Name of the tag
	 */
	public function getType()
	{
		$this->LOGGER->log_notice('Function called for '.$this, 'XsdElement::getType');
		return $this->elementType;
	}
	
	/**
	 * Return every attributes of an element 
	 * @return array Associative array with couples attributeName => attributeValue
	 */
	public function getAttributes()
	{
		$this->LOGGER->log_notice('Function called for '.$this, 'XsdElement::getAttributes');
		return $this->elementAttributes;
	}
	
	/**
	 * Set the array of attributes
	 * 
	 * @todo Remove this function (redundant with addAttribute)
	 * 
	 * @param array $attrArray The array of attributes
	 */
	public function setAttributes($attrArray)
	{
		if(is_array($attrArray))
		{
			if(count($this->elementAttributes)>0) $this->LOGGER->log_info('Attributes are already set and will be erased. To avoid that, use the function addAttributes(array)', 'XsdElement::setAttributes');
			
			$this->elementAttributes = $attrArray;
			$this->LOGGER->log_debug('Attributes array replaced with '.serialize($this->elementAttributes), 'XsdElement::setAttributes');
			
			return 0;
		}
		else 
		{
			$this->LOGGER->log_error('Input parameter must be an array ('.gettype($attrArray).' given)', 'XsdElement::setAttributes');
			return -1;
		}
		
	}
	
	/**
	 * Add new attributes to the current object
	 * 
	 * @todo Rename into addAtrribute and set param as $attrName, $attrValue
	 * 
	 * @param array $attrArray Array of attributes
	 * @return int Error code (0=OK, -1=$attrArray is not an array)
	 */
	public function addAttributes($attrArray)
	{
		if(is_array($attrArray))
		{
			$keys = array_keys($attrArray);
			
			foreach($keys as $key)
			{
				if(array_key_exists($key, $this->elementAttributes))
					$this->LOGGER->log_info('Attribute '.$key.' is already set and will be erased. To avoid that, set up a different attribute name', 'XsdElement::addAttributes');
				
				$this->elementAttributes[$key] = $attrArray[$key];
				
				$this->LOGGER->log_debug('Attributes array is now '.serialize($this->elementAttributes), 'XsdElement::addAttributes');
			}
			
			return 0;
		}
		else 
		{
			$this->LOGGER->log_error('Input parameter must be an array ('.gettype($attrArray).' given)', 'XsdElement::addAttributes');
			return -1;
		}
	}
	
	/**
	 * Remove an attribute from the attribute list
	 * 
	 * @param string $attrName Name of the attribute to remove
	 * @return int 0 if everything is OK, -1 otherwise
	 */
	public function removeAttribute($attrName)
	{
		if(array_key_exists($attrName, $this->elementAttributes))
		{
			unset($this->elementAttributes[$attrName]);
			$this->LOGGER->log_debug('Attribute '.$attrName.' has been erased', 'XsdElement::removeAttribute');
			
			return 0;
		}
		else 
		{
			$this->LOGGER->log_error('Attribute '.$attrName.' does not exists', 'XsdElement::removeAttribute');
			return -1;
		}
		
	}
	
	/**
	 * Compare the current object with another XsdElement
	 * 
	 * @todo Rename to equalsTo(...)
	 * 
	 * @return boolean TRUE if the two objects are identical
	 */
	public function compare($otherXsdElement)
	{
		if(gettype($otherXsdElement)=='object' && get_class($otherXsdElement)=='XsdElement') // If we have two instance of the same class
		{
			// Compare type
			$otherType = $otherXsdElement->getType();
			$sameType = false;
			
			if($otherType[0]=='/' && $otherType[strlen($otherType)-1]=='/')
				$sameType = preg_match($otherType, $this->elementType);
			else
				$sameType = $otherType==$this->elementType;
			
			if($sameType)
			{
				// Compare attributes
				$otherAttributes = $otherXsdElement->getAttributes();
				$otherAttrKeys = array_keys($otherAttributes);
				
				$thisAttributes = $this->elementAttributes;
				$thisAttrKeys = array_keys($thisAttributes);
				
				foreach($otherAttrKeys as $otherKey)
				{
					if(in_array($otherKey, $thisAttrKeys))
					{
						$otherAttr = $otherAttributes[$otherKey];
						$sameAttr = false;
						
						if($otherAttr[0]=='/' && $otherAttr[strlen($otherAttr)-1]=='/')
							$sameAttr = preg_match($otherAttr, $thisAttributes[$otherKey]);
						else
							$sameAttr = $otherAttr==$thisAttributes[$otherKey];
						
						if(!$sameAttr)
						{
							$this->LOGGER->log_debug('Comparison failed at key '.$otherKey.' for elements '.$otherXsdElement.' and '.$this, 'XsdElement::compare');
							return false;
						}
					}
					else
					{
						$this->LOGGER->log_debug('Comparison failed at key '.$otherKey.' for elements '.$otherXsdElement.' and '.$this, 'XsdElement::compare');
						return false;
					}
				}
				
				$this->LOGGER->log_debug('Element comparison return true for '.$otherXsdElement.' and '.$this, 'XsdElement::compare');
				return true;
			}
			else {
				$this->LOGGER->log_debug('Type are not matching for elements '.$otherXsdElement.' and '.$this, 'XsdElement::compare');
				return false;
			}
		}
		else
		{
			$type = gettype($otherXsdElement);
			$class = $type=='object'?' ('.get_class($otherXsdElement).')':'';
			
			$this->LOGGER->log_debug('XsdElement cannot be compared with '.$type.$class, 'XsdElement::compare');
			return false;
		}
	}

	/**
	 * Return the description of the object
	 * @return string Description of the object
	 */
	public function __toString()
	{
		$resultString = $this->elementType.'{ ';
		foreach($this->elementAttributes as $attrName=>$attrValue)
		{
			if(!is_array($attrValue)) $resultString.=$attrName.' = '.$attrValue;
			else {
				$resultString.=$attrName.' = (';
				foreach($attrValue as $value)
				{
					$resultString.=$value;
					if(end($attrValue)!=$value) $resultString.=',';
				}
				$resultString.=')';
			}
			if(end($this->elementAttributes)!=$attrValue) $resultString.=' | ';
		}
		
		$resultString.=' }';
		
		$this->LOGGER->log_debug('Function returned '.$resultString, 'XsdElement::toString');
		
		return $resultString;
	}
}