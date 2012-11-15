<?php 
	/**
	 * ** Class Logger v1.0 **
	 * 
	 * Released on 10-11-12
	 * (c) P. Dessauw 2012
	 */
	// TODO move it into the helper folder
	class Logger
	{
		private static $LOG_LEVELS = array('notice', 'debug', 'info', 'warning', 'error');
		
		private $logLevel;
		private $logFile;
		
		/**
		 * Logger constructor. Take the level and the name of the file as parameters.
		 * Levels are (log registration decreasing):
		 * 	- notice,
		 * 	- debug,
		 * 	- info,
		 * 	- warning,
		 * 	- error.
		 * 
		 * @example $logger = new Logger('warning', 'path/to/file.log');
		 */
		public function __construct()
		{
			if(func_num_args()==2)
			{
				$level = func_get_arg(0);
				$file = func_get_arg(1);
				
				if(in_array($level, self::$LOG_LEVELS))
				{
					
						$this->logLevel = $level;
						$this->logFile = $file;
						
						$this->log_notice('Logger instantiation OK', basename(__FILE__));
						
						return;
					
				}
				else
					throw new Exception("[Logger::__construct] Level '".$level."' is not a valid log level");
			}
			else
				throw new Exception("[Logger::__construct] Invalid number of argument");
		}
		
		/**
		 * Log a message into the specified file. If the log level is incorrect or the file cannot be opened, an exception is thrown.
		 * 
		 * 
		 * @param $level refers to self::$LOG_LEVELS
		 * @param $message is the message to write
		 * @param $fileName name of the caller
		 * 
		 * @return NULL
		 */
		public function log($level, $message, $fileName)
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
						
						if(gettype($message)=='string' && gettype($fileName)=='string')
						{
							$logString = '['.$date.']['.$level.']['.$fileName.'] '.$message.PHP_EOL;
						}
						else 
						{
							$logString = '['.$date.'][error] ### LOG FORMAT ERROR ###'.PHP_EOL;
						}
						
						fwrite($fp, $logString);
						fclose($fp);
					}
					else
						throw new Exception("[Logger::log] Unable to open the log file ".$file);
				}
				
			}	
			else
				throw new Exception("[Logger::log] Level '".$level."' is not a valid log level");		
		}
		
		/**
		 * Log a notice message.
		 * 
		 * @param $message is the message to write
		 * @param $fileName name of the caller
		 * 
		 * @return NULL
		 */
		public function log_notice($message, $fileName)
		{
			$this->log('notice', $message, $fileName);
		}
		
		/**
		 * Log a debug message.
		 * 
		 * @param $message is the message to write
		 * @param $fileName name of the caller
		 * 
		 * @return NULL
		 */
		public function log_debug($message, $fileName)
		{
			$this->log('debug', $message, $fileName);
		}
		
		/**
		 * Log an informative message.
		 * 
		 * @param $message is the message to write
		 * @param $fileName name of the caller
		 * 
		 * @return NULL
		 */
		public function log_info($message, $fileName)
		{
			$this->log('info', $message, $fileName);
		}
		
		/**
		 * Log a warning message.
		 * 
		 * @param $message is the message to write
		 * @param $fileName name of the caller
		 * 
		 * @return NULL
		 */
		public function log_warning($message, $fileName)
		{
			$this->log('warning', $message, $fileName);
		}
		
		/**
		 * Log an error message.
		 * 
		 * @param $message is the message to write
		 * @param $fileName name of the caller
		 * 
		 * @return NULL
		 */
		public function log_error($message, $fileName)
		{
			$this->log('error', $message, $fileName);
		}
	}
?>