<?php
/**
 * Display the view of the plugin
 * 
 * 
 */
class TableDisplay 
{
	private $tableModule; // The instance of the plugin
	
	// Logging variables
	private $LOGGER;
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	private static $LOG_FILE;
	private static $FILE_NAME = 'TableDisplay.php';
	
	/**
	 * 
	 */
	public function __construct() 
	{
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['logs_dirname'].'/module.log';

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 1 :
				// new TableModule(tree)
				if (is_object($argv[0]) && get_class($argv[0]) == 'TableModule')
				{
					$this -> tableModule = $argv[0];
					$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> tableModule = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			case 2 :
				// new TableModule(tree, debugBoolean)
				if (is_object($argv[0]) && get_class($argv[0]) == 'TableModule' && is_bool($argv[1]))
				{
					$this -> tableModule = $argv[0];
					
					if ($argv[1])
						$level = self::$LEVELS['DBG'];
					else
						$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> tableModule = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default :
				$this -> tableModule = null;
				$level = self::$LEVELS['NO_DBG'];
				break;
		}

		try
		{
			$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);
		}
		catch (Exception $ex)
		{
			echo '<b>Impossible to build the Logger:</b><br/>' . $ex -> getMessage();
			return;
		}

		if ($this -> tableModule == null)
		{
			$log_mess = '';

			switch($argc)
			{
				case 1 :
					$log_mess .= '1st parameter must be a Tree object';
					break;
				case 2 :
					$log_mess .= 'Supports {Tree, boolean} as parameters ({' . gettype($argv[0]) . ',' . gettype($argv[1]) . '} given)';
					break;
				default :
					$log_mess .= '1 or 2 parameters must be entered (' . $argc . 'given)';
					break;
			}

			$this -> LOGGER -> log_error($log_mess, 'TableDisplay::__construct');
		}
		else
		{
			$this -> LOGGER -> log_debug('Table module successfully built', 'TableDisplay::__construct');
		}
	}
	
	/**
	 * Display the plugin view
	 * @return {string} HTML code of the module
	 */
	public function display()
	{
		$moduleCode = '<div class="module_title">Table module</div>';
		
		$moduleCode .= '<form id="file_upload" enctype="multipart/form-data">';
		
		/*' accept=".xlsx,.xls"'+*/
		$moduleCode .= '<div class="import"><input type="file" name="table_input[0]" class="text"/><span class="table_import_status"></span></div>';
		
		$moduleCode .= '</form>';
		
		// $moduleCode .= <span class="icon delete"></span>
		$moduleCode .= '<script src="parser/_plugins/table/controllers/js/addRemoveFile.js"></script>';
		$moduleCode .= '<script>loadAddRemoveFileController();</script>';
		
		return $moduleCode;
	}
	
	/**
	 * 
	 * @return {TableModule} Instance of TableModule used
	 */
	public function getTableModule()
	{
		return $this->tableModule;
	}
}


?>