<?php
/**
 * <Display class>
 */
require_once '../app/core/Website.php';
/**
 * 
 * 
 * 
 */
class Display {
	/**
	 * 
	 * @var \App\Core\Website
	 */
	private $website;
	
	
	public function __construct() {
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc)
		{
			case 1:
				// TODO Control type and everything
				$this -> website = $argv[0];
									
				break;
			default;
				// TODO log that
				throw new Exception("Invalid number of parameter", -1);
				break;
		}
	}
	
	/* TODO functions to write:
	 * 	public displayHead
	 * 		private displayMeta
	 * 		private displayCss
	 *
	 * 
	 * 
	 */
	
	public function displayMenu()
	{
		$menu = $this -> website -> getMenu();
	}
}
