<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" type="text/css" href="resources/css/style.css">
<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.1/themes/base/jquery-ui.css" />
<title>Ontology viewer</title>
</head>
<body>
<script src="resources/js/lib/d3.v3.min.js"></script>
<script src="resources/js/lib/d3.packages.js"></script>
<h1>Ontology viewer</h1>
<p id="disclaimer">
	This is a partial reprensentation of the ontology living in the Neo4j database. The starting point is <b>ObjectType</b>	and it displayed up to 5 layers of related terms.
</p>
<div id="node-link"></div>
<!--div id="tabs">
	<ul>
		<li><a href="#node-link">Node link</a></li>
		<li><a href="#edge-bunding">Edge bunding</a></li>
	</ul>
</div-->
<script src="resources/js/lib/jquery-1.9.1.min.js"></script>
<script src="resources/js/lib/jquery-ui-1.10.1.min.js"></script>
<script src="resources/js/draw.js"></script>
<script>
loadDrawController();
drawNodeTree();	

/*$(function() {
	$( "#tabs" ).tabs();
});*/
</script>
</body>
</html>