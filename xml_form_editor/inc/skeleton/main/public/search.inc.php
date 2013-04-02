<?php
	require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';
?>
<div id="featured-wrapper"><div id="featured">
	<h1>Data Exploration</h1>
	<p>
		This page is dedicated to the data exploration. Fill out the form to retrieve the corresponding data.
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
	displayQuery();
?>

	<div>
		<div class="right-side">
			<span class="ctx_menu">
				<span class="icon legend add id">Submit</span>
			</span>
		</div>
	</div>
	
	<div id="query_result"></div>
	
	<script src="inc/controllers/js/explore_data.js"></script>
	<script>
		loadExploreDataController();
	</script>
</div>