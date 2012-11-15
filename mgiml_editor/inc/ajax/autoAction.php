<?php
if(isset($_SESSION['app']['actions']) && isset($_SESSION['app']['data_tree'])) 
{
?>
<script src="resources/js/autoFill.js"></script>
<script>
$(document).ready(function(){
	<?php
		$actionIndex = 0;
	
		// Adding/removing the proper elements
		foreach($_SESSION['app']['actions'] as $action)
		{
			$actionInfos = explode('|', $action);
			echo 'autoClick("'.$actionInfos[1].'","'.$actionInfos[0].'");'.PHP_EOL;
			
			unset($_SESSION['app']['actions'][$actionIndex]);
			$actionIndex += 1;
		}
		
		$inputs = array_keys($_SESSION['app']['data_tree']);
		foreach($inputs as $input)
		{
			$jsArrayBuildString = '[';
			foreach($_SESSION['app']['data_tree'][$input] as $value)
			{
				$jsArrayBuildString .= '"'.$value.'",';
			}
			
			$jsArrayBuildString[strlen($jsArrayBuildString)-1] = ']';
			
			echo 'autoFill("'.$input.'",'.$jsArrayBuildString.');'; 
		}
		
		
	?>
});
</script>
<?php
	$_SESSION['app']['actions'] = array_values($_SESSION['app']['actions']);
}
?>