<?php
	// TODO Check if there is no error in case nothing is loaded
	require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';
?>
<div id="featured-wrapper"><div id="featured">
	<h1>Data Entry</h1>
	<p>
		Here you can fill in the Material Data form. Once it is completed, you can view the data you have entered.
	</p>
</div></div>

<div id="main">
<?php
	if(($htmlForm = displayHTMLForm()) == null)
	{
?>
<div class="alert alert-block">
	<p>
		<i class="icon warning"></i>
		<strong>Warning:</strong> You have to select a template to be able to see this preview.
		
		<button class="btn btn-small btn-warning pull-right">Select a template</button>
	</p>
</div>
<?php
	}
	else 
	{
?>
<div class="message"></div>
<div class="toolbar">
	
	
	<div class="btn-group pull-right">
		<button class="btn clear-fields"><i class="icon-file"></i> Clear fields</button>
		<button class="btn load-form"><i class="icon-folder-open"></i> Load form</button>
		<button class="btn save-form"><i class="icon-hdd"></i> Save form</button>
	</div>
	
	
	
	<div class="pagination">
	<?php
		displayPageNavigator();
	?>	
	</div>
	
	
	
	<!--div class="right-side">
		<span class="ctx_menu">
			<span class="icon legend long blank">Clear all fields</span>
			<span class="icon legend long load">Load form</span>
			<span class="icon legend save">Save</span>
		</span>
	</div-->
</div>

<?php
	echo $htmlForm;
?>

<div class="toolbar">
	<div class="pagination">
	<?php
		displayPageNavigator();
	?>	
	</div>
	
	
<!--div class="left-side">
<?php
	displayPageNavigator();
?>	
</div-->
</div>
<?php	
	}
?>
	
	
	
	
</div>

<script src="parser/controllers/js/addRemove.js"></script>
<script src="parser/controllers/js/pagination.js"></script>
<script src="parser/controllers/js/choice.js"></script>
<script src="ontology/auto-complete.js"></script>
<script src="inc/controllers/js/register_form.js"></script>
<script>
	/**
	 * Load all the JavaScript events needed
	 * Prevent addition of a listener to a same element
	 */
	loadRegisterFormController();
	
	if(!registerFormLibLoaded)
	{
		loadAddRemoveController();
		loadPaginationController();
		loadChoiceController();
		
		loadAutoComplete();
		
		
		console.log('[/register] Libraries succefully loaded!');
		
		registerFormLibLoaded = true;
	}
	else console.log('[/register] Libraries already loaded');
</script>