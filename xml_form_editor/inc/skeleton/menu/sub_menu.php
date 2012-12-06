<?php
if(isset($_GET['p']) && $_GET['p']=="admin")
{
	$submenus = array("website" => array("Workflow", "Pages", "Menus", "Modules"), "schemas" => array("Current model", "Manage schemas"), "users" => array("New user", "New group", "Search"));
	$submenusIds = array("website" => array("workflow", "pages", "menus", "modules"), "schemas" => array("currentModel", "manageSchemas"), "users" => array("newUser", "newGroup", "search"));
?>
	<ul class="tabbed">
		<?php
			if(isset($_GET['sp']) && isset($submenus[$_GET['sp']]))
			{
				$keys = array_keys($submenus[$_GET['sp']]);
				
				$names = $submenus[$_GET['sp']];
				$ids = $submenusIds[$_GET['sp']];
				
				foreach($keys as $key)
					//echo '<li class="submenu current_page_item">'.$submenu.'</li>';
					echo '<li class="submenu" id="'.$ids[$key].'">'.$names[$key].'</li>';
			}
		?>
	</ul>
<?php
}
else 
{
?>
	<!--ul class="tabbed">
		<li class="current_page_item"><a href="#">Audio Software</a></li>
		<li><a href="#">Video Software</a></li>
		<li><a href="#">Third Party Plugins</a></li>
	</ul-->
<?php	
}
?>




