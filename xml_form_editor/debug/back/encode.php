<?php

require_once '../../MongoDB/xml2json/parker.php';
require_once '../../MongoDB/xml2json/badgerFish.php';
require_once '../../MongoDB/xml2json/spark.php';
require_once '../../MongoDB/xml2json/gData.php';


function encodeToJSON()
{
	$type = $_GET["encode"];
	
	switch ($type) {
		case "encodeBadgerFish":
			return encodeBadgerFish(DOMDocument::load('../../MongoDB/testXml.xml'));
			break;
		case "encodeGData":
			return encodeGData(DOMDocument::load('../../MongoDB/testXml.xml'));
			break;
		case "encodeParker":
			return encodeParker(DOMDocument::load('../../MongoDB/testXml.xml'));
			break;
		case "encodeSpark":
			return encodeSpark(DOMDocument::load('../../MongoDB/testXml.xml'));
			break;
	}
}

echo encodeToJSON();

?>