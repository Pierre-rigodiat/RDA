<center>
	<h2>Form edition</h2>
</center>

<?php
$xsd_parser = new XsdParser($_SESSION['elementList'], $_SESSION['rootElement'], $_SESSION['namespace']/*, true*/);
?>

<?php
	echo '<a href=""><<</a> ';
	echo '<a href=""><</a> ';

	for($i=1; $i<6; $i++)
	{
		echo '<a href="">'.$i.'</a> ';
	}

	echo '<a href="">></a> ';
	echo '<a href="">>></a> ';
?>

<form method="post" action="inc/ajax/registerXmlData.php">
	<?php
	/* Configuring the reset of the $_SESSION */
	if(isset($_GET['reset']))
	{
		unset($_SESSION['xml_content']);
		unset($_SESSION['app']['data_tree']);
		unset($_SESSION['app']['actions']);
		unset($_SESSION['app']['xml']['tables']);
		
		// Delete multiplicity
		unset($_SESSION['app']['multiplicity']);
		$keys_array = preg_grep('`^e[0-9]+$`', array_keys($_SESSION));
		foreach($keys_array as $key)
		{
			unset($_SESSION[$key]);
		}
	}	
	
	// XXX debug
	/*if(isset($_SESSION['app']['actions'])) print_r($_SESSION['app']['actions']);
	if(isset($_SESSION['app']['data_tree'])) print_r($_SESSION['app']['data_tree']);*/
	
	// todo find a cleaner way to do that
	/*if(isset($_SESSION['page']))
	{
		$xsd_parser->pageNumber = $_SESSION['page'];
		
		echo 'Page: '.$_SESSION['page'];
	}*/
	 
	
	$xsd_parser->buildHTML();
	
	// XXX Last element is not working properly (max occurs is false)
	
	?>
	
	<!--input type="submit" class="button" name="goto1" value="Go back" /-->
	<input type="button" class="button reset" value="Reset form" />
	<input type="submit" class="button" name="goto3" value="Next step" />
	
	<?php
		// TODO Implement the automated click when $data_tree and actions is set
		require_once '/inc/ajax/autoAction.php';
	
		// xxx debug
		/*if(isset($_SESSION['app']['actions'])) print_r($_SESSION['app']['actions']);
		if(isset($_SESSION['app']['data_tree'])) print_r($_SESSION['app']['data_tree']);*/
	
	?>
</form>