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
 * // Then we add new attributes
 * $newAttribute = array(
 * 		"minOccurs" => 0,
 * 		"maxOccurs" => "unbounded"
 * );
 * $xsdElement -> addAttributes($newAttribute); // Return code: 0
 *
 * // Remove an attribute
 * $attrToRemove = array(
 * 		"maxOccurs"
 * );
 * $xsdElement -> removeAttributes($attrToRemove); // Return code: 0
 *
 * // Compare to an attribute
 *
 * // Display the
 * echo $xsdElement; // Will return xs:element{ name = root | type = Root | minOccurs = 0 }
 *
 * </code>
 *
 * @todo Improve the debugging
 * @todo Complete the __equalsTo description
 *
 * @author P. Dessauw <philippe.dessauw@nist.gov>
 * @copyright NIST 2013
 * @example debug/UnitTest/XsdElementUnitTest.php Unit tests for an XsdElement
 *
 * @package XsdMan\Core
 */
class XsdElement
{
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
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
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
	 * @throws Exception Argument count or type of argument not good
	 */
	public function __construct()
	{
		// Require the logger and configure the log file
		require_once $_SESSION['xsd_parser']['conf']['dirname'] . '/inc/helpers/Logger.php';
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'] . '/logs/xsd_element.log';

		// Get args and the number of them
		$argc = func_num_args();
		$argv = func_get_args();

		// Initialize the object regarding the parameters given
		switch($argc)
		{
			case 2 :
				// new XsdElement(elementTypeString, attributesArray)
				if (is_string($argv[0]) && is_array($argv[1]))
				{
					$this -> elementType = $argv[0];
					$this -> elementAttributes = $argv[1];
				}
				else
				{
					$this -> elementType = null;
				}

				$level = self::$LEVELS['NO_DBG'];

				break;
			case 3 :
				// new XsdElement(elementTypeString, attributesArray, debugBoolean)
				if (is_string($argv[0]) && is_array($argv[1]) && is_bool($argv[2]))// Check data type
				{
					$this -> elementType = $argv[0];
					$this -> elementAttributes = $argv[1];
					if ($argv[2])
						$level = self::$LEVELS['DBG'];
					else
						$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> elementType = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default :
				// Number of args != 2 or 3
				$this -> elementType = null;
				$level = self::$LEVELS['NO_DBG'];
				break;
		}

		// Initialize the logger (will throw an Exception if any problem occurs)
		$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);

		if ($this -> elementType == null)// If an error occured during the initalization of the object
		{
			$log_mess = '';

			// Build the log message according to the number of args
			switch($argc)
			{
				case 2 :
					$log_mess .= 'Supports {string, array} as parameters ({' . gettype($argv[0]) . ',' . gettype($argv[1]) . '} given)';
					break;
				case 3 :
					$log_mess .= 'Supports {string, array, boolean} as parameters ({' . gettype($argv[0]) . ',' . gettype($argv[1]) . ',' . gettype($argv[2]) . '} given)';
					break;
				default :
					$log_mess .= '2 or 3 parameters must be entered (' . $argc . ' given)';
					break;
			}

			$this -> LOGGER -> log_error($log_mess, 'XsdElement::__construct');
			throw new Exception('Invalid parameters given to XsdElement');
		}
		else
		{
			$this -> LOGGER -> log_debug('Element set ' . $this, 'XsdElement::__construct');
		}
	}

	/**
	 * Add new attributes to the current object
	 * 
	 * <u>Error code</u> are the following:
	 * <ul>
	 * 		<li><b>0</b> Attributes have been removed</li>
	 * 		<li><b>1</b> One or several attributes have been override</li>
	 * 		<li><b>2</b> Attribute name is not a string</li>
	 * 		<li><b>3</b> Combinaison of error code 1 & 2</li>
	 * 		<li><b>-1</b> Parameter is not an array</li>
	 * </ul>
	 * 
	 * <u>Example:</u>
	 * <code>
	 * // Let $xsdElement attributes be equals to the empty array
	 * $additionalAttr = array(
	 * 	"attr1" => "value1",
	 * 	"attr2" => "value2"
	 * );
	 * 
	 * $xsdElement->addAttributes($additionalAttr); // $xsdElement now contains 2 attributes
	 * </code>
	 *
	 * @param array $attrArray Array of attributes
	 * @return int Error code
	 */
	public function addAttributes($attrArray)
	{
		if (is_array($attrArray))
		{
			$keys = array_keys($attrArray);

			// Possible error code (non code breaker)
			$overrideExistingAttributeError = 0;
			$notStringAttributeNameError = 0;

			foreach ($keys as $key)
			{
				if(is_string($key))
				{
					if (array_key_exists($key, $this -> elementAttributes)) // Attribute will be override
					{
						$this -> LOGGER -> log_info('Attribute ' . $key . ' is already set and will be erased. To avoid that, set up a different attribute name', 'XsdElement::addAttributes');
						$overrideExistingAttributeError = 1;
					}

					$this -> elementAttributes[$key] = $attrArray[$key];
					$this -> LOGGER -> log_debug('Attributes array is now ' . serialize($this -> elementAttributes), 'XsdElement::addAttributes');
				}
				else // Attribute name is not a string
				{
					$this -> LOGGER -> log_warning('Attribute ' . $key . ' is not a string and will be excluded', 'XsdElement::addAttributes');
					$notStringAttributeNameError = 1;
				}
			}

			return ($notStringAttributeNameError*2+$overrideExistingAttributeError);
		}
		else
		{
			$this -> LOGGER -> log_error('Input parameter must be an array (' . gettype($attrArray) . ' given)', 'XsdElement::addAttributes');
			return -1;
		}
	}

	/**
	 * Remove an attribute from the attribute list
	 * 
	 * <u>Error code</u> are the following:
	 * <ul>
	 * 		<li><b>0</b> Attributes have been removed</li>
	 * 		<li><b>-1</b> Array does not respect the correct structure</li>
	 * 		<li><b>1</b> One of the attribute does not exist</li>
	 * </ul>
	 * 
	 * <u>Example:</u>
	 * <code>
	 * // Let assume that $xsdElement has 2 attributes: attr1 with value value1, attr2 with value value2 
	 * $removalAttr = array(
	 * 	"attr1"
	 * );
	 * 
	 * $xsdElement->removeAttributes($removalAttr); // $xsdElement now contains 1 attributes (attr2 containing value2)
	 * </code>
	 *
	 * @param array $attrNameArray An array containing the name of all attributes to remove
	 * @return int Error code
	 */
	public function removeAttributes($attrNameArray)
	{
		if(is_array($attrNameArray))
		{
			$errorCode = 0;
			
			foreach ($attrNameArray as $attrName) {
				if (array_key_exists($attrName, $this -> elementAttributes))
				{
					unset($this -> elementAttributes[$attrName]);
					$this -> LOGGER -> log_debug('Attribute ' . $attrName . ' has been erased', 'XsdElement::removeAttributes');
				}
				else
				{
					$this -> LOGGER -> log_info('Attribute ' . $attrName . ' does not exists', 'XsdElement::removeAttributes');
					$errorCode = 1;
				}
				
				return $errorCode;
			}
		}
		else 
		{
			$this -> LOGGER -> log_error('Parameter is not an array', 'XsdElement::removeAttributes');
			return -1;
		}		
	}

	/**
	 * Remove all attributes of the element
	 * 
	 * <u>Error code</u> are the following:
	 * <ul>
	 * 		<li><b>0</b> Attributes have been removed</li>
	 * 		<li><b>1</b> Attribute list does not exist</li>
	 * </ul>
	 * 
	 * @return int Error code
	 */
	public function removeAllAttributes()
	{
		if(isset($this -> elementAttributes))
		{
			$this -> elementAttributes = array();
			$this -> LOGGER -> log_debug('Attributes has been erased for ' . $this, 'XsdElement::removeAllAttributes');
			
			return 0;
		}
		else
		{
			$this -> LOGGER -> log_error('Attributes not found for' . $this, 'XsdElement::removeAllAttributes');
			return -1;
		}
		
	}

	/**
	 * Return the name of an element
	 * @return string Name of the tag
	 */
	public function getType()
	{
		$this -> LOGGER -> log_notice('Function called for ' . $this, 'XsdElement::getType');
		return $this -> elementType;
	}

	/**
	 * Return every attributes of an element. 
	 * 
	 * Structure of the result is the following:
	 * <code>
	 * array(
	 * 		"attrName_1" => "attrValue_1",
	 * 		...
	 * 		"attrName_n" => "attrValue_n"
	 * );
	 * </code>
	 * 
	 * @return array Associative array
	 */
	public function getAttributes()
	{
		$this -> LOGGER -> log_notice('Function called for ' . $this, 'XsdElement::getAttributes');
		return $this -> elementAttributes;
	}

	/**
	 * Compare the current object with another XsdElement
	 * 
	 * @param XsdElement $otherXsdElement Another XsdElement object
	 * @return boolean TRUE if the two objects are similar
	 */
	public function __equalsTo($otherXsdElement)
	{
		if (gettype($otherXsdElement) == 'object' && get_class($otherXsdElement) == 'XsdElement')// If we have two instance of the same class
		{
			// Compare type
			$otherType = $otherXsdElement -> getType();
			$sameType = false;

			if ($otherType[0] == '/' && $otherType[strlen($otherType) - 1] == '/')
				$sameType = preg_match($otherType, $this -> elementType);
			else
				$sameType = $otherType == $this -> elementType;

			if ($sameType)
			{
				// Compare attributes
				$otherAttributes = $otherXsdElement -> getAttributes();
				$otherAttrKeys = array_keys($otherAttributes);

				$thisAttributes = $this -> elementAttributes;
				$thisAttrKeys = array_keys($thisAttributes);

				foreach ($otherAttrKeys as $otherKey)
				{
					if (in_array($otherKey, $thisAttrKeys))
					{
						$otherAttr = $otherAttributes[$otherKey];
						$sameAttr = false;

						if ($otherAttr[0] == '/' && $otherAttr[strlen($otherAttr) - 1] == '/')
							$sameAttr = preg_match($otherAttr, $thisAttributes[$otherKey]);
						else
							$sameAttr = $otherAttr == $thisAttributes[$otherKey];

						if (!$sameAttr)
						{
							$this -> LOGGER -> log_debug('Comparison failed at key ' . $otherKey . ' for elements ' . $otherXsdElement . ' and ' . $this, 'XsdElement::__equalsTo');
							return false;
						}
					}
					else
					{
						$this -> LOGGER -> log_debug('Comparison failed at key ' . $otherKey . ' for elements ' . $otherXsdElement . ' and ' . $this, 'XsdElement::__equalsTo');
						return false;
					}
				}

				$this -> LOGGER -> log_debug('Element comparison return true for ' . $otherXsdElement . ' and ' . $this, 'XsdElement::__equalsTo');
				return true;
			}
			else
			{
				$this -> LOGGER -> log_debug('Type are not matching for elements ' . $otherXsdElement . ' and ' . $this, 'XsdElement::__equalsTo');
				return false;
			}
		}
		else
		{
			$type = gettype($otherXsdElement);
			$class = $type == 'object' ? ' (' . get_class($otherXsdElement) . ')' : '';

			$this -> LOGGER -> log_debug('XsdElement cannot be compared with ' . $type . $class, 'XsdElement::__equalsTo');
			return false;
		}
	}

	/**
	 * Return the description of the object
	 * 
	 * The string is formatted like that:
	 * <code>
	 * 		XSD:ELEMENT{ATTR1 = VAL1 | ... | ATTRn = VALn}
	 * </code>
	 * 
	 * @return string Description of the object
	 */
	public function __toString()
	{
		$resultString = $this -> elementType . '{ ';
		foreach ($this->elementAttributes as $attrName => $attrValue)
		{
			if (!is_array($attrValue))
				$resultString .= $attrName . ' = ' . $attrValue;
			else
			{
				$resultString .= $attrName . ' = (';
				foreach ($attrValue as $value)
				{
					$resultString .= $value;
					if (end($attrValue) != $value)
						$resultString .= ',';
				}
				$resultString .= ')';
			}
			if (end($this -> elementAttributes) != $attrValue)
				$resultString .= ' | ';
		}

		$resultString .= ' }';

		$this -> LOGGER -> log_notice('Function returned ' . $resultString, 'XsdElement::__toString');
		return $resultString;
	}

}
