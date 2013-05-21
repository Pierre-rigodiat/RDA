<?php
	/* Starting point of the app */
	session_start();
	require_once 'app/init.app.php';
	require_once 'app/core/Website.php';
	require_once 'app/view/Display.php';
	
	$website = new Website();
	$wDisplay = new Display($website);
?>
<!DOCTYPE html>
<html>
<head>
	<?php
		// Write meta
		// Write title
		// Load CSS
	?>
</head>
<body>
	<?php
		// Write menus
		
		// Write content
	
		// Write JS libs
		// Put controllers
	?>
</body>
</html>