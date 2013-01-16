<?php
/**
 * 
 */
class PageHandler
{
	private $numberOfPage;
	private $pageArray; // An array linking page number with ID of XSD element
	// private $moduleHandler;
	// private $tree;
	// private static $modulePerPages = 1;
	
	// Debug and logging variables
	private $LOGGER;
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	private static $LOG_FILE;
	private static $FILE_NAME = 'PageHandler.php';
	
	/**
	 * 
	 * @param $tree {object}
	 * @param $moduleHandler {object}
	 * @param $numberOfPages {integer}
	 * @param $isDebugEnable {boolean} Optional 
	 */
	public function __construct() {
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'] . '/logs/page_handler.log';

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 1 :
				// new XsdDisplay(numberOfPage)
				if (is_int($argv[0]))
				{
					$this -> numberOfPage = $argv[0];
					$this -> pageArray = array();
					
					$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> numberOfPage = -1;
					$this -> pageArray = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			case 2 :
				// new XsdDisplay(numberOfPage, debugBoolean)
				if (is_int($argv[0]) && is_bool($argv[1]))
				{
					$this -> numberOfPage = $argv[0];
					$this -> pageArray = array();

					if ($argv[1])
						$level = self::$LEVELS['DBG'];
					else
						$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> numberOfPage = -1;
					$this -> pageArray = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default :
				$this -> numberOfPage = -1;
				$this -> pageArray = null;
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

		if ($this -> numberOfPage == -1 && $this -> pageArray == null)
		{
			$log_mess = '';

			switch($argc)
			{
				case 1 :								
					$log_mess .= 'Supports {integer} as parameter ({' . gettype($argv[0]) . '} given)';
					break;
				case 2 :					
					$log_mess .= 'Supports {integer,boolean} as parameters ({' . gettype($argv[0]) . ',' . gettype($argv[1]) . '} given)';
					break;
				default :
					$log_mess .= 'Supports 1 or 2 parameters at input (' . $argc . 'given)';
					break;
			}

			$this -> LOGGER -> log_error($log_mess, 'PageHandler::__construct');
		}
		else
			$this -> LOGGER -> log_debug('PageHandler built ('.$this->numberOfPage.' page(s))', 'PageHandler::__construct');
	}

	/*public function setModuleForPage($moduleName, $pageNumber)
	{
		
	}*/
	
	public function setIdForPage($elementId, $pageNumber)
	{
		//$this->
	}
	
	public function getIdForPage($pageNumber)
	{
		
	}
	
	public function getPageForId($elementId)
	{
		
	}
	
	public function getNumberOfPage()
	{
		return $this->numberOfPage;
	}
	
	public function __toString()
	{
		// TODO Implement it
		return null;
	}
}


?>