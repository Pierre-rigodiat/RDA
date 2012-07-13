<!DOCTYPE html>
<html>
	<head>
		<title>MGIML Editor v0.1</title>
		<meta http-equiv="X-UA-Compatible" content="IE=8;" />	
		<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	
		<meta name="description" content="This page contains a demonstration launcher for the AXEL (Adaptable XML Editing Library) Javascript library.  It starts diverse XML editors based on different document templates." />
		<meta name="keywords" content="editor, XML, document template" />
		<meta name="author" content="Stéphane Sire" />
		
		<style type="text/css">
		body {
			padding: 0;
			margin: 0;
			min-width: 650px;
		}
		div#menu {
			background: lightgray;
			min-width: 600px;
			margin: 0 auto;		
			padding: 5px 10px;
		}	
		#document {
			border: none;
			background: white;  
			position: fixed;
			top: 2em;
			right: 10px;
			bottom: 10px;
			left: 10px;	 
			margin: 0;		
			padding: 0;
			z-index: 2;
		}
		#container {
			border: none;
			position: static;
			width: 100%;
			height: 100%;
		}
		#feedback {
			padding: 0;
			margin: 0;
			text-align: center;
		}
		</style>     
		
	  <!--[if IE 7]>    
	  <style type="text/css">
		#document {
			height: 95%;
		}
		</style>
	  <![endif]-->	
		<script type="text/javascript" src="../lib/axel/axel/axel.js"></script>
		<script type="text/javascript" src="../lib/axel/src/util/debug.js"></script>
		<script type="text/javascript" src="../lib/axel/src/util/davmenubar.js"></script>
		<script type="text/javascript" src="launch.js"></script>
		<script type="text/javascript">
			function init () { 
				new Editor('../lib/axel/axel');  // for axel.css and resource folder bundles/
			}		
			xtdom.addEventListener(window,  'load', init, false);
		</script>
	</head>
	<body>
		<?php 
			//echo 'MGIML Editor';
		?>
		<div id="menu" class="noprint">
		<p id="feedback">Usage: edit.xhtml#t=template.xtd[ &amp;d=data.xml ][ &amp; p=path_to_lib ]</p>	
		</div>         
		<div id="document">                            
		  	<iframe id="container">	iframe content </iframe>	
		</div>
	</body>
</html>
