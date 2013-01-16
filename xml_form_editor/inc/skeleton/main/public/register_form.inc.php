<div id="featured-wrapper"><div id="featured">
	<h1>Data entering</h1>
	<p>
		In this step, you have to fill in the form. During the process you can save your work in order to complete it later.<br/>
		Once you have fill every field, you can view the XML.
	</p>
</div></div>

<div id="main">
<div class="left-side">
	<span class="ctx_menu"><span class="icon begin"></span></span>
	<span class="ctx_menu"><span class="icon previous"></span></span>
	<span class="ctx_menu button">1</span>
	<span class="ctx_menu selected">2</span>
	<span class="ctx_menu button">3</span>
	<span class="ctx_menu button">4</span>
	<span class="ctx_menu button">5</span>
	<span class="ctx_menu"><span class="icon next"></span></span>
	<span class="ctx_menu"><span class="icon end"></span></span>
</div>
	
<div class="right-side">
	<span class="ctx_menu">
		<span class="icon legend long blank">Clear all fields</span>
		<span class="icon legend save">Save</span>
	</span>
</div>

<?php
	// TODO Check if there is no error in case nothing is loaded
	require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';
	displayHTMLForm();
?>

<div class="left-side">
	<span class="ctx_menu"><span class="icon begin"></span></span>
	<span class="ctx_menu"><span class="icon previous"></span></span>
	<span class="ctx_menu button">1</span>
	<span class="ctx_menu selected">2</span>
	<span class="ctx_menu button">3</span>
	<span class="ctx_menu button">4</span>
	<span class="ctx_menu button">5</span>
	<span class="ctx_menu"><span class="icon next"></span></span>
	<span class="ctx_menu"><span class="icon end"></span></span>
</div>
	
<div class="right-side">
	<span class="ctx_menu">
		<span class="icon legend long blank">Clear all fields</span>
		<span class="icon legend save">Save</span>
	</span>
</div>
</div>

<script src="parser/controllers/js/addRemove.js"></script>
<script src="resources/js.new/mod_mgr.js"></script>
<script>
	loadAddRemoveController();
</script>