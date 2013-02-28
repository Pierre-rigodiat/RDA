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
		var registerFormLibLoaded = false;
	</script>
	
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<meta name="description" content="" />
	<meta name="keywords" content="" />
	<meta name="author" content="" />
	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css"	media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/xml_display.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	
	<script type="text/javascript" src="resources/js/xml_display.js"></script>
	<script type="text/javascript" src="resources/js.new/php.js"></script>
	
	<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css" />

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js"></script>
	<script type="text/javascript" src="resources/js.new/pageLoader.js"></script>
	
	<script type="text/javascript" src='resources/js/message.js'></script>
	
	<link rel="stylesheet" href="resources/css/dialog.css" />
	
	<script>
		$(window).load(function () {
			var unitArray = new Array("B", "kB", "MB", "GB");
			var unitArrayIndex = 0;
			   
	       	var endTime = (new Date()).getTime();
	      	var msLoadJS = endTime - startTime;

	       	var msLoadPHP = $('#php_exec_time').attr('value');

			var memPHP = $('#php_mem').attr('value');  
			while(memPHP>1024 && unitArrayIndex<unitArray.length)
			{
				memPHP = memPHP / 1024;
				unitArrayIndex += 1;
			}

			memPHP = Math.round(memPHP*100)/100;
			memPHP = memPHP + ' ' + unitArray[unitArrayIndex];
			

			unitArrayIndex = 0;
			
	       	var memPHPPeak = $('#php_mem_peak').attr('value');
	       	while(memPHPPeak>1024 && unitArrayIndex<unitArray.length)
			{
	       		memPHPPeak = memPHPPeak / 1024;
				unitArrayIndex += 1;
			}

	       	memPHPPeak = Math.round(memPHPPeak*100)/100;
	       	memPHPPeak = memPHPPeak + ' ' + unitArray[unitArrayIndex];
	
	       	$('#exec_time').html("<u>Execution time:</u> <b>"+msLoadJS+" ms (JS) / "+msLoadPHP+" ms (PHP)</b>");
	       	$('#php_mem_debug').html("<u>PHP Memory:</u> <b>"+memPHP+" (peak: "+memPHPPeak+")</b>");
   		});
	</script>
	
	<title><?php echo TOOL_TITLE.' '.TOOL_VERSION; ?></title>
</head>
<body id="top">
	<div id="header-wrapper">
		<div id="header-wrapper-2">
			<div class="center-wrapper">
				<div id="header">
					<?php 
						require_once 'inc/skeleton/header/logo.php';
						require_once 'inc/skeleton/header/menu.php';
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
	<div id="invisible_message"></div>
</body>
</html>
