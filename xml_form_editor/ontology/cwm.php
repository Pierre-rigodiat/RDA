<?php

$output = array();
$name = "sessionid";
$search = "";
$onto = "";
$relation = "";

$unit = array("unitOfMeasureType", "name");
$crystal = array("crystalStructure", "name");
$form = array("materialForm", "name");
$phase = array("phase", "name");

$element = array($_GET["parent"], $_GET["node"]);

if (array_diff($element, $crystal) == array()) {
	$search = "CrystalLattice";
	$onto = "Materials.owl";
	$relation = "rdfs:subClassOf";
}
if (array_diff($element, $form) == array()) {
	$search = "MaterialForm";
	$onto = "Materials.owl";
	$relation = "rdf:type";
}
if (array_diff($element, $phase) == array()) {
	$search = "MaterialPhaseComposition";
	$onto = "Materials.owl";
	$relation = "rdfs:subClassOf";
}
if (array_diff($element, $unit) == array()) {
	$search = "UnitOfMeasure";
	$onto = "OntologyRequirements.owl";
	$relation = "rdfs:subClassOf";
}

if ($search != "") {
	exec('ontology-bash/cwm.sh'.' '.$search.' '.$name.' '.$onto.' '.$relation, $output,$val);
	/*print_r($output);
	echo $val;*/
	$file = $name.".json";
	$pattern = $_GET["term"];
	$handle = fopen($file,"r");
	$match = array();
	if ($handle) {
	    while (($buffer = fgets($handle)) !== false) {
		if (stristr($buffer,$pattern) !== false)
			array_push($match, trim($buffer));
	    }
	    fclose($handle);
	}
	if ($match[0] != null)
		echo implode(",", $match);
}
else echo "";
?>
