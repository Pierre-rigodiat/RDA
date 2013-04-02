<?php
/**
 * 
 */
require_once /**$_SESSION[]**/'../app/core/Menu.php';
/**
 * 
 * 
 * 
 */
class Website {
	
	private $menu;
	private $currentUrl;
	
	public function __construct() {
		
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc)
		{
			case 0:
				$this -> currentUrl = $_SERVER['PHP_SELF'];
					
				$this -> menu = new Menu($this -> currentUrl);
				
				break;
			default;
				// TODO log that
				throw new Exception("Invalid number of parameter", -1);
				break;
		}
		
	}
	
	
	public function getMenu()
	{
		return $this -> menu;
	}
}
