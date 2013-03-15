<?php
// TODO Rewrite the debug part using the parser configuration
/*define("DEBUG_XML_LIB", true);
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/inc/helpers/Logger.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';*/

/**
 * XML parser functions
 * 
 * 		function stop($parser,$element_name)
 * 		function start($parser,$element_name,$element_attrs)
 * 		function char($parser,$data)
 * 		function displayXMLContent(string $content)
 * 
 */
 
// Logger implementation
/*$LOGGER = null;

if(DEBUG_XML_LIB) $LOGGER = new Logger('notice', $_SESSION['xsd_parser']['conf']['dirname'].'/logs/xml_lib.log', 'XmlParserFunctions.php');
else $LOGGER = new Logger('info', $_SESSION['xsd_parser']['conf']['dirname'].'/logs/xml_lib.log', 'XmlParserFunctions.php');
 
// Attributes
$level = 0;
$id = -1;
$stack = array();
$elementList = array();
$elementTree = new Tree(DEBUG_XML_LIB);*/

/**
 * Function used on a start tag (<element>)
 */
/*function start($parser,$element_name,$element_attrs)
{
	global $id, $level, $stack, $elementList, $elementTree, $LOGGER;

	/**
	 * Store the element into the elementList
	 */
	// Find the parent of the element
	/*$parent = -1;
	if($level > 0) {
		$parent = $stack[$level-1];
	}

	// Create the element
	$element = new XsdElement($element_name, $element_attrs, true);
	// Add the element to the tree
	$id = $elementTree->insertElement($element, $parent);
	
	$LOGGER->log_debug('New element '.$element_name.' inserted', 'start');

	/**
	 * Updating the stack
	 */
	// Add the element to the stack
	/*$stack[$level] = $id;

	// Increment the level
	$level += 1;
}

/**
 * Function used reading a character
 */
/*function char($parser,$data) {}

/**
 * Function used at the end of an element (</element>)
 */
/*function stop($parser,$element_name)
{
	global $id, $level, $stack, $elementList, $elementTree, $LOGGER;

	/**
	 * Updating the stack
	 */

	// Decrease the level
	/*$level -= 1;

	// Remove the stack element
	$stack[$level] = null;
	
	$LOGGER->log_debug('End reading '.$element_name, 'stop');
}

/**
 * Make the XML readable in a HTML page
 */
/*function displayXMLContent($content)
{
	$old = array(htmlspecialchars('<br />'), htmlspecialchars(' '));
	$new = array('<br/>', '&nbsp;');
	
	return str_replace($old, $new, $content);
}*/
?>