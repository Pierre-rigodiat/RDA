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
					
					$currentFilename =  '';
					if(isset($_SESSION['xsd_parser']['xsd_filename'])) $currentFilename = $_SESSION['xsd_parser']['xsd_filename'];
					
					foreach($schemaFolderFiles as $file)
					{
						if(endsWith($file, '.xsd')) echo '<option'.($currentFilename==$file?' selected="selected"':'').'>'.$file.'</option>';
					}
				?>
			</select>
		</div>
		<div>
			<p style="font-weight: bold">Pages</p>
			<div id="schema_pages">
			<?php
				displayPageChooser();
			?>
			</div>
		</div>
		<div>
			<p style="font-weight: bold">Modules</p>
			<div id="schema_modules">
			<?php
				displayModuleChooser();
			?>
			</div>
		</div>
		<div class="icon legend save file">Save configuration</div>
	</div>
	
	<div class="block" id="cfg_view">
		<h3>Elements <span class="icon refresh conf"></span></h3>
		<?php
			displayConfiguration();
		?>
	</div>
	
	<hr/>
	<h2>HTML Form View <span class="icon refresh form"></span></h2>
	<?php
		displayPageNavigator();
		displayHTMLForm();
	?>
	<div class="icon legend save data">Save fields</div>
	<hr/>
	<h2>XML View</h2>
	<?php
		displayXMLTree();
	?>
	<script>
		loadEditController();
		loadAddRemoveController();
		
		loadModuleController();
		loadPaginationController();
		
		loadAutocomplete();
	</script>
</body>
</html>