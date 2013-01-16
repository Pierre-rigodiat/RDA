<?php
	session_start();
	if(isset($_SESSION['xsd_parser']))
	{
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
	}
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
	<h1>Session variables explorer</h1>
	
	<hr/>
	<h3>Main variable: $_SESSION['xsd_parser']</h3>
	<a href="back/clrsessvar.php?v=parser">Clear variables</a><br/>
	<?php
		if(isset($_SESSION['xsd_parser'])) var_dump($_SESSION['xsd_parser']);
		else echo 'Parser variables not set';
	?>
	<hr/>
	<h3>Configuration: $_SESSION['xsd_parser']['conf']</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<ul>
	<?php
		/*if(isset($_SESSION['xsd_parser']) && isset($_SESSION['xsd_parser']['tree']))
		{
			$treeObj = unserialize($_SESSION['xsd_parser']['tree']);
			foreach($treeObj->getTree() as $id=>$element)
			{
				echo '<li>ID '.$id.': '.$element['object'].'</li>';
			}
		}
		else echo 'Tree not set';*/
	
	?>
	</ul>
	<hr/>
	<h3>Parser: $_SESSION['xsd_parser']['parser']</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<hr/>
	<h3>XSD Tree</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<hr/>
	<h3>XML Tree</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<hr/>
	<h3>Module handler</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<hr/>
	<h3>Page handler</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
</body>
</html>