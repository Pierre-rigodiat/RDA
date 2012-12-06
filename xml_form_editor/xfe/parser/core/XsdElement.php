<?php
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';

/**
 * The class managing the element data structure
 */
/*
 * TODO define precisely an element
 * It has:
 * - A unique ID (automatically generated)
 * - A tagName
 * - Attributes
 * 
 * TODO define a function list
 * You can
 * - Get an Set the tagName
 * - 
 *  
 */
class XsdElement {
	private $elementType;
	private $elementAttributes;
	
	private $LOGGER;
	
	private static $LEVELS = array('DBG'=>'notice', 'NO_DBG'=>'info');
	private static $LOG_FILE;
	private static $FILE_NAME = 'XsdElement.php';
	
	public function __construct()
	{
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'].'/logs/xsd_element.log';
		
		$argc = func_num_args();
		$argv = func_get_args();
		
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
					$this->elementAttributes = null;
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
					$this->elementAttributes = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default:
				$this->elementType = null;
				$this->elementAttributes = null;
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
		
		if($this->elementType==null && $this->elementAttributes == null)
		{
			$log_mess = '';
			
			switch($argc)
			{
				case 2: 
					$log_mess .= 'Supports {string, array} as parameters ({'.gettype($argv[0]).','.gettype($argv[1]).'} given)';
					break;
				case 3: 
					$log_mess .= 'Supports {string, array, boolean} as parameters ({'.gettype($argv[0]).','.gettype($argv[1]).','.gettype($argv[2]).'} given)';
					break;
				default:
					$log_mess .= '2 or 3 parameters must be entered ('.$argc.'given)';
					break;
			}
			
			$this->LOGGER->log_error($log_mess, 'XsdElement::__construct');
		}
		else
		{
			$this->LOGGER->log_debug('Element set with {type: '.$this->elementType.';attributes: '.serialize($this->elementAttributes).'} ', 'XsdElement::__construct');
		}
	}
	
	public function getType()
	{
		$this->LOGGER->log_notice('Function called', 'XsdElement::getType');
		return $this->elementType;
	}
	
	public function getAttributes()
	{
		$this->LOGGER->log_notice('Function called', 'XsdElement::getAttributes');
		return $this->elementAttributes;
	}
	
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
							$this->LOGGER->log_debug('Comparison failed at key '.$otherKey.' for elements '.serialize($otherXsdElement).' and '.serialize($this), 'XsdElement::compare');
							return false;
						}
					}
					else
					{
						$this->LOGGER->log_debug('Comparison failed at key '.$otherKey.' for elements '.serialize($otherXsdElement).' and '.serialize($this), 'XsdElement::compare');
						return false;
					}
				}
				
				$this->LOGGER->log_debug('Element comparison return true for '.serialize($otherXsdElement).' and '.serialize($this), 'XsdElement::compare');
				return true;
			}
			else {
				$this->LOGGER->log_debug('Type are not matching for elements '.serialize($otherXsdElement).' and '.serialize($this), 'XsdElement::compare');
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
}

?>