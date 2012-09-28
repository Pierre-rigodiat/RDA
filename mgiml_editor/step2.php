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

<!-- script src="http://code.jquery.com/jquery-latest.js"></script-->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script src="js/util.js"></script>
<script src="js/step2.js"></script>

</head>
<body>
<?php
	$start = (float) array_sum(explode(' ',microtime()));

	$xsd_parser = new XsdParser($_SESSION['elementList'], $_SESSION['rootElement'], $_SESSION['namespace']);
?>
	<h1>The XML Form</h1>
	<form method="post" action="validation.php">
		<?php 
		if(isset($_SESSION)) // XXX Act wisely before erasing everything
		{
			$keys_array = preg_grep('`^e[0-9]+$`', array_keys($_SESSION));
				
			echo count($keys_array).' counted element';
				
			foreach($keys_array as $key)
			{
				unset($_SESSION[$key]);
			}
		}
		
		
			// XXX Last element is not working properly (max occurs is false)
			$xsd_parser->buildHTML();
		?>
	
		<a href="main.php">Go back</a>
		<input type="Submit" value="Submit" />
	</form>
	<?php 
	$end = (float) array_sum(explode(' ',microtime()));
	
	echo '<hr/>';
	echo "Processing time: <b>".sprintf("%.4f", ($end-$start))."</b> seconds";
	?>
</body>