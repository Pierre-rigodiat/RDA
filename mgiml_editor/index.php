<!DOCTYPE html>
<html>
<head>
<title>MGIML Editor v0.1</title>
<meta http-equiv="X-UA-Compatible" content="IE=8;" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8" />

<meta name="description" content="This page is the MGIML Editor" />
<meta name="keywords" content="editor, XML, mgiml" />

<link rel="stylesheet" type="text/css" href="css/main.css" />

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
<script type="text/javascript" src="scripts/launch.js"></script>
<script type="text/javascript">
			function init () { 
				new Editor('../lib/axel/axel');  // for axel.css and resource folder bundles/
			}		
			xtdom.addEventListener(window,  'load', init, false);
		</script>
</head>
<body>
	<div id="menu" class="noprint">
		<p id="feedback">Template undefined</p>
	</div>
	<div id="document">
		<iframe id="container"> iframe content </iframe>
	</div>
</body>
</html>
