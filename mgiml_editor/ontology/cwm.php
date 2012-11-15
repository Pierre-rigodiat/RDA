<?php

$output = array();
$name = "sessionid";
exec('ontology-bash/cwm.sh'.' '.'MaterialSubstance'.' '.$name, $output,$val);
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

?>
