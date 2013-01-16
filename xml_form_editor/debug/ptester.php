<?php
	session_start();
	require_once '../inc/lib/StringFunctions.php';
	require_once '../parser/parser.inc.php';
?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>

	<link rel="stylesheet" type="text/css" href="resources/css/style.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/style.add.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="resources/css/dialog.css" media="screen" />
	
	<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="ontology/auto-complete.css" media="screen" />
	
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js"></script>
	
	<script src="ontology/auto-complete.js"></script>
	<script src="parser/controllers/js/addRemove.js"></script>
	<script src="parser/controllers/js/edit.js"></script>
	<script src="parser/controllers/js/module.js"></script>
	<script src="parser/controllers/js/pagination.js"></script>
	<script src="resources/js.new/php.js"></script>
	<script src="debug/front/ptester.js"></script>
	
	<title>Parser Tester</title>
</head>
<body id="content-wrapper">
	<h1>Parser Implementation Tester</h1>
	<div class="warn">
		The purpose of this tool is to test all parser features and verify that all is working good.	
		This is a debug page, not meant for production purposes. 
	</div>
	<h2>Configuration view</h2>
	<div class="block">
		<h3>Configuration</h3>
		<div>
			<label for="schema_file">Load</label>
			<select id="schema_file">
				<?php
					$schemaFolder = '../resources/files/schemas';
					$schemaFolderFiles = scandir($schemaFolder);
					
					foreach($schemaFolderFiles as $file)
					{
						if(endsWith($file, '.xsd')) echo '<option>'.$file.'</option>';
					}
				?>
			</select>
			<label for="page_number">with</label>
			<input class="text" type="number" id="page_number" name="page_number" value="<?php echo isset($_SESSION['xsd_parser']['phandler'])? unserialize($_SESSION['xsd_parser']['phandler'])->getNumberOfPage():'1'; ?>"/>
			page(s)
			<div class="icon refresh file"></div>
		</div>
		<div>
			<p style="font-weight: bold">Modules</p>
			<div id="schema_modules">
			<?php
				displayModuleChooser();
			?>
			</div>
		</div>
	</div>
	
	<div class="block" id="cfg_view">
		<h3>Elements <span class="icon refresh conf"></span></h3>
		<?php
			displayConfiguration();
		?>
	</div>
	
	<hr/>
	<h2>HTML Form View <span class="icon refresh form"></span></h2>
	<div>
		<span class="ctx_menu"><span class="icon begin"></span></span>
		<span class="ctx_menu"><span class="icon previous"></span></span>
		<span class="ctx_menu button">1</span>
		<span class="ctx_menu selected">2</span>
		<span class="ctx_menu button">3</span>
		<span class="ctx_menu button">4</span>
		<span class="ctx_menu button">5</span>
		<span class="ctx_menu"><span class="icon next"></span></span>
		<span class="ctx_menu"><span class="icon end"></span></span>
	</div>
	<?php
		displayHTMLForm();
	?>
	<hr/>
	<h2>XML View</h2>
	<?php
		displayXMLTree();
	?>
	<script>
		loadEditController();
		loadModuleController();
		loadPaginationController();
		
		loadAutocomplete();
	</script>
</body>
</html>