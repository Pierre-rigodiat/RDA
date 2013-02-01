<?php
	require_once $_SESSION['config']['_ROOT_'].'/inc/lib/StringFunctions.php';
?>
<div id="featured-wrapper"><div id="featured">
	<h1>Schema manager</h1>
</div></div>

<div id="main">
<?php
	if(!isset($_SESSION['xsd_parser']['xsd_filename']))
	{
		echo '<div class="warn"><div class="icon warning"></div>The system has no schema loaded. Please set a current model to allow user to use the repository.</div>';	
	}
?>
	
<div class="right-side">
	<span class="ctx_menu">
		<div class="icon legend long upload">Upload schema</div>
		<div class="icon legend long blank">Create new file</div>
	</span>
</div>

<table class="data-table">
	<tr>
		<th>Schema name</th>
		<th>Root element</th>
		<th>Status</th>
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
							<td>'.'Experiment'.'</td>
							<td style="color:'.'green'.'">'.'Registered'.'</td>
							<td>'.'<div class="icon legend extra-long add">Set as current model</div><div class="icon legend delete">Delete</div>'.'</td>
						</tr>';
			}
			$even = !$even;
		}
	?>
	<tr class="even">
		<td>file1.xsd</td>
		<td>Experiment</td>
		<td style="color:orange">Uploaded</td>
		<td><div class="icon legend save">Save</div><div class="icon legend edit">Edit</div><div class="icon legend delete">Delete</div></td>
	</tr>
	<tr>
		<td>schema.xsd</td>
		<td>Experiment</td>
		<td style="color:blue; font-weight:bold">Current model</td>
		<td><div class="icon legend delete">Delete</div></td>
	</tr>
	<tr class="even">
		<td>demo3.xsd</td>
		<td>Experiment</td>
		<td style="color:green">Registered</td>
		<td><div class="icon legend extra-long add">Set as current model</div><div class="icon legend delete">Delete</div></td>
	</tr>
</table>

<div class="right-side">
	<span class="ctx_menu">
		<div class="icon legend long upload">Upload schema</div>
		<div class="icon legend long blank">Create new file</div>
	</span>
</div>
</div>

<script src="resources/js.new/xsd_mgr.js"></script>
<script>
	loadXsdManagerHandler();
</script>