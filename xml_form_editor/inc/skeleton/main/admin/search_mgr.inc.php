<?php
require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';
?>
<div id="featured-wrapper"><div id="featured">
	<h1>Query Handler View</h1>
	<p>
		This page enables you to choose elements to display in the data exploration. Check the box to display the corresponding element.
	</p>
</div></div>

<div id="main">
	<div>
		<h3 style="float:left">Elements</h3>
		<div class="right-side">
			<span class="ctx_menu">
				<span class="icon legend add id">Submit</span>
			</span>
		</div>
	</div>
	<div id="schema_elements">	
	<?php
		displayAdminQueryTree();
	?>
	</div>
	
	<script src="inc/controllers/js/editModule.js"></script>
	<script src="inc/controllers/js/search_mgr.js"></script>
	<script>
		loadQueryEditController();
		loadQueryManagerController();
	</script>
</div>