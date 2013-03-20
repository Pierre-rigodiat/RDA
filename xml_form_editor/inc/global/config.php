<?php
	// todo add the display config

	define("DEBUG", false);
	define("LOG_LEVEL", "notice"); // Log level: {notice, debug, info, warn, error} // TODO Implement it
	
	define("CACHED", false); // todo implement it
		
	define("PROJECT_NAME", "Material Genome Initiative");
	
	define("TOOL_NAME", "XML Form Editor");
	define("TOOL_TITLE", "Form Generator");
	define("TOOL_VERSION", "0.4a");
	define("TOOL_RELEASE_DATE", ""); // xxx unused...
	
	define("_ROOT_", dirname(dirname(dirname(__FILE__)))); // todo only use the session variable
	$_SESSION['config']['_ROOT_'] = _ROOT_;
	
	$_SESSION['config']['_XSDFOLDER_'] = $_SESSION['config']['_ROOT_'].'/resources/files/schemas';
	
	//todo configuration of the pages
	//todo log configuration
?>