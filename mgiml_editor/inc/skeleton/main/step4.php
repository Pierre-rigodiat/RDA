<center><h2>Form validation</h2></center>

<?php
	
	//print_r($_SESSION['app']['data_tree']);
	
	// XXX Modify it to fit it to our needs
	/*function myErrorHandler($errno, $errstr, $errfile, $errline) {
		if ( E_RECOVERABLE_ERROR===$errno ) {
			echo "'catched' catchable fatal error (".$errno.", ".$errstr.", ".$errfile.", ".$errline.") <br/>";
			throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
			
			//return true;
		}
		return false;
	}
	set_error_handler('myErrorHandler');*/
	if(!isset($_SESSION['app']['actions'])) $_SESSION['app']['actions'] = array();
	
	$xsd_parser = new XsdParser($_SESSION['elementList'], $_SESSION['rootElement'], $_SESSION['namespace']);
	$xmlContent = $xsd_parser->buildXML($_SESSION['app']['data_tree'], $_SESSION['app']['actions']);
	
	$_SESSION['xml_content'] = $xmlContent;
?>
<div id="XMLHolder" style="background-color:#FFFFFF;" ></div>
<script>LoadXMLString('XMLHolder',"<?php echo $xmlContent; ?>");</script>

<input type="button" class="button" id="tostep3" value="Go back"/>
<input type="button" class="button" id="download" value="Download the file"/>
<?php 
/*
 * xxx debug
 * 
 * echo '<hr/>';

if(isset($_POST))
{
	print_r($_POST);
}

echo '<hr/>';

if(isset($_SESSION))
{
	print_r($_SESSION);
}*/
?>