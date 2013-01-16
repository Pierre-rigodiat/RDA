<!--
	Schema Configuration View
	Version 0.2 (12-13-2012)
-->
<div id="featured-wrapper"><div id="featured">
	<h1>Module manager</h1>
	<p>
		Here you can choose the module to enable or disable.
	</p>
</div></div>

<div id="main">

<div class="left-side">
	<span class="ctx_menu">
		<div class="icon legend long upload">Upload module</div>
	</span>
</div>

<div class="right-side">
<form>
	<input type="text" class="text" id="search" name="search"/>
	<div class="icon search"></div>
</form>
</div>

<hr/>
<div id="schema_content">
	<div id="schema_modules">
		<?php
			require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';		
			displayModuleChooser();
		?>
		<!--div class="module"><span class="icon legend off">Pagination<span class="icon new"></span></span></div>
		<div class="module"><span class="icon legend off">HDF-5</span></div>
		<div class="module"><span class="icon legend disable">Images (Coming soon)</span></div>
		<div class="module"><span class="icon legend disable">Videos (Coming soon)</span></div-->
	</div>
</div>
</div>

<script src="parser/controllers/js/module.js"></script>
<script src="resources/js.new/mod_mgr.js"></script>
<script>
	loadModuleController();
	loadModMgrController();
</script>