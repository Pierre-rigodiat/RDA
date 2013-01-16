<?php
/**
 * 
 */
// TODO Change class name as HandlerDisplay 
// TODO Add a PageHandler to the class
class ModuleDisplay 
{
	private $moduleHandler;
	//xxx private $pageHandler;
	
	// Debug and logging variables
	private $LOGGER;
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	private static $LOG_FILE;
	private static $FILE_NAME = 'ModuleDisplay.php';
	
	/**
	 * 
	 */
	public function __construct() 
	{
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'] . '/logs/module_display.log';

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 1 :
				// new ModuleDisplay(moduleHandler)
				if (is_object($argv[0]) && get_class($argv[0]) == 'ModuleHandler')
				{
					$this -> moduleHandler = $argv[0];
					$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> moduleHandler = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			case 2 :
				// new ModuleDisplay(moduleHandler, debugBoolean)
				if (is_object($argv[0]) && get_class($argv[0]) == 'ModuleHandler' && is_bool($argv[1]))
				{
					$this -> moduleHandler = $argv[0];

					if ($argv[1])
						$level = self::$LEVELS['DBG'];
					else
						$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> moduleHandler = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default :
				$this -> moduleHandler = null;
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

		if ($this -> moduleHandler == null)
		{
			$log_mess = '';

			switch($argc)
			{
				case 1 :
					$log_mess .= 'Supports ModuleHandler (object) as parameter (' . gettype($argv[0]) . ' given)';
					break;
				case 2 :
					$log_mess .= 'Supports {ModuleHandler(object), boolean} as parameters ({' . gettype($argv[0]) . ',' . gettype($argv[1]) . '} given)';
					break;
				default :
					$log_mess .= '1 or 2 parameters must be entered (' . $argc . 'given)';
					break;
			}

			$this -> LOGGER -> log_error($log_mess, 'ModuleDisplay::__construct');
		}
		else
			$this -> LOGGER -> log_debug('ModuleDisplay successfully built', 'ModuleDisplay::__construct');
	}

	/**
	 * 
	 */
	public function setModuleHandler($moduleHandler)
	{
		
	}
	
	/**
	 * 
	 */
	public function displayModuleChooser()
	{
		$result = '';
		
		$moduleList = $this -> moduleHandler -> getModuleList();
		foreach($moduleList as $module)
		{
			$iconString = $this->moduleHandler->getModuleStatus($module['name'])==1?'on':'off';
					
			$result .= '<div class="module"><span class="icon legend '.$iconString.'">'.ucfirst($module['name']).'</span></div>';
		}
		
		return $result;
	}
	
	/**
	 * 
	 */
	public function displayPopUpModuleSelect()
	{
		$result = '';
		
		$moduleList = $this -> moduleHandler -> getModuleList('enable');
		foreach($moduleList as $module)
		{
			$result .= '<option value="'.$module['name'].'">'.ucfirst($module['name']).'</option>';
		}
		
		return $result;		
	}
	
	/**
	 * 
	 */
	public function displayModulePage($moduleName)
	{
		
	}
	
}



?>