<?php
	session_start();
	
	require_once $_SESSION['config']['_ROOT_'].'/inc/lib/StringFunctions.php';

	/**
	 * Edit the $_SESSION array containing the element list.
	 * The request should be:
	 * 		changeELement.php?id=13&min=1&max=unbounded&type=string&...
	 * The $_GET array should contain:
	 * 		id: Id of the element inside the $_SESSION array
	 * 		min: the minimum number of elements
	 * 		max: the maximum number of elements
	 * 		[type: datatype of the element]
	 * 		[default: XXX NOT YET IMPLEMENTED]
	 * 		[ai: "on" if the data is auto-generated]
	 */
	// TODO add additional control to be sure nothing has been manually modified into the code
	// ie the ID of the element
	// Check the difference between the 2 states of the element if it appears to be incoherent, we cancel the change
	// todo need to update $_SESSION[i_m] 
	if(isset($_GET['id']) && isset($_GET['min']) && (isset($_GET['max']) || isset($_GET['unbounded'])))
	{
		$attributes = $_SESSION['elementList'][$_GET['id']]['attributes']; // A value to simplify the writting
		$set_min = -1; // MINOCCURS default value (-1 = not set)
		$set_max = -1; // MAXOCCURS default value (-1 = not set)
		$set_ai = 'false';
				
		// The function to filter attributes into the attributes array	
		if(!defined("filter_attribute")) // Avoid to redefine the function
		{
			define("filter_attribute", true);
			
			function filter_attribute($var)
			{
				$attr_not_disp = array('NAME', 'id', 'TYPE'); // TYPE is first removed but if needed it will be pushed into the array			
				return !in_array($var, $attr_not_disp);
			}
		}
			
		/* 1st PART: COMPUTING $_SESSION */
				
		// Check if MINOCCURS, MAXOCCURS and AUTO_GEN are set in the $_SESSION array
		if(isset($attributes['MINOCCURS'])) $set_min = $_SESSION['elementList'][$_GET['id']]['attributes']['MINOCCURS'];
		if(isset($attributes['MAXOCCURS'])) $set_max = $_SESSION['elementList'][$_GET['id']]['attributes']['MAXOCCURS'];
		if(isset($attributes['AUTO_GEN'])) $set_ai = $attributes['AUTO_GEN'];
		
		// MINOCCURS management
		if($_GET['min'] != $set_min)
		{
			if($_GET['min']!=1)
			{
				$_SESSION['elementList'][$_GET['id']]['attributes']['MINOCCURS'] = $_GET['min'];
			}
			else
			{
				if($set_min > -1) unset($_SESSION['elementList'][$_GET['id']]['attributes']['MINOCCURS']);		
			}
		}
		
		// MAXOCCURS management
		if(!isset($_GET['max'])) $max = 'unbounded';
		else $max = $_GET['max'];
		
		if($max != $set_max)
		{
			if($max!=1)
			{
				$_SESSION['elementList'][$_GET['id']]['attributes']['MAXOCCURS'] = $max;
			}
			else
			{
				if($set_max > -1) unset($_SESSION['elementList'][$_GET['id']]['attributes']['MAXOCCURS']);		
			}
		}
		
		// TYPE management
		if(isset($_GET['type']) && $_GET['type']!='')
		{
			$_SESSION['elementList'][$_GET['id']]['attributes']['TYPE'] = $_SESSION['namespace'].$_GET['type'];
		}

		// Autogenerate management
		if(isset($_GET['ai']) && $_GET['ai']!=$set_ai)
		{
			if($_GET['ai']== 'true') $_SESSION['elementList'][$_GET['id']]['attributes']['AUTO_GEN'] = $_GET['ai'];
			else unset($_SESSION['elementList'][$_GET['id']]['attributes']['AUTO_GEN']);
		}
		
		/* 2nd PART: DISPLAY */
		
		$attributes = $_SESSION['elementList'][$_GET['id']]['attributes']; // We reset the variable regarding the changes made above
		//print_r($attributes);
		
		// Format the attributes array
		$attr_name_array = array_filter(array_keys($attributes), "filter_attribute");
		$type_attr = array();
		
		if(isset($attributes['TYPE']) && startsWith($attributes['TYPE'], $_SESSION['namespace']))
		{
			// Attribute type is truncated
			$type_attr = explode(':', $attributes['TYPE']);				
			array_push($attr_name_array, 'TYPE');
		}
		
		foreach($attr_name_array as $attr_name)
		{		
			if($attr_name=='TYPE') echo $attr_name.': '.$type_attr[1];
			else echo $attr_name.': '.$attributes[$attr_name];
				
			if(end($attr_name_array)!=$attr_name) echo ' | ';	
		}
	}
?>