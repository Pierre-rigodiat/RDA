<?php
	require_once $_SESSION['config']['_ROOT_'].'/inc/lib/StringFunctions.php';
?>
<div id="featured-wrapper"><div id="featured">
	<h1>Form Template Selection</h1>
	<p>
		Select a template from the following table. It will automatically load the appropriate form and display it in the next page.
	</p>
</div></div>

<div id="main">
<?php
$current_filename = null;
if(!isset($_SESSION['xsd_parser']['xsd_filename']))
{
?>
<div class="alert">
	<button type="button" class="close" data-dismiss="alert">&times;</button>
	<i class="icon warning disable-selection"></i> No template selected. Select one in the table below.
</div>
<?php
}
else 
{
	$current_filename = $_SESSION['xsd_parser']['xsd_filename'];
}
?>

<!--div class="control-group">
  <div class="controls">
    <div class="input-prepend">
      <span class="add-on"><i class="icon-search"></i></span>
      <input class="input-large" id="inputIcon" type="text" placeholder="Search...">
    </div>
  </div>
</div-->	
	
<table class="table table-bordered">
	<tr>
		<th>Template name</th>
		<!--th>Description</th-->
		<th>Actions</th>
	</tr>
	<?php
		$schemaFolder = $_SESSION['config']['_XSDFOLDER_'];
		$schemaFolderFiles = scandir($schemaFolder);
		
		$even = true;
		foreach($schemaFolderFiles as $file)
		{
			if(endsWith($file, '.xsd')) 
			{
				echo '	<tr'.($even?' class="even"':'').'>
							<td>'.$file.'</td>
							<!--td>'.'In nunc et nibh rutrum volutpat. Sed tempus interdum. Aliquam tempor.'.'</td-->
							<td>'.($current_filename==$file?'<span style="color:green;font-weight:bold">Current template</span>':'<button class="btn set-template"><i class="icon-plus-sign"></i> Set as current template</button>').'</td>
						</tr>';
			}
			$even = !$even;
		}
	?>
</table>

<script src="inc/controllers/js/tpl_sel.js"></script>
<script>	
	loadTemplateSelectionControllers();
</script>
</div>