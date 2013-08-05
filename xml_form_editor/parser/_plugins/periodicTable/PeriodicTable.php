<?php
/**
 *
 */
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/_plugins/__model__/ModuleInterface.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['modules_dirname'].'/periodicTable/core/PeriodicTableModule.php';
/** @ignore */
require_once $_SESSION['xsd_parser']['conf']['modules_dirname'].'/periodicTable/view/PeriodicTableDisplay.php';
/**
 *
 */
class PeriodicTable implements ModuleInterface {

    public static function initModule($tree)
    {
        if(!isset($_SESSION['xsd_parser']['modules']['pertable']['model']) || !isset($_SESSION['xsd_parser']['modules']['pertable']['view']))
        {
            // TODO Check the return codes
            $periodicTableModule = new PeriodicTableModule($tree, true);
            $periodicTableDisplay = new PeriodicTableDisplay($periodicTableModule, true);

            $_SESSION['xsd_parser']['modules']['pertable']['model'] = serialize($periodicTableModule);
            $_SESSION['xsd_parser']['modules']['pertable']['view'] = serialize($periodicTableDisplay);

            return 0;
        }
        else return 1; // Module already loaded
    }


    public static function displayModule()
    {
        if(isset($_SESSION['xsd_parser']['modules']['pertable']['view']))
        {
            $moduleDisplay = unserialize($_SESSION['xsd_parser']['modules']['pertable']['view']);

            $module = '<div class="periodic_table_module">';
            $module .= $moduleDisplay->display();
            $module .= '</div>';

            return $module;
        }
        else
        {
            return 'Module not initialized';
        }
    }


    public static function getModuleData()
    {
		if(isset($_SESSION['xsd_parser']['modules']['pertable']['model']))
		{
			$periodicTable = unserialize($_SESSION['xsd_parser']['modules']['pertable']['model']);
			return $periodicTable -> getXmlData();
		}
		else
			return null;
    }


    public static function __toArray()
    {

    }
}
