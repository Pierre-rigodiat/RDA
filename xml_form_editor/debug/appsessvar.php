<?php
	session_start();
?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	<title>Session variables explorer</title>
</head>
<body id="content-wrapper">
	<h1>Session variables explorer</h1>
	<h3>Parser</h3>
	<a href="back/clrsessvar.php?v=parser">Clear variables</a><br/>
	<?php
		if(isset($_SESSION['xsd_parser'])) var_dump($_SESSION['xsd_parser']);
		else echo 'Parser variables not set';
	?>
</body>
</html>