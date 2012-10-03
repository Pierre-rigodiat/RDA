<?php 
	$step = 1;

	if(isset($_GET['step']))
	{
		$step = $_GET['step'];
		
		if($step<1 || $step>3)
		{
			$step = 1;
		}
	}

?>

<ul class="tabbed">
	<li <?php if($step==1) echo 'class="current_page_item"'; ?>><a href="">Load Schema</a></li>
	<li <?php if($step==2) echo 'class="current_page_item"'; ?>><a href="">Enter data</a></li>
	<li <?php if($step==3) echo 'class="current_page_item"'; ?>><a href="">Validate XML</a></li>
</ul>