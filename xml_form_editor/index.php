<?php 
	session_start();
	require_once 'inc/global/config.php';
	
	// todo load the parser here
	// TODO Organize all the imports
	// TODO Reduce code generation if debug is disabled
	
	if(DEBUG) $startTime = (float) array_sum(explode(' ',microtime()));
?>
<!DOCTYPE html>
<html>
<head>	
	<script>
		var startTime = (new Date()).getTime();
		var registerFormLibLoaded = false,
			schemaConfLibLoaded = false;
		
	</script>
	
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<meta name="description" content="" />
	<meta name="keywords" content="" />
	<meta name="author" content="" />
	
	<!-- Twitter bootstrap -->
	<!-- TODO Use a smaller version of the lib -->
	<link href="resources/css/lib/bootstrap.min.css" rel="stylesheet" media="screen">
	<!--link href="resources/css/lib/bootstrap-responsive.min.css" rel="stylesheet" media="screen"-->
	
	<!-- JQuery UI -->
	<link rel="stylesheet" type="text/css" href="resources/css/lib/jquery-ui-1.10.1.custom.min.css" />
	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css"	media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/xml_display.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	
	<link rel="stylesheet" href="resources/css/dialog.css" />
	
	
	<!-- TODO Put all JS calls at the end of the body tag -->
	<script type="text/javascript" src="inc/controllers/js/xml_display.js"></script>
	<script type="text/javascript" src="inc/controllers/js/php.js"></script>
	
	
	<!-- JQuery & JQuery UI -->
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"></script>
	<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.10.2/themes/smoothness/jquery-ui.css" />
	
	
	<script type="text/javascript" src="inc/controllers/js/pageLoader.js"></script>
	<!--script type="text/javascript" src='resources/js/message.js'></script-->
	
	<title><?php echo TOOL_TITLE.' '.TOOL_VERSION; ?></title>
</head>
<body id="top">
	<div id="header-wrapper">
		<div id="header-wrapper-2">
			<div class="center-wrapper">
				<div id="header">
					<?php 
						require_once 'inc/skeleton/header/logo.php';
						//require_once 'inc/skeleton/header/menu.php';
					?>
				</div>

			</div>
		</div>
	</div>

	<div id="navigation-wrapper">
		<div id="navigation-wrapper-2">
			<div class="center-wrapper">
				<div id="navigation">
					<?php require_once 'inc/skeleton/menu/main_menu.php' ?>
					<div class="clearer">&nbsp;</div>
				</div>
			</div>
		</div>
	</div>
	<div id="subnav-wrapper">
		<div id="subnav-wrapper-2">
			<div class="center-wrapper">
				<div id="subnav">
					<?php require_once 'inc/skeleton/menu/sub_menu.php'; ?>
					<div class="clearer">&nbsp;</div>
				</div>
			</div>
		</div>
	</div>
	
	<div id="content-wrapper">
		<?php 
			if(DEBUG)
			{
		?>
		<div class="debug-wrapper">
			<div class="debug-panel">
				<?php require_once 'inc/skeleton/debug/info.php'; ?>
			</div>
			<div class="debug-panel">
				<?php require_once 'inc/skeleton/debug/console.php'; ?>
			</div>
		</div>
		<?php 
			}
		?>

		<div class="center-wrapper">
			<div class="content">
				<div id="main">
					<div class="clearer">&nbsp;</div>
				</div>
			</div>
		</div>
	</div>

	<div id="footer-wrapper">
		<div class="center-wrapper">
			<div id="footer">
				<?php 
					require_once 'inc/skeleton/footer/left.php';
					require_once 'inc/skeleton/footer/right.php';
				?>
				<div class="clearer">&nbsp;</div>
			</div>
		</div>
	</div>

	<?php 
		if(DEBUG)
		{
			$endTime = (float) array_sum(explode(' ',microtime()));
	
			echo '<input type="hidden" id="php_exec_time" value="'.round(($endTime-$startTime)*1000).'"/>';
			echo '<input type="hidden" id="php_mem" value="'.memory_get_usage().'"/>';
			echo '<input type="hidden" id="php_mem_peak" value="'.memory_get_peak_usage().'"/>';
		}
	?>
	
	<script src="resources/js/bootstrap.min.js"></script>
</body>
</html>
