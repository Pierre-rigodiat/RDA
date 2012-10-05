<?php 
session_start();
require_once 'inc/global/config.php';

if(DEBUG)
	$startTime = (float) array_sum(explode(' ',microtime()));
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr">
<head>
	<script>
		var startTime = (new Date()).getTime();
	</script>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<meta name="description" content="" />
	<meta name="keywords" content="" />
	<meta name="author" content="" />
	
	<link rel="stylesheet" type="text/css" href="resources/css/style.css"
		media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/add.css"
		media="screen" />
	<link rel="stylesheet" type="text/css"
		href="resources/css/xml_display.css" media="screen" />
	
	<?php 
	// TODO Organize all the imports
	?>
	
	<script type="text/javascript" src="resources/js/xml_display.js"></script>
	
	<!-- script src="http://code.jquery.com/jquery-latest.js"></script-->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
	<script src="resources/js/util.js"></script>
	<script src="resources/js/step3.js"></script>
	<script src="resources/js/step2.js"></script>
	<script src="resources/js/step1.js"></script>
	
	<script type="text/javascript" src='resources/js/message.js'></script>
	<link rel="stylesheet" type="text/css"
		href="resources/css/themes/message_growl_shiny.css" />
	
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

	require_once 'inc/global/images.php'; // XXX Regroupe in the head.php file
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
	if(isset($_GET['menu']) && $_GET['menu']=='full')
	{
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
	}
	?>

	<div id="content-wrapper">
		<?php 
		if(DEBUG)
		{
			?>
		<div class="debug-wrapper">
			<h2>
				Debug panel
				<!-- img src="resources/img/debug-loader.gif" alt="Loading..."/-->
			</h2>
			<ul>
				<li><?php echo '<u>Root folder:</u> <b>' . _ROOT_ . '</b><br/>'; ?>
				</li>
				<li id="php_mem_debug"></li>
				<li id="exec_time"></li>
			</ul>
		</div>
		<?php 
		}
		?>

		<div class="center-wrapper">
			<div class="content">
				<div id="main">

					<?php 
					require_once 'inc/skeleton/message.php';

					$file = 'step1.php';

					if(isset($_GET['step']))
					{
						switch($_GET['step'])
						{
							case '10':
								$file = 'step1.demo.php';
								break;
							case '2':
								$file = 'step2.php';
								break;
							case '20':
								$file = 'step2.demo.php';
								break;
							case '3':
								$file = 'step3.php';
								break;
							case '30':
								$file = 'step3.demo.php';
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
</body>
</html>
