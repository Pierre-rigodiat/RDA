<center>
	<h2>Form edition</h2>
</center>

<?php
	$start = (float) array_sum(explode(' ',microtime()));

	$xsd_parser = new XsdParser($_SESSION['elementList'], $_SESSION['rootElement'], $_SESSION['namespace']);
?>


<form method="post" action="?step=3">
		<?php 
		if(isset($_SESSION)) // XXX Act wisely before erasing everything
		{
			$keys_array = preg_grep('`^e[0-9]+$`', array_keys($_SESSION));
				
			//echo count($keys_array).' counted element'; XXX DEBUG
				
			foreach($keys_array as $key)
			{
				unset($_SESSION[$key]);
			}
		}
		
		
			// XXX Last element is not working properly (max occurs is false)
			$xsd_parser->buildHTML();
		?>
		
		<input type="button" class="button" id="tostep1" value="Go back" />
		<input type="submit" class="button" value="Submit" />
	</form>
	<?php 
	$end = (float) array_sum(explode(' ',microtime()));
	
	echo '<hr/>';
	echo "Processing time: <b>".sprintf("%.4f", ($end-$start))."</b> seconds<br/>";
	echo "Allocating memory: <b>".memory_get_usage().'</b> bytes';
	?>