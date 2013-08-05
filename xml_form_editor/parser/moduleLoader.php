<?php
/**
 * Load every module in a variable session
 *
 *
 */

// FIXME All these functions must be in the ModuleHandler class

if(!isset($_SESSION['xsd_parser']['modules'])) $_SESSION['xsd_parser']['modules'] = array();

// TODO Use the module configuration _plugins/modules.conf.php
$modules = array(
	//'folderName' => 'InitClassName'
	'table' => 'Table',
	'periodictable' => 'PeriodicTable'
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
function initModuleWithId($moduleName, $elementId=0)
{
	global $modules;

	// TODO add a return value to know if the module has been properly initialized
	$initModuleClass = $modules[$moduleName];

	// FIXME Send an actual tree
	$tree = new Tree("ModuleTree");
	$tree -> insert($elementId);

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
	/*if(!isset($_SESSION[]))*/initModuleWithId($moduleName);

	$initModuleClass = $modules[$moduleName];
	$moduleCode = call_user_func($initModuleClass.'::displayModule');

	return $moduleCode;
}

/**
 *
 */
function retrieveModuleDataForId($moduleName, $elementId)
{
	global $modules;

	// TODO Check if the module has been initialzed
	$initModuleClass = $modules[$moduleName];

	$moduleDataArray = call_user_func($initModuleClass.'::getModuleData');

	return $moduleDataArray;
}
?>