<?php 
	session_start();
	require_once 'inc/global/config.php';
	
	if(DEBUG) $startTime = (float) array_sum(explode(' ',microtime()));
?>
<!DOCTYPE html>
<html>
<head>
	<?php 
		// TODO Organize all the imports
		// TODO Reduce code generation if debug is disabled
	?>
	
	<script>
		var startTime = (new Date()).getTime();
	</script>
	
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<meta name="description" content="" />
	<meta name="keywords" content="" />
	<meta name="author" content="" />
	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/add.css"	media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/xml_display.css" media="screen" />
	
	<script type="text/javascript" src="resources/js/xml_display.js"></script>
	
	<!-- script src="http://code.jquery.com/jquery-latest.js"></script-->
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
	<script src="resources/js/util.js"></script>
	<script src="resources/js/step3.js"></script>
	<script src="resources/js/step2.js"></script>
	<script src="resources/js/step1.js"></script>
	<script src="resources/js/upload.js"></script>
	<script src="resources/js/actionHandler.js"></script>
	<script src="resources/js/schemaConfig.js"></script>
	
	<script type="text/javascript" src='resources/js/message.js'></script>
	<link rel="stylesheet" type="text/css" href="resources/css/themes/message_growl_shiny.css" />
	
	<script src="resources/js/popup.js"></script>
	<link rel="stylesheet" href="resources/css/popup.css" />
	
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
	<?php
		// TODO Work on all those requires
		require_once 'inc/lib/StringFunctions.php';
	
		require_once 'inc/classes/XsdParser.php';
	
		require_once 'inc/global/images.php'; // XXX Regroup in the head.php file
	?>
	
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

	<?php 
		// FIXME Condition not good
		/*if(isset($_GET['menu']) && $_GET['menu']=='full')
		{*/
	?>
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
	<?php 
		//}
	?>

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
					<?php 
						require_once 'inc/skeleton/message.php';
	
						// TODO Build a function loadContent($getParam, $rule) or smth
						$file = 'public/home.php';
						
						if(isset($_GET['p']))
						{	
							switch($_GET['p'])
							{
								case 'admin':
									if(isset($_GET['sp']) && $_GET['sp']=='schemas') $file = 'xsd_cfg.inc.php';
									else $file = 'other/wip.php';
									break;
								default:
									break;
							}
						}
	
						if(isset($_GET['step']))
						{
							switch($_GET['step'])
							{
								case '1':
									$file = 'step1.php';
									break;
								case '10':
									$file = 'demo/step1.php';
									break;
								case '2':
									$file = 'step2.php';
									break;
								case '20':
									$file = 'demo/step2.php';
									break;
								case '3':
									$file = 'step3.php';
									break;
								case '4':
									$file = 'step4.php';
									break;
								case '40':
									$file = 'demo/step3.php';
									break;
								case 'debug':
									$file = 'debug.php';
									break;
								default:
									break;
							}
						}
	
						require_once 'inc/skeleton/main/'.$file;
					?>

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