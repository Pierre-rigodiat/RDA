<?php
if(isset($_GET['p']) && $_GET['p']=="admin")
{
	$submenus = array("website" => array("Workflow", "Pages", "Menus", "Modules"), "schemas" => array("Current Model", "Manage Schemas", "Manage Modules", "Manage Queries"), "users" => array("New User", "New Group", "Search"));
	$submenusIds = array("website" => array("workflow", "pages", "menus", "modules"), "schemas" => array("currentModel", "manageSchemas", "manageModules", "manageQueries"), "users" => array("newUser", "newGroup", "search"));
	
	if(isset($_GET['sp']) && isset($submenus[$_GET['sp']]))
	{
?>
	<ul class="tabbed">
	<?php
		$keys = array_keys($submenus[$_GET['sp']]);
		
		$names = $submenus[$_GET['sp']];
		$ids = $submenusIds[$_GET['sp']];
		
		$isFirstElement = true;
		
		foreach($keys as $key)
		{
			//echo '<li class="submenu current_page_item">'.$submenu.'</li>';
			echo '<li class="submenu';
			if($isFirstElement) echo ' current';
			echo '" id="'.$ids[$key].'">'.$names[$key].'</li>';
			
			$isFirstElement = false;
		}	
	?>
	</ul>
<?php
	}
}
else 
{
	$submenus = array("register" => array("Enter Data", "View XML"));
	$submenusIds = array("register" => array("form", "xml"));
	
	// Include modules
	
	if(isset($_GET['sp']) && isset($submenus[$_GET['sp']]))
	{
?>
	<ul class="tabbed">
	<?php
		$keys = array_keys($submenus[$_GET['sp']]);
		
		$names = $submenus[$_GET['sp']];
		$ids = $submenusIds[$_GET['sp']];
		
		$isFirstElement = true;
		
		foreach($keys as $key)
		{
			//echo '<li class="submenu current_page_item">'.$submenu.'</li>';
			echo '<li class="submenu';
			if($isFirstElement) echo ' current';
			echo '" id="'.$ids[$key].'">'.$names[$key].'</li>';
			
			$isFirstElement = false;
		}	
	?>
	</ul>
<?php	
	}
}
?>




