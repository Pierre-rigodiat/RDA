<?php
	define("DEBUG", false);
	define("CACHED", false);
		
	define("DOCUMENT_TITLE", "Form Generator");
	define("DOCUMENT_VERSION", "0.1a");
	
	define("_ROOT_", dirname(dirname(dirname(__FILE__))));
	/*set_include_path(get_include_path() . PATH_SEPARATOR . _ROOT_);*/
	echo 'Root folder: ' . _ROOT_ . '<br/>';

?>