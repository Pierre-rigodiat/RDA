<?php
	/* TODO Implement it
	
	require_once $_SESSION['config']['_ROOT_'].'/app/core/Website.php';
	require_once $_SESSION['config']['_ROOT_'].'/app/view/Display.php';

	$website = new Website();
	$display = new Display($website);
	
	$display -> displayMenu();*/
	
	// Subpart configuration
	$defaultCursor = 'home'; // 'home' is the default configuration page
	
	if(isset($_GET['sp']))
	{
		$existingPages = array('website','schemas', 'users', 'register', 'search'); // todo handle it in a different class or into the db
		
		if(in_array($_GET['sp'], $existingPages)) $cursor = $_GET['sp'];
		else $cursor = $defaultCursor;
	}
	else $cursor = $defaultCursor; 
?>

<?php
	if(isset($_GET['p']) && $_GET['p']=="admin")
	{
?>
<ul class="tabbed">
	<li class="<?php if($cursor=='home') echo ' current_page_item'; ?>"><a href="home">Home</a></li>
	<li class="<?php if($cursor=='website') echo ' current_page_item current_page_parent'; ?>"><a href="website">Website</a></li>
	<li class="<?php if($cursor=='schemas') echo ' current_page_item current_page_parent'; ?>"><a href="schemas">XML Schemas</a></li>
	<li class="<?php if($cursor=='users') echo ' current_page_item current_page_parent'; ?>"><a href="users">User Management</a></li>
</ul>
<?php	
	}
	else {
?>
<ul class="tabbed">
	<li <?php if($cursor=='home') echo 'class="current_page_item"'; ?>><a href="home">Home</a></li>
	<li <?php if($cursor=='register') echo 'class="current_page_item current_page_parent"'; ?>><a href="register">Data Curation</a></li>
	<li <?php if($cursor=='search') echo 'class="current_page_item"'; ?>><a href="search">Data Exploration</a></li>
</ul>
<?php	
	}
?>