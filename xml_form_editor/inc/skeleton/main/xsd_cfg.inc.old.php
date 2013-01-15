<h2>Schema configuration</h2>

<?php
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
		
		if($xsdFileNumber>0)
		{
?>

<!--form>
	<select id="xsdFile">
		<?php
			echo $htmlSelectOptionsString;
		?>
	</select>
	
	<input type="button" class="button" id="loadXsd" value="Load schema" />
	<input type="button" class="button" id="importXsd" value="Import new schema" />
</form-->
<div id="loadSchemaInfo"></div>
<?php
		}
		else 
		{
			echo 'The schema folder does not contains any correct schema file (*.xsd)'; // TODO error message
		}
	}
	else 
	{
		echo 'The schema folder is not correctly configured (listDir error '.$dirInfo['error'].')'; // TODO error message	
	}
?>
<div id="cfg_content">
<?php
	if(isset($_SESSION['elementList']) && isset($_SESSION['rootElement']) && isset($_SESSION['namespace'])) // If the list of element has been already built, we just reload the display
	{
		$xsd_parser = new XsdParser(null/*, true*/);
		
		$xsd_parser->setElementList($_SESSION['elementList']);
		$xsd_parser->setRoot($_SESSION['rootElement']);
		$xsd_parser->setNamespace($_SESSION['namespace']);
		
		$xsd_parser->displayForm();
	}
?>	
</div>
