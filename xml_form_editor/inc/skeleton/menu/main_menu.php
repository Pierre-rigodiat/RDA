<?php 
	$step = 1;

	if(isset($_GET['step']))
	{
		$step = $_GET['step'];
		
		if($step<1 || $step>4)
		{
			$step = 1;
		}
	}
	
	// Subpart configuration
	$defaultCursor = 'home'; // 'home' is the default configuration page
	
	if(isset($_GET['sp']))
	{
		$existingPages = array('website','schemas', 'users'); // todo handle it in a different class or into the db
		
		if(in_array($_GET['sp'], $existingPages)) $cursor = $_GET['sp'];
		else $cursor = $defaultCursor;
	}
	else $cursor = $defaultCursor; 
	

?>

<?php
	if(isset($_GET['p']) && $_GET['p']=="admin")
	{
?>
<!--ul class="tabbed">
	<li class="menu<?php if($cursor=='home') echo ' current_page_item'; ?>" id="home"><a href="home">Home</a></li>
	<li class="menu<?php if($cursor=='website') echo ' current_page_item current_page_parent'; ?>" id="website"><a href="website">Website</a></li>
	<li class="menu<?php if($cursor=='schemas') echo ' current_page_item current_page_parent'; ?>" id="schema"><a href="schemas">XML Schemas</a></li>
	<li class="menu<?php if($cursor=='users') echo ' current_page_item current_page_parent'; ?>" id="users"><a href="users">User management</a></li>
</ul-->
<ul class="tabbed">
	<li class="<?php if($cursor=='home') echo ' current_page_item'; ?>"><a href="home">Home</a></li>
	<li class="<?php if($cursor=='website') echo ' current_page_item current_page_parent'; ?>"><a href="website">Website</a></li>
	<li class="<?php if($cursor=='schemas') echo ' current_page_item current_page_parent'; ?>"><a href="schemas">XML Schemas</a></li>
	<li class="<?php if($cursor=='users') echo ' current_page_item current_page_parent'; ?>"><a href="users">User management</a></li>
</ul>
<?php	
	}
	else {
?>
<ul class="tabbed">
	<!--li <?php if($step==1) echo 'class="current_page_item"'; ?>><a href="">Load Schema</a></li-->
	<li <?php if($step==2) echo 'class="current_page_item"'; ?>><a href="">Enter data</a></li>
	<li <?php if($step==3) echo 'class="current_page_item"'; ?>><a href="">Register tables</a></li>
	<li <?php if($step==4) echo 'class="current_page_item"'; ?>><a href="">Validate XML</a></li>
</ul>
<?php	
	}
?>
