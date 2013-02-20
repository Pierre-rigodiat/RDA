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
	<div>
		<div class="right-side">
			<span class="ctx_menu">
				<span class="icon legend long download xml">Download file</span>
			</span>
		</div>
	</div>
	
	<div id="XMLHolder"></div>
	
	<script src="resources/js.new/view_xml.js"></script>
	<script>
		LoadXMLString('XMLHolder', <?php echo "'".str_replace('"', '\\"', displayXmlTree())."'"; ?>);
		
		loadViewXmlController();
	</script>
</div>