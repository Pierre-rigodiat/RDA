<center><h2>Form validation</h2></center>

<?php 
				//$start = (float) array_sum(explode(' ',microtime()));

	$xsd_parser = new XsdParser($_SESSION['elementList'], $_SESSION['rootElement'], $_SESSION['namespace']);
	
	// XXX Modify it to fit it to our needs
	function myErrorHandler($errno, $errstr, $errfile, $errline) {
		if ( E_RECOVERABLE_ERROR===$errno ) {
			echo "'catched' catchable fatal error (".$errno.", ".$errstr.", ".$errfile.", ".$errline.") <br/>";
			throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
			
			//return true;
		}
		return false;
	}
	set_error_handler('myErrorHandler');
	
	
	$xmlContent = $xsd_parser->buildXML($_POST, $_SESSION);
	
	$_SESSION['xml_content'] = $xmlContent;
	
	
	?>
	
	<div id="XMLHolder" style="background-color:#FFFFFF;" ></div>
	<script>LoadXMLString('XMLHolder',"<?php echo $xmlContent; ?>");</script>
	
	<input type="button" class="button" id="tostep2" value="Go back"/>
	<input type="button" class="button" id="download" value="Download the file"/>
	
	
	
	<?php 
	/*echo '<hr/>';
	
	if(isset($_POST))
	{
		print_r($_POST);
	}
	
	echo '<hr/>';
	
	if(isset($_SESSION))
	{
		print_r($_SESSION);
	}*/
	
	/*$end = (float) array_sum(explode(' ',microtime()));
	
	echo '<hr/>';
	echo "Processing time: <b>".sprintf("%.4f", ($end-$start))."</b> seconds<br/>";
	echo "Allocating memory: <b>".memory_get_usage().'</b> bytes';*/
	
	?>