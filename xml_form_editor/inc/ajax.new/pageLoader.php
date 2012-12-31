<?php
/**
 * Page loader v0.1
 * 
 * 
 * 
 * 
 */
session_start();
 
// TODO use another way to store the menus
$universe = array('admin', 'public');

$main['public'] = array('home', 'form');
$main['admin'] = array('home', 'website', 'schemas', 'users');

$sub['public']['home'] = array();
$sub['public']['form'] = array('enter_data', 'view_xml');

$sub['admin']['home'] = array();
$sub['admin']['website'] = array();
$sub['admin']['schemas'] = array('current_model', 'manage_schemas');
$sub['admin']['users'] = array();

 
if(isset($_GET['url']))
{
	// Identifying website parts
	$url = $_GET['url'];
	$menu = array();
	
	$urlParts = explode('?', $url);
	if(isset($urlParts[1])) $menu['sub'] = 	$urlParts[1];
	
	$urlParts = explode('/', $urlParts[0]);
	
	$menu['main'] = $urlParts[count($urlParts)-1];
	$menu['universe'] = $urlParts[count($urlParts)-2];
	
	
	if($menu['main']=='schemas')
		require_once $_SESSION['config']['_ROOT_'].'/inc/skeleton/main/admin/xsd_cfg.inc.php';
	
	print_r($menu);
	
	
}
?>