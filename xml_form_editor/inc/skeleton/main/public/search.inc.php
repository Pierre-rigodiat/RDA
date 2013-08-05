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
		<button class="btn submit query pull-right"><i class="icon-search"></i> Submit</button>
	</div>
	
<?php
	displayQuery();
?>

	<div>
		<button class="btn submit query pull-right"><i class="icon-search"></i> Submit</button>
	</div>
	
	<div id="XMLContainer"></div>
	
	<div>
		<div id="download"></div>
	</div>
	
	<script src="inc/controllers/js/explore_data.js"></script>
	<script>
		loadExploreDataController();
	</script>
</div>