<?php
/**
 * 
 * 
 * @package Plugins\Table\Core
 */ 
class TableModule {
	/**
	 * Global variables (used in every plugin)
	 */
	private $tree; // Elements used in the plugin
	private static $referenceTree = null;
	private $dataArray; 
	
	/**
	 * Local variables
	 */
	private $files; // The file used to store the table
	
	// Logging variables
	private $LOGGER;
	private static $LEVELS = array(
		'DBG' => 'notice',
		'NO_DBG' => 'info'
	);
	private static $LOG_FILE;
	private static $FILE_NAME = 'TableModule.php';
	
	/**
	 * 
	 */
	public function __construct() {
		self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['logs_dirname'].'/module.log';

		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 1 :
				// new TableModule(tree)
				if (is_object($argv[0]) && get_class($argv[0]) == 'Tree')
				{
					$this -> tree = $argv[0];
					$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> tree = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			case 2 :
				// new TableModule(tree, debugBoolean)
				if (is_object($argv[0]) && get_class($argv[0]) == 'Tree' && is_bool($argv[1]))
				{
					$this -> tree = $argv[0];
					
					if ($argv[1])
						$level = self::$LEVELS['DBG'];
					else
						$level = self::$LEVELS['NO_DBG'];
				}
				else
				{
					$this -> tree = null;
					$level = self::$LEVELS['NO_DBG'];
				}
				break;
			default :
				$this -> tree = null;
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

		if ($this -> tree == null)
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

			$this -> LOGGER -> log_error($log_mess, 'TableModule::__construct');
		}
		else
		{
			// TODO Compare the tree object to the expected one
			if($this->isValid())
			{
				$this -> LOGGER -> log_debug('Table module successfully built', 'TableModule::__construct');
				$this -> files = array();
				$this -> dataArray = array();
			}
			else 
			{
				$this -> tree = null;
				$this -> LOGGER -> log_debug('Table module successfully built', 'TableModule::__construct');
			}
		}
	}
	
	/**
	 * Check if the tree is valid regarding the configuration of the plugin
	 */
	// FIXME Use the Module abstract class
	private function isValid()
	{
		return true;
	}
	
	
	public function addFile($fileName)
	{
		// TODO Check if the fileName really exists
		array_push($this->files, $fileName);
	}
	
	/**
	 * Remove the file and
	 */
	public function removeFile($fileId)
	{
		// TODO Check that the ID is in the array
		// TODO Delete the file on the server
		
		// Delete the file
		unset($this -> files[$fileId]);
		$this -> files = array_values($this -> files);
		
		// Delete the data
		$elementId = $this -> tree -> getObject(0); // FIXME Tree not treated as we wanted
		unset($this -> dataArray[$elementId][$fileId]);
		$this -> dataArray[$elementId] = array_values($this -> dataArray[$elementId]);
	}
	
	public function parseFile($fileName)
	{
		$this -> LOGGER -> log_debug('Parsing '.$fileName.'...', 'TableModule::parseFile');
		
		// TODO Change to a configuration variable
		$pythonExec = '"C:/Program Files (x86)/Python/273/python.exe"';
		
		// TODO Check if we cannot create a most practical session value
		$pythonFile = $_SESSION['xsd_parser']['conf']['modules_dirname'].'/table/controllers/python/excelToHDF5.py';
		
		$excelFile = $_SESSION['xsd_parser']['conf']['dirname'].'/resources/files/tables/'.$fileName; // todo test if the file exists (if not it returns an error)
		$output = array();
		
		exec($pythonExec.' '.$pythonFile.' "'.$excelFile.'"', $output, $ret_val);
		
		if($ret_val == 0) // No errors
		{
			$this -> LOGGER -> log_debug($fileName.' parsed. Retrieving table structure...', 'TableModule::parseFile');
			
			$table = "";
			foreach($output as $print_element)
			{
				$table.=/*htmlspecialchars(*/$print_element/*)*/;
			}
			
			$this -> LOGGER -> log_debug('Data set = [[['.$table.']]]', 'TableModule::parseFile');
			
			// FIXME Add data differently into the array
			$elementId = $this -> tree -> getObject(0);
			//$currentData = '';
			
			if(!isset($this -> dataArray[$elementId])) $this -> dataArray[$elementId] = array();
			
			array_push($this -> dataArray[$elementId], $table);
			
			//$currentData .= $table;
			//array_push($this -> dataArray[$elementId], $table);
			
			//$this -> dataArray[$elementId] = $currentData;
			
			$this -> LOGGER -> log_debug('Data inserted for element '.$elementId, 'TableModule::parseFile');
		}
		else
		{
			$this -> LOGGER -> log_error($fileName.' returned an error: '.$ret_val, 'TableModule::parseFile');
		}
		
		return $ret_val;
	}
	
	/**
	 * 
	 */
	public function getFiles()
	{
		return $this->files;
	}
	
	/**
	 * 
	 */
	public function getXmlData()
	{		
		// FIXME The way to retrieve xml is should be changed
		$elementId = $this -> tree -> getObject(0);
		$xmlData = '';
		
		$this -> LOGGER -> log_debug('Retrieving data for element '.$elementId, 'TableModule::getXmlData');
		
		if(isset($this -> dataArray[$elementId]))
		{
			foreach($this -> dataArray[$elementId] as $table)
			{
				$this -> LOGGER -> log_notice('New table found', 'TableModule::getXmlData');
				$xmlData .= $table;
				$this -> LOGGER -> log_debug('Data set: '.$table, 'TableModule::getXmlData');
				$this -> LOGGER -> log_notice('Table added', 'TableModule::getXmlData');
			}
		}
		
		
		$xmlDataArray = array($elementId => $xmlData);
		return $xmlDataArray;
	}
	
}


?>