<?php
	require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';
?>
<div id="featured-wrapper"><div id="featured">
	<h1>XML View</h1>
	<p>
		This a preview of the XML which will be generated. Each modification you make in the form will be written in this preview.
	</p>
</div></div>

<div id="main">
	<div id="XMLHolder"></div>
	<script>
		LoadXMLString('XMLHolder', <?php displayXmlTree(); ?>);
	</script>
</div>