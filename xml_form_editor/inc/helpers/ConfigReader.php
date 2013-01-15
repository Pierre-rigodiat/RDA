<?php
/**
 * 
 * Reads
 * 	*.ini
 * 	*.xml
 * 
 */

// TODO implement this function and use it in XsdDisplay class
// xxx Use it to load every parameter of the website
class ConfigReader
{
	private $configFile;
	private $paremeterList;
	
	public function __construct()
	{
		/* Not yet implemented */
	}
	
	public function getParameter($paramName)
	{
		/* Not yet implemented */
	}
	
	private function parseFile()
	{
		/* Not yet implemented */
	}
	
	private function parseIniFile()
	{
		/* Not yet implemented */
	}
	
	private function parseXmlFile()
	{
		/* Not yet implemented */
		
		// Parsing the xml file containing the menu
		/*$_SESSION['config']['menu'] = array();
		$xmlDoc = new DOMDocument();
		$xmlDoc->load($_SESSION['config']['menu_desc']);
		
		$xmlDocSectionNodeList = $xmlDoc->getElementsByTagName('sectionName');
		foreach($xmlDocSectionNodeList as $section)
		{
			array_push($_SESSION['config']['menu'], $section->nodeValue);
			
			$xmlDocSectionMenuNodeList = $section->getElementsByTagName('sectionMenu');
			
			foreach($xmlDocSectionMenuNodeList as $sectionMenu)
			{
				
			}
		}*/
	}
}


?>