<center><h2>Form configuration</h2></center>
<?php
// TODO logging debug trace, etc.
// todo add a reset button
// todo validate the xsd before going on part 2

/* File choosing */
$xsd = "resources/files/schemas/mgiml_a.xsd";
//$xsd = "files/mgiml_light.xsd";
//$xsd = "resources/files/mgiml_ultra_light_b.xsd";

if(isset($_GET['reset']))
{
	//echo 'Reset the element list<br/>';
	
	unset($_SESSION['elementList']);
	unset($_SESSION['rootElement']);
	unset($_SESSION['namespace']);
	
	// xxx modify it to be more precise
	unset($_SESSION['app']);
	
	// todo remove every use of this variable
	unset($_SESSION['temp_content']);
	
	unset($_SESSION);
}

/*if(isset($_SESSION['elementList']))
{
	echo 'Element list is set<br/>';
} xxx debug */

// We begin to parse the file
// TODO Could we use ajax to do that ?
$xsd_parser = new XsdParser($xsd, true);

/* Display the list of element with their attributes */
if(isset($_SESSION['elementList']) && isset($_SESSION['rootElement']) && isset($_SESSION['namespace'])) // If the list of element has been already built, we just reload the display
{
	$xsd_parser->setElementList($_SESSION['elementList']);
	$xsd_parser->setRoot($_SESSION['rootElement']);
	$xsd_parser->setNamespace($_SESSION['namespace']);
	
	$xsd_parser->displayForm();
}
else // Nothing has been build yet so we create the element list
{
	// todo 2 different functions (2 different classes? - 1 for the engineering part the other for the display...)
	$xsd_parser->buildForm();
	
	/*echo '<hr/>'; XXX DEBUG
	print_r($xsd_parser->getElementList());*/ 
	
	$_SESSION['elementList']=$xsd_parser->getElementList();
	$_SESSION['rootElement']=$xsd_parser->getRoot();
	$_SESSION['namespace']=$xsd_parser->getNamespace();
}
?>
<input type="button" class="button" id="tostep2" value="Build the form" />