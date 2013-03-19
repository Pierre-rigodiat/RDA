<?php
/**
 * <ModuleHandler class>
 */
/**
 * The class handling every module
 * 
 * 
 * @package XsdMan\Core
 */
class ModuleHandler 
{
	/**
	 * Array containing all ID associated with a module
	 * 
	 * @var array
	 */
	private $moduleList;
	
	/**
	 * Name of the directory containing all the modules 
	 * @var string
	 */
	private $moduleDir;
	
	private $LOGGER;
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	private static $LOG_FILE;
	private static $FILE_NAME = 'ModuleHandler.php';
	
	/**
	 * Constructor of the class
	 * Takes 1 or 2 parameters
	 * 
	 */
	public function __construct() {
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['logs_dirname'].'/'.$_SESSION['xsd_parser']['conf']['log_file'];

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 1 :
				// new ModuleHandler(moduleDir)
				if (is_string($argv[0]) && is_dir($argv[0]))
				{
					$this -> moduleDir = $argv[0];
					$this -> moduleList = array();
					
					$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> moduleDir = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			case 2 :
				// new ModuleHandler(moduleDir, debugBoolean)
				if (is_string($argv[0]) && is_dir($argv[0]) && is_bool($argv[1]))
				{
					$this -> moduleDir = $argv[0];
					$this -> moduleList = array();

					if ($argv[1])
						$level = self::$LEVELS['DBG'];
					else
						$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> moduleDir = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default :
				$this -> moduleDir = null;
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

		if ($this -> moduleDir == null)
		{
			$log_mess = '';

			switch($argc)
			{
				case 1 :
					$log_mess .= '1st parameter must be a string and a valid directory name';
					break;
				case 2 :
					$log_mess .= 'Supports {string (a valid directory), boolean} as parameters ({' . gettype($argv[0]) . ',' . gettype($argv[1]) . '} given)';
					break;
				default :
					$log_mess .= '1 or 2 parameters must be entered (' . $argc . 'given)';
					break;
			}

			$this -> LOGGER -> log_error($log_mess, 'ModuleHandler::__construct');
		}
		else
		{
			// Build the list of module (avoid listing files and '.' beggining folders)
			// Set up all modules as disabled
			$fileList = scandir($this -> moduleDir);
			
			foreach($fileList as $file)
			{
				if(is_dir($this -> moduleDir.'/'.$file) && !startsWith($file, '.'))
				{
					array_push($this -> moduleList, array('name' => strtolower($file), 'enable' => false, 'ids' => array()));
					
					$this -> LOGGER -> log_debug('Adding '.$file.' to the module list', 'ModuleHandler::__construct');
				}
			}
			
			$this -> LOGGER -> log_debug('Module handler successfully built', 'ModuleHandler::__construct');
		}
	}
	
	/**
	 * 
	 */
	public function updateModuleList()
	{
		/* Not yet implemented */
	}
	
	/**
	 * 
	 * @param string $moduleName Name of the module the user searches
	 */
	public function isInModuleList($moduleName)
	{
		$this->LOGGER->log_debug('Function called w/ module name "'.$moduleName.'"', 'ModuleHandler::isInModuleList');
		
		$index = 0;
		foreach($this -> moduleList as $module)
		{
			if($module['name'] == strtolower($moduleName))
			{
				$this->LOGGER->log_debug('Module '.$moduleName.' has been found at index '.$index, 'ModuleHandler::isInModuleList');
				return $index;
			} 
			$index += 1;
		}
		
		$this->LOGGER->log_info('Module '.$moduleName.' not found', 'ModuleHandler::isInModuleList');
		return -1;
	}
	
	/**
	 * 
	 * 
	 * 
	 */
	public function getModuleStatus($moduleName)
	{
		$this->LOGGER->log_debug('Function called w/ module name "'.$moduleName.'"', 'ModuleHandler::getModuleStatus');
		if(($moduleIndex = $this->isInModuleList($moduleName)) != -1)
		{
			if($this -> moduleList[$moduleIndex]['enable'])
			{
				$this->LOGGER->log_debug('Module '.$moduleName.' is enable', 'ModuleHandler::getModuleStatus');
				return 1;
			} 
			else
			{
				$this->LOGGER->log_debug('Module '.$moduleName.' is disable', 'ModuleHandler::getModuleStatus');
				return 0;
			} 
		}
		else 
		{
			$this->LOGGER->log_info('Module '.$moduleName.' not found', 'ModuleHandler::getModuleStatus');
			return -1;
		}
	}
	
	/**
	 * 
	 */
	public function setModuleStatus($moduleName, $isEnable)
	{
		$this->LOGGER->log_debug('Function called w/ module name "'.$moduleName.'"', 'ModuleHandler::setModuleStatus');
		if(($moduleIndex = $this->isInModuleList($moduleName)) != -1)
		{
			$this -> moduleList[$moduleIndex]['enable'] = $isEnable;
			$this->LOGGER->log_debug('Module '.$moduleName.' '.($isEnable?'enabled':'disabled'), 'ModuleHandler::setModuleStatus');
			return 0;
		}
		else 
		{
			$this->LOGGER->log_info('Module '.$moduleName.' not found', 'ModuleHandler::setModuleStatus');
			return -1;
		}
	}
	
	/**
	 * 
	 */
	public function setIdWithModule($elementId, $moduleName)
	{
		$this->LOGGER->log_debug('Setting id '.$elementId.' with module '.$moduleName.'...', 'ModuleHandler::setIdWithModule');
		if(($moduleIndex = $this->isInModuleList($moduleName)) != -1)
		{
			if(!in_array($elementId, $this -> moduleList[$moduleIndex]['ids']))
				array_push($this -> moduleList[$moduleIndex]['ids'], $elementId);
			
			$this->LOGGER->log_debug('Id '.$elementId.' has been set with module'.$moduleName, 'ModuleHandler::setIdWithModule');
			return 0;
		}
		else 
		{
			$this->LOGGER->log_info('Module '.$moduleName.' not found', 'ModuleHandler::setIdWithModule');
			return -1;
		}
		
	}
	
	/**
	 * 
	 */
	public function getModuleForId($elementId)
	{
		$this->LOGGER->log_debug('Getting module for id '.$elementId, 'ModuleHandler::getModuleForId');
		
		foreach($this->moduleList as $module)
		{
			if(in_array($elementId, $module['ids']))
			{
				$this->LOGGER->log_debug('Id '.$elementId.' is associated with '.$module['name'], 'ModuleHandler::getModuleForId');
				return $module['name'];
			}
		}

		$this->LOGGER->log_debug('Id '.$elementId.' is not associated with any module', 'ModuleHandler::getModuleForId');
		return '';
	}
	
	
	/**
	 * 
	 * @param string $filter Status of the module
	 * @return array
	 */
	public function getModuleList($filter = 'none')
	{
		$result = array();
		switch($filter)
		{
			case 'none':
				$result = $this->moduleList;
				break;
			case 'enable':
				foreach($this->moduleList as $module)
				{
					if($this->getModuleStatus($module['name']) == 1) array_push($result, $module); 
				}
				break;
			case 'disable':
				foreach($this->moduleList as $module)
				{
					if($this->getModuleStatus($module['name']) == 0) array_push($result, $module); 
				}
				break;
			default:
				$result = null;
				break;
		}
		
		return $result;
	}
	
	/**
	 * String representation of the ModuleHandler
	 * @return string ModuleHandler representation
	 */
	public function __toString()
	{
		$return = '{ moduleDir = '.$this->moduleDir.' | moduleList = ';
		
		if(is_array($this->moduleList))
		{
			foreach ($this->moduleList as $module) {
				$return .= $module['name'].'('.$module['enable'].')';
				
				if(end($this->moduleList)!=$module) $return.=', ';
			}
		}
		else {
			$return.='#error#';
		}
		
		$return .= ' }';
		
		return $return;
	}
}



?>