<?php
	require_once '../app/core/Menu.php';
	
	$menu = new Menu("admin");
	
	$menu = new Menu("admin/schemas/manager");
	
	
	echo $menu.'<hr/>';
	var_dump($menu->getMenusName());
	var_dump($menu->getSubmenusName());
	
	echo $menu -> getPageFileName();
