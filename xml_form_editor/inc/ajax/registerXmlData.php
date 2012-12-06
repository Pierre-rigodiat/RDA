<?php
	session_start();

	/*print_r($_POST);
	echo '<br/>';*/

	// TODO figure out another way to display max and min occurs (in an hiding div or smth)
	if(isset($_POST['maxoccurs'])) unset($_POST['maxoccurs']);
	if(isset($_POST['minoccurs'])) unset($_POST['minoccurs']);
	
	/* Modify the page to reach regarding the button pressed. 
	 * If the button name is changed, you are just going to the page where you coming from page
	 */
	$page = "../../index.php"; // XXX Security ? Adaptibility ?
	if(isset($_POST['goto1']))
	{
		$page .= '?step=1';
		unset($_POST['goto1']);
	}
	else if(isset($_POST['goto3']))
	{
		$page .= '?step=3';
		unset($_POST['goto3']);
	}
	else {
		$page .= '?step=2';
	}

	/* We store the $_POST arrays into a $_SESSION variable
	 * Index of $_POST values are resetted to have a nice array
	 */
	$_SESSION['app']['data_tree'] = array();
	$postKeys = array_keys($_POST);
	
	foreach($postKeys as $postKey)
	{
		if(is_array($_POST[$postKey])) 
		{
			$postValue = array_values($_POST[$postKey]);
			$_SESSION['app']['data_tree'][$postKey] = $postValue;
		}
	}
	
	
	/*if(isset($_POST['hasNext']))
	{
		$page = '../../index.php?step=2';
		$_SESSION['page'] += 1;
		
		//echo $_SESSION['page'];
	}
	else {
		unset($_SESSION['page']);
	}
	*/
	/*print_r($_SESSION['app']['data_tree']);
	echo '<br/>Page: '.$page;*/
	
	header('Location: '.$page);
?>