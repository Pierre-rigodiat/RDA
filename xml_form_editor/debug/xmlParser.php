<?php
	session_start();
	/*if(isset($_SESSION['xsd_parser']))
	{
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
	}*/
	
	require_once '../parser/core/XmlParser.php';
?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	<title>Session explorer</title>
</head>
<body id="content-wrapper">
	<h1>XMLParser class</h1>
	<p>
		File: demo.diffusion.xsd<br/>
		<?php
			$time = microtime(TRUE);
			$mem = memory_get_usage();
		
			$fileName = $_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/schemas/demo.diffusion.xsd';
			
			$xmlParser = new XmlParser();
			$xmlParser -> parse($fileName);
			echo 'Memory: '.round((memory_get_usage() - $mem) / (1024 * 1024), 2).' Mb<br/>';
			echo 'Time: '.round(microtime(TRUE) - $time, 1). ' sec';
			
			echo $xmlParser -> getParsingData();
		?>
	</p>
</body>
</html>