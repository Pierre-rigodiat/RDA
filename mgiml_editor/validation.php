<?php 
	session_start(); 
	require_once 'inc/global/config.php';
	require_once 'classes/XsdParser.php';
	
	require_once 'lib/StringFunctions.php';
	require_once 'inc/global/images.php'; // XXX Regroupe in the head.php file
	
?>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Form Generator 0.1</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<meta http-equiv="Author" content="Alexander Bell" />
<meta http-equiv="Copyright" content="2011 Infosoft International Inc" />
<meta http-equiv="Expires" content="0" />
<meta http-equiv="Cache-control" content="no-cache">

<meta name="Robots" content="all" />
<meta name="Distribution" content="global" />

<link rel="stylesheet" href="css/step2.css" />

<script type="text/javascript" src='js/message.js'></script>
<link rel="stylesheet" type="text/css" href="css/themes/message_growl_shiny.css">

<link href="css/xml_display.css" type="text/css" rel="stylesheet">
<script type="text/javascript" src="js/xml_display.js"></script>

<script src="http://code.jquery.com/jquery-latest.js"></script>
<script src="js/util.js"></script>
<script src="js/step3.js"></script>

</head>
<body>
<?php
	$start = (float) array_sum(explode(' ',microtime()));

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
?>
	<h1>Validation page</h1>
	
	<a href="">Display all</a> <a href="">Hide all</a>
	<br />

	<?php 
		
	
	
		$xmlContent = $xsd_parser->buildXML($_POST, $_SESSION);
		
		$_SESSION['xml_content'] = $xmlContent;
		/*$xmlContent = htmlspecialchars(nl2br($xmlContent), ENT_NOQUOTES, "UTF-8", false);
		
		$xmlContent = displayXMLContent($xmlContent);*/
	?>
	
	<div id="XMLHolder" style="background-color:#FFFFFF;" ></div>
	<script>LoadXMLString('XMLHolder',"<?php echo $xmlContent; ?>");</script>
	
	<a href="step2.php">Back to the edition page</a> <input type="button" class="download" value="Download the file"/>
	
	
	
	<?php 
	echo '<hr/>';
	
	if(isset($_POST))
	{
		print_r($_POST);
	}
	
	echo '<hr/>';
	
	if(isset($_SESSION))
	{
		print_r($_SESSION);
	}
	
	$end = (float) array_sum(explode(' ',microtime()));
	
	echo '<hr/>';
	echo "Processing time: <b>".sprintf("%.4f", ($end-$start))."</b> seconds";
	
	?>
</body>