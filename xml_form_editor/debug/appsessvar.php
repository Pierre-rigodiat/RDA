<?php
	session_start();
	if(isset($_SESSION['xsd_parser']))
	{
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdManager.php';
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/Tree.php';
		require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/core/XsdElement.php';
	}
?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	<meta http-equiv="refresh" content="5" />
	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	<title>Session explorer</title>
</head>
<body id="content-wrapper">
	<?php
		$xsdManager = null;
	
	
		if(isset($_SESSION['xsd_parser'])) 
		{
			
		}
		
		if(isset($_SESSION['xsd_parser']['parser'])) 
		{
			$xsdManager = unserialize($_SESSION['xsd_parser']['parser']);
		}
		
		
	
	?>
	<h1>Session variables explorer</h1>
	<a href="../debug">< Main menu</a>
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
	<?php
		if($xsdManager) var_dump($xsdManager);
		else echo 'Parser variables not set';
	?>
	<hr/>
	<h3>XSD Original Tree</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<?php
		if($xsdManager)
		{
			$originalTree = $xsdManager -> getXsdOriginalTree() -> getTree();
			
			echo '<ul>';
			
			foreach ($originalTree as $elementId => $treeLeaf) {
				echo '<li>';
					
				//echo 'Element ID '.$elementId.': ';
				
				foreach($treeLeaf as $leafAttrName => $leafAttrValue)
				{
					echo $leafAttrName.'=';
					
					if(!is_array($leafAttrValue)) echo $leafAttrValue;
					else {
						echo '{';
						foreach ($leafAttrValue as $key => $value) {
							echo $value;
							
							if(end($leafAttrValue)!=$value) echo ', ';
						}
						
						echo '}';
					}
					
					if(end($treeLeaf)!=$leafAttrValue) echo ' | ';
				}
				
				echo '</li>';
			}
			
			echo '</ul>';
		}
		else echo 'XsdManager not set';
	?>
	<hr/>
	<h3>XML Tree</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<?php
	if($xsdManager)
		{
			$originalTree = $xsdManager -> getXsdCompleteTree() -> getTree();
			
			echo '<ul>';
			
			foreach ($originalTree as $elementId => $treeLeaf) {
				echo '<li>';
					
				//echo 'Element ID '.$elementId.': ';
				
				foreach($treeLeaf as $leafAttrName => $leafAttrValue)
				{
					echo $leafAttrName.'=';
					
					if(!is_array($leafAttrValue)) echo $leafAttrValue;
					else {
						echo '{';
						foreach ($leafAttrValue as $key => $value) {
							echo $value;
							
							if(end($leafAttrValue)!=$value) echo ', ';
						}
						
						echo '}';
					}
					
					if(end($treeLeaf)!=$leafAttrValue) echo ' | ';
				}
				
				echo '</li>';
			}
			
			echo '</ul>';
		}
		else echo 'XsdManager not set';
	?>
	<hr/>
	<h3>Module handler</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<hr/>
	<h3>Page handler</h3>
	<a href="back/clrsessvar.php?v=null">Clear variable</a><br/>
	<?php
		if($xsdManager)
		{
			$pageHandler = $xsdManager -> getPageHandler();
			
			echo nl2br($pageHandler);
		}
	?>
</body>
</html>