<?php
	session_start();

	require_once $_SESSION['config']['_ROOT_'].'/inc/lib/FileFunctions.php';

	$dirInfo = listDir($_SESSION['config']['_XSDFOLDER_']);
	
	if($dirInfo['error']==0)
	{
		$xsdFileNumber=0;
		$htmlSelectOptionsString ="";
		
		foreach($dirInfo['files'] as $file)
		{
			if($file[1]=='file' && endsWith($file[0], '.xsd'))
			{
				$htmlSelectOptionsString .= '<option>'.$file[0].'</option>';
				$xsdFileNumber+=1;
			} 
		}
	}
?>


<h2>Schema manager</h2>


<form>
	<select id="xsdFile">
		<?php
			echo $htmlSelectOptionsString;
		?>
	</select>
	
	<input type="button" class="button" id="loadXsd" value="Load schema" />
	<input type="button" class="button" id="importXsd" value="Import new schema" />
</form>


<table border="1">
	<tr>
		<td>a</td>
		<td>b</td>
		<td>c</td>
	</tr>
	<tr>
		<td>a</td>
		<td>b</td>
		<td>c</td>
	</tr>
	<tr>
		<td>a</td>
		<td>b</td>
		<td>c</td>
	</tr>
	<tr>
		<td>a</td>
		<td>b</td>
		<td>c</td>
	</tr>
</table>