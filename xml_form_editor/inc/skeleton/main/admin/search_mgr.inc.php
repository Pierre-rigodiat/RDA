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
		<div class="right-side">
			<span class="ctx_menu">
				<span class="icon legend add id">Submit</span>
			</span>
		</div>
	</div>
	
<?php
	displayAdminQueryTree();
?>

	<div>
		<div class="right-side">
			<span class="ctx_menu">
				<span class="icon legend add id">Submit</span>
			</span>
		</div>
	</div>
	
	<script src="inc/controllers/js/search_mgr.js"></script>
	<script>
		loadQueryManagerController();
	</script>
</div>