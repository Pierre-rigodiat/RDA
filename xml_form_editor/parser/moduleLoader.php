<?php
/**
 * Load every module in a variable session
 * 
 * 
 */
if(!isset($_SESSION['xsd_parser']['modules'])) $_SESSION['xsd_parser']['modules'] = array();

// TODO Use the module configuration _plugins/modules.conf.php
$modules = array(
	//'folderName' => 'InitClassName'
	'table' => 'Table'
);

foreach ($modules as $folderName => $moduleInitClass) {
	require_once $_SESSION['xsd_parser']['conf']['modules_dirname'].'/'.$folderName.'/'.$moduleInitClass.'.php';
}

// TODO Make the appropriate checks to avoid errors
// XXX Check if the class implements ModuleInterface
// XXX Check if files & folders exists

/**
 * Initialize a module
 * @param {string} $moduleName
 */
function initModuleWithId($moduleName)
{
	global $modules;
	// TODO add a return value to know if the module has been properly initialize
	
	$initModuleClass = $modules[$moduleName];
	
	$tree = 3;
	call_user_func($initModuleClass.'::initModule', $tree);
}

/**
 * Display a module
 * @param {string} $moduleName
 */
function displayModule($moduleName)
{
	global $modules;
	
	// TODO Check if the module has been initialze, otherwise do it
	initModuleWithId($moduleName);
	
	$initModuleClass = $modules[$moduleName];
	$moduleCode = call_user_func($initModuleClass.'::displayModule');
	
	return $moduleCode;
}
?>