<?php

require_once '../../MongoDB/xml2json/parker.php';
require_once '../../MongoDB/xml2json/badgerFish.php';
require_once '../../MongoDB/xml2json/spark.php';
require_once '../../MongoDB/xml2json/gData.php';
require_once '../../MongoDB/xml2json/jsonML.php';

function encodeToJSON($type)
{
	$type = $_GET["encode"];
	
	switch ($type) {
		case "encodeBadgerFish":
			return json_encode(encodeBadgerFish(DOMDocument::load('../../MongoDB/experiment_data.xml')));
			break;
		case "encodeGData":
			return json_encode(encodeGData(DOMDocument::load('../../MongoDB/testXml.xml')));
			break;
		case "encodeParker":
			return json_encode(encodeParker(DOMDocument::load('../../MongoDB/testXml.xml')));
			break;
		case "encodeSpark":
			return json_encode(encodeSpark(DOMDocument::load('../../MongoDB/testXml.xml')));
			break;
		case "encodeJSONML":
			return json_encode(encodeJSONML(DOMDocument::load('../../MongoDB/experiment_data.xml')));
			break;
	}
}
$type = '';
echo encodeToJSON($type);

?>