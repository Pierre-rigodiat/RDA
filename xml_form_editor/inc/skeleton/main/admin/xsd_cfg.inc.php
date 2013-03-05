<?php
require_once $_SESSION['config']['_ROOT_'].'/parser/parser.inc.php';

$file = array(
	"name" => "<i>undefined</i>",
	"modif" => "<i>N/A</i>",
	"size" => "<i>N/A</i>",
	"unit" => ''
);

if(isset($_SESSION['xsd_parser']['xsd_filename']))
{
	$unit = array('', 'K', 'M', 'G', 'T');
	
	$file['name'] = $_SESSION['xsd_parser']['xsd_filename'];
	$file['size'] = floatval(filesize($_SESSION['config']['_XSDFOLDER_'].'/'.$file['name']));

	$currentUnit = 0;
	while($file['size'] > 1000 && $currentUnit<4)
	{
		$file['size'] = number_format($file['size']/1024, 2);
		$currentUnit += 1;
	}
	
	$file['unit'] = $unit[$currentUnit].'o';
	
	$file['modif'] = date( "D d M Y g:i A", filemtime($_SESSION['config']['_XSDFOLDER_'].'/'.$file['name']));
}
?>
<div id="featured-wrapper"><div id="featured">
	<h1>Schema View Configuration</h1>
</div></div>

<div id="main">
<?php
	if(!isset($_SESSION['xsd_parser']['xsd_filename']))
	{
		echo '<div class="warn"><span class="icon warning"></span>The system has no schema loaded. Please configure one with the <span class="clickable schemas-manageSchemas">schema manager</span>.</div>';	
	}
?>
<div id="schema_prop">
	<div id="main_prop">
		<div class="prop"><span class="fieldname">Filename:</span> <?php echo $file['name'] ?></div>
	</div>
	<div id="misc_prop">
		<div class="prop"><span class="fieldname">Last modification:</span> <?php echo $file['modif'] ?></div>
		<div class="prop"><span class="fieldname">Size:</span> <?php echo $file['size'].' '.$file['unit'] ?></div>
	</div>
</div>
<div id="schema_content">	
	<h3 style="float:left">Elements</h3>
	<div class="right-side">
		<span>
		<?php
			displayPageChooser();
		?>
		</span>
		<span class="ctx_menu">
			<div class="icon legend refresh">Cancel</div>
			<div class="icon legend save">Save</div>
		</span>
	</div>
	<div id="schema_elements">
		<?php
			displayConfiguration();
		?>
	</div>
</div>
</div>

<script src="parser/controllers/js/edit.js"></script>
<script src="resources/js.new/xsd_cfg.js"></script>
<script>
	loadEditController();
	loadXsdConfigHandler();
</script>

