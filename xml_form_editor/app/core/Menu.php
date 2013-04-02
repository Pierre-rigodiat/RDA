<?php
/**
 * <Menu class>
 */
/** @ignore */
require_once /*$_SESSION['app']['config']['_ROOT_'].*/'../inc/db/mongodb/MongoDBStream.php';
/**
 * 
 * 
 * 
 */
class Menu {
	/**
	 * 
	 * @var array
	 */
	private $menuStructure;
	
	/**
	 * 
	 * @var array
	 */
	private $menuSelection;
	
	/**
	 * @var array
	 */
	private $sectionInfo;
	
	/**
	 * 
	 * @var string
	 */
	private $pageName;
	
	
	public function __construct() {
		// Initialize the logger (will throw an Exception if any problem occurs)
		/*self::$LOG_FILE = $_SESSION['xsd_parser']['conf']['dirname'].'/logs/closure.log';
		$level = self::$LEVELS['DBG'];
		$this -> LOGGER = new Logger($level, self::$LOG_FILE, self::$FILE_NAME);*/
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc)
		{
			case 1: // new Menu(idSection)
				if(is_string($argv[0]))
				{
															
					if(strpos($argv[0], '/')!==FALSE)
					{
						// We use argv to split into path element
						$argv = explode('/', $argv[0]);
						if(count($argv) > 3)
						{
							throw new Exception("Invalid path parameter");
						}
					}
					
					$this->pageName = $argv[0];
				}
				else
				{
					//TODO Write some error log
					throw new Exception('Invalid type of parameter given to the object');
				}
				
				break;
			default:
				//TODO Error log
				throw new Exception('Invalid number of parameters given to the object');
				break;
		}		
		
		/* Connection to MongoDb */
		try
		{
			$mongoDbStream = new MongoDBStream();
			$mongoDbStream -> setDatabaseName("website");
			$mongoDbStream -> openDB();
			
			$sectionCollection = $mongoDbStream -> getCollection("sections");
		}
		catch(Exception $e)
		{
			throw new Exception('Connection to MongoDb impossible');
		}
		
		$query = array(
			"baseUrl" => $this->pageName
		);
		
		$queryCursor = $sectionCollection -> find($query);
		$resultArray = iterator_to_array($queryCursor);

		
		if(!empty($resultArray))
		{
			$resultArray = array_values($resultArray);
			
			$this -> sectionInfo = $resultArray[0];
			unset($this->sectionInfo["menus"]);
			$this -> menuStructure = $resultArray[0]["menus"];
			
			$pathIndex = 1;
		}
		else
		{
			/* By default we try to get the void baseUrl */
			$query = array(
				"baseUrl" => ''
			);
			
			$queryCursor = $sectionCollection -> find($query);
			$resultArray = iterator_to_array($queryCursor);
			
			if(!empty($resultArray))
			{
				$resultArray = array_values($resultArray);
				
				$this -> sectionInfo = $resultArray[0];
				unset($this->sectionInfo["menus"]);
				$this -> menuStructure = $resultArray[0]["menus"];
				
				$pathIndex = 0;
			}
			else
			{
				throw new Exception('Section name invalid');
			}	
		}
		
		
		
		
		$this -> menuSelection = array(
			"menu" => isset($argv[$pathIndex])?$this -> getMenuId($argv[$pathIndex]):0,
			"submenu" => isset($argv[$pathIndex+1])?$this -> getSubmenuId($argv[$pathIndex+1]):0
		);
	}
	
	public function setSelectedMenu($menuId)
	{
		$this -> menuSelection ["menu"] = $menuId;
	}
	
	public function setSelectedSubmenu($submenuId)
	{
		$this -> menuSelection ["submenu"] = $submenuId;
	}
	
	public function getMenuId($menuName)
	{
		foreach($this -> menuStructure as $menuId => $menu)
		{
			if($menu["url"] == $menuName)
			{
				return $menuId;
			}
		}
	}
	
	public function getSubmenuId($submenuName)
	{
		foreach($this -> menuStructure as $menuId => $menu)
		{
			if(isset($menu["submenus"]))
			{
				foreach ($menu["submenus"] as $submenuId => $submenu) {
					if($submenu["url"] == $submenuName)
					{
						return $submenuId;
					}
				}
			}
			
		}
	}
	
	public function getMenusName()
	{
		$menusName = array();
		if(isset($this -> menuStructure))
		{
			foreach($this -> menuStructure as $menu)
			{
				array_push($menusName, $menu["name"]);
			}
		}
		
		return $menusName;
	}
	
	public function getSubmenusName()
	{
		$submenusName = array();
		$selectedMenu = $this -> menuSelection["menu"];
		if(isset($this -> menuStructure[$selectedMenu]))
		{
			if(isset($this -> menuStructure[$selectedMenu]["submenus"]))
			{
				foreach($this -> menuStructure[$selectedMenu]["submenus"] as $submenu)
				{
					array_push($submenusName, $submenu["name"]);
				}
			}
		}
		
		return $submenusName;
	}
	
	public function getLink($itemName)
	{
		
	}
	
	/**
	 * 
	 * @return string File name
	 */
	public function getPageFileName()
	{
		$menuId = $this -> menuSelection["menu"];
		$submenuId = $this -> menuSelection["submenu"];
		
		if(isset($this->menuStructure[$menuId]["file"]))
		{
			return $this->menuStructure[$menuId]["file"];
		}
		else 
		{
			return $this->menuStructure[$menuId]["submenus"][$submenuId]["file"];
		}
	}
	
	/**
	 * 
	 * @return string Object description
	 */
	public function __toString()
	{
		var_dump($this -> menuSelection);
		var_dump($this -> sectionInfo);
		var_dump($this -> menuStructure);
		return '';
	}
}
