<?php
/*define("DEBUG_XML_LIB", false);
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

// Attributes
/*$level = 0;
$id = -1;
$stack = array();
$elementList = array();*/

//Function to use at the end of an element
/*function stop($parser,$element_name)
{
	global $id, $level, $stack, $elementList;*/

	/**
	 * Updating the stack
	 */

	// Decrease the level
	/*$level -= 1;

	// Remove the stack element
	$stack[$level] = null;

	if(DEBUG_XML_LIB)
	{
		echo "** END of " . $element_name . "<br />";
	}
}

//Function to use at the start of an element
function start($parser,$element_name,$element_attrs)
{
	global $id, $level, $stack, $elementList;

	if(DEBUG_XML_LIB)
	{
		echo 'New elememt: ' . $element_name . '<br/>';
		echo "level: " . $level . ' - ';
		print_r($stack);
		echo '<br/>';
	}

	/**
	 * Store the element into the elementList
	 */

	// Updating the identifier of the element
	/*$id += 1;

	// Find the parent of the element
	$parent = -1;
	if($level > 0) {
		$parent = $stack[$level-1];

		array_push($elementList[$parent]['children'], $id); // Updating the children array
	}

	// Add the element to the list
	$elementList[$id] = array('id' => $id, 'name' => $element_name, 'parent' => $parent, 'children' => array(), 'attributes' => $element_attrs);

	/**
	 * Updating the stack
	 */

	// Add the element to the stack
	/*$stack[$level] = $id;

	// Increment the level
	$level += 1;
}

// Function to use when finding character data
function char($parser,$data) {}

// Make the XML readable in a HTML page
function displayXMLContent($content)
{
	$old = array(htmlspecialchars('<br />'), htmlspecialchars(' '));
	$new = array('<br/>', '&nbsp;');
	
	return str_replace($old, $new, $content);
}
?>*/