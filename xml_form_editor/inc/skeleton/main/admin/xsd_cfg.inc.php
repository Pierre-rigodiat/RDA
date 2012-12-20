<h2>Schema configuration</h2>
<div id="schema_prop">
	<div id="main_prop">
		<div class="prop"><span class="fieldname">Filename:</span> test.xsd</div>
		<div class="menu">
			<div class="icon legend refresh">Reload</div>
			<div class="icon legend save">Save</div>	
		</div>
	</div>
	<div id="misc_prop">
		<div class="prop"><span class="fieldname">Last modification:</span> 12-04-2012 11:32am</div>
		<div class="prop"><span class="fieldname">Size:</span> 120 Mo</div>
	</div>
</div>
<div id="schema_content">
	<h3>Modules</h3>
	<div id="schema_modules">
		<div class="module"><span class="icon legend off">Pagination<span class="icon new"></span></span></div>
		<div class="module"><span class="icon legend off">HDF-5</span></div>
		<div class="module"><span class="icon legend disable">Images (Coming soon)</span></div>
		<div class="module"><span class="icon legend disable">Videos (Coming soon)</span></div>
	</div>
	
	<h3>Elements</h3>
	<div id="schema_elements">
		<?php
			require_once 'parser/parser.inc.php';
		
			$schemaFile = 'resources/files/demo_2.xsd';
			loadSchema($schemaFile);
		
			displayConfiguration();
		?>
	</div>
</div>

