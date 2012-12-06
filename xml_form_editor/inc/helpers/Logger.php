<?php 
/**
 * ** Class Logger v1.0c **
 * 
 * CHANGELOG
 * **1.0b**
 * Add IP address
 * Change element order
 * **1.0c**
 * Caller is now a parameter of the constructor
 * Function name is now the second parameter of the log function
 * 
 * 
 * Released on 10-11-19
 * (c) P. Dessauw 2012
 */
class Logger
{
	private static $LOG_LEVELS = array('notice', 'debug', 'info', 'warning', 'error');
	
	private $logLevel;
	private $logFile;
	private $caller;
	
	/**
	 * Logger constructor. Take the level and the name of the file as parameters.
	 * Levels are (log registration decreasing):
	 * 	- notice,
	 * 	- debug,
	 * 	- info,
	 * 	- warning,
	 * 	- error.
	 * 
	 * @example $logger = new Logger('warning', 'path/to/file.log', 'callerFileName.php');
	 */
	public function __construct()
	{
		$argc = func_num_args();
		$argv = func_get_args();
		
		if($argc==3)
		{
			
			
			if(is_string($argv[0]) && is_string($argv[1]) && is_string($argv[2]))
			{
				$level = func_get_arg(0);
				$file = func_get_arg(1);
				$caller = func_get_arg(2);
				
				if(in_array($level, self::$LOG_LEVELS))
				{
						$this->logLevel = $level;
						$this->logFile = $file;
						$this->caller = $caller;
						
						$this->log_notice('Logger instantiation OK (level:'.$this->logLevel.', file:'.$this->logFile.')', 'Logger::__construct');
						
						return;
					
				}
				else
					throw new Exception("[Logger::__construct] Level '".$level."' is not a valid log level");
			}
			else
				throw new Exception('[Logger::__construct] Arguments must be {string, string, string} ({'.gettype($argv[0]).','.gettype($argv[1]).','.gettype($argv[2]).'} given)');
		}
		else
			throw new Exception("[Logger::__construct] 3 arguments must be entered (".$argc." given) ");
	}
	
	/**
	 * Log a message into the specified file. If the log level is incorrect or the file cannot be opened, an exception is thrown.
	 * 
	 * 
	 * @param $level refers to self::$LOG_LEVELS
	 * @param $message is the message to write
	 * @param $function name of the function calling the logger
	 * 
	 * @return NULL
	 */
	public function log($level, $message, $function)
	{
		if(in_array($level, self::$LOG_LEVELS))
		{
			$current_level_key = array_search($level, self::$LOG_LEVELS);
			$default_level_key = array_search($this->logLevel, self::$LOG_LEVELS);
			
			if($current_level_key>=$default_level_key)
			{
				$fp = fopen($this->logFile, 'a');
				
				if($fp!=null)
				{
					$date = date('m-d-Y H:i:s');
					$logString = null;
					
					if(gettype($message)=='string' && gettype($function)=='string')
					{
						$logString = '['.$date.']['.$_SERVER['REMOTE_ADDR'].']['.$this->caller.']['.$level.']['.$function.'] '.$message.PHP_EOL;
					}
					else 
					{
						$logString = '['.$date.']['.$_SERVER['REMOTE_ADDR'].'][error] ### LOG FORMAT ERROR ###'.PHP_EOL;
					}
					
					fwrite($fp, $logString);
					fclose($fp);
				}
				else
					throw new Exception("[Logger::log] Unable to open the log file ".$this->logFile);
			}
			
		}
		else
			throw new Exception("[Logger::log] Level '".$this->logLevel."' is not a valid log level");		
	}
	
	/**
	 * Log a notice message.
	 * 
	 * @param $message is the message to write
	 * @param $function name of the function calling the logger
	 * 
	 * @return NULL
	 */
	public function log_notice($message, $function)
	{
		$this->log('notice', $message, $function);
	}
	
	/**
	 * Log a debug message.
	 * 
	 * @param $message is the message to write
	 * @param $function name of the function calling the logger
	 * 
	 * @return NULL
	 */
	public function log_debug($message, $function)
	{
		$this->log('debug', $message, $function);
	}
	
	/**
	 * Log an informative message.
	 * 
	 * @param $message is the message to write
	 * @param $function name of the function calling the logger
	 * 
	 * @return NULL
	 */
	public function log_info($message, $function)
	{
		$this->log('info', $message, $function);
	}
	
	/**
	 * Log a warning message.
	 * 
	 * @param $message is the message to write
	 * @param $function name of the function calling the logger
	 * 
	 * @return NULL
	 */
	public function log_warning($message, $function)
	{
		$this->log('warning', $message, $function);
	}
	
	/**
	 * Log an error message.
	 * 
	 * @param $message is the message to write
	 * @param $function name of the function calling the logger
	 * 
	 * @return NULL
	 */
	public function log_error($message, $function)
	{
		$this->log('error', $message, $function);
	}
}
?>