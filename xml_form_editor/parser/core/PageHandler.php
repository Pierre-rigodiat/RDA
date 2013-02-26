<?php
/**
 * 
 */
class PageHandler
{
	private $numberOfPage;
	private $currentPage;
	private $pageArray; // An array linking page number with a Tree of XSD element
	
	// Debug and logging variables
	private $LOGGER;
	private static $LEVELS = array(
		'DEV' => 'notice',
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	private static $LOG_FILE;
	private static $FILE_NAME = 'PageHandler.php';
	
	/**
	 * 
	 * @param $numberOfPages {integer}
	 * @param $isDebugEnable {boolean} Optional 
	 */
	public function __construct() {
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['logs_dirname'].'/'.$_SESSION['xsd_parser']['conf']['log_file'];

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 1 :
				// new PageHandler(numberOfPage)
				if (is_int($argv[0]) && $argv[0] > 0)
				{
					$this -> numberOfPage = $argv[0];
					$this -> currentPage = 1;
					
					// Creation of the page array structure
					$this -> pageArray = array();
					for($i=0; $i < $this->numberOfPage; $i++)
						$this -> pageArray[$i] = array();
					
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
				// new PageHandler(numberOfPage, debugBoolean)
				if (is_int($argv[0]) && $argv[0] > 0 && is_bool($argv[1]))
				{
					$this -> numberOfPage = $argv[0];
					$this -> currentPage = 1;

					// Creation of the page array structure
					$this -> pageArray = array();
					for($i=0; $i < $this->numberOfPage; $i++)
						$this -> pageArray[$i] = array();

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
				// TODO Complete log message differentiating if integer is >0 or not
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
	
	public function setPageForId($pageNumber, $elementId)
	{
		//$this -> LOGGER -> log_debug('Setting page for ID ...', 'PageHandler::setPageForId');
		
		if(isset($this->pageArray[$pageNumber-1]))
		{
			array_push($this->pageArray[$pageNumber-1], $elementId);
			$this -> LOGGER -> log_debug('ID '.$elementId.' set to page '.($pageNumber-1), 'PageHandler::setPageForId');
		}
		else 
			$this -> LOGGER -> log_error('Page '.$pageNumber.' does not exist', 'PageHandler::setPageForId');
	}
	
	public function removePageForId($pageNumber, $elementId)
	{
		$this -> pageArray[$pageNumber-1] = array_diff($this -> pageArray[$pageNumber-1], array($elementId));
		$this -> pageArray[$pageNumber-1] = array_values($this -> pageArray[$pageNumber-1]);
		
		$this -> LOGGER -> log_debug('Page '.$pageNumber.' removed for ID '.$elementId, 'PageHandler::removePageForId');
	}
	
	public function removePagesForId($elementId)
	{
		$this -> LOGGER -> log_debug('Removing pages for ID '.$elementId.'...', 'PageHandler::removePagesForId');
		
		for ($i=1; $i<=$this->numberOfPage; $i++) 
		{
			$this -> removePageForId($i, $elementId);
		}
		
		$this -> LOGGER -> log_debug('Pages removed for ID '.$elementId, 'PageHandler::removePagesForId');
	}
	
	/**
	 * 
	 */
	public function getIdsForPage($pageNumber)
	{
		
	}
	
	
	
	/**
	 * 
	 */
	public function getPageForId($elementId)
	{
		$this -> LOGGER -> log_debug('Getting pages for ID '.$elementId.'...', 'PageHandler::getPageForId');
		
		$pageArray = array();
		
		foreach ($this->pageArray as $pageNumber => $elementArray) {
			if(in_array($elementId, $elementArray))
			{
				$this -> LOGGER -> log_debug('Page '.($pageNumber+1).' contains ID '.$elementId, 'PageHandler::getPageForId');
				array_push($pageArray, $pageNumber+1);
			}
		}
		
		$this -> LOGGER -> log_debug('Pages got for ID '.$elementId, 'PageHandler::getPageForId');
		
		return $pageArray;
	}
	
	/**
	 * 
	 */
	public function setCurrentPage($newCurrentPage)
	{
		if(is_int($newCurrentPage) && $newCurrentPage > 0 && $newCurrentPage <= $this -> numberOfPage)
		{
			$this -> currentPage = $newCurrentPage;
			$this -> LOGGER -> log_debug('$currentPage set to '.$newCurrentPage, 'PageHandler::setCurrentPage');
		}
		else if(!is_int($newCurrentPage))
			$this -> LOGGER -> log_error('$newCurrentPage is not an integer', 'PageHandler::setCurrentPage');
		else
			$this -> LOGGER -> log_error('Invalid range for $newCurrentPage ($newCurrentPage = '.$newCurrentPage.', $numberOfPage = '.$this->numberOfPage.')', 'PageHandler::setCurrentPage');
	}
	
	public function getCurrentPage()
	{
		$this -> LOGGER -> log_notice('Function called', 'PageHandler::getCurrentPage');
		return $this -> currentPage;
	}
	
	public function getNumberOfPage()
	{
		return $this->numberOfPage;
	}
	
	public function __toString()
	{
		$pageHandlerString = '';
		
		foreach ($this -> pageArray as $pageNumber => $arrayOfElement) {
			$pageHandlerString .= 'Page '.($pageNumber+1).' {';
			
			foreach ($arrayOfElement as $elementId) {
				$pageHandlerString .= $elementId;
				
				if(end($arrayOfElement) != $elementId) $pageHandlerString.=', ';
			}
			
			$pageHandlerString .= '}';
			
			if(count($this -> pageArray)!=$pageNumber+1) $pageHandlerString .= ' | ';
		}
		
		return $pageHandlerString;
	}
}


?>