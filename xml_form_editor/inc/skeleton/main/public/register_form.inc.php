<?php
	// TODO Check if there is no error in case nothing is loaded
	require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';
?>
<div id="featured-wrapper"><div id="featured">
	<h1>Data entering</h1>
	<p>
		In this step, you have to fill in the form. During the process you can save your work in order to complete it later.<br/>
		Once you have fill every field, you can view the XML.
	</p>
</div></div>

<div id="main">

<div>
	<div class="left-side">
	<?php
		displayPageNavigator();
	?>	
	</div>
		
	<div class="right-side">
		<span class="ctx_menu">
			<span class="icon legend long blank">Clear all fields</span>
			<span class="icon legend save">Save</span>
		</span>
	</div>
</div>

<?php
	displayHTMLForm();
?>

<div>
	<div class="left-side">
	<?php
		displayPageNavigator();
	?>	
	</div>
		
	<div class="right-side">
		<span class="ctx_menu">
			<span class="icon legend long blank">Clear all fields</span>
			<span class="icon legend save">Save</span>
		</span>
	</div>
</div>	
</div>


<script src="parser/controllers/js/addRemove.js"></script>
<script src="parser/controllers/js/pagination.js"></script>
<script src="ontology/auto-complete.js"></script>
<script src="resources/js.new/register_form.js"></script>
<script>
	loadAddRemoveController();
	loadPaginationController();
	loadRegisterFormController();
	
	loadAutocomplete();
</script>