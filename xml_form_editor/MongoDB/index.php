<?php

require_once 'mongodb.php';
require_once 'xml2json/xml2jsonIBM.php';
require_once 'xml2json/xml2jsonBadgerFish.php';
require_once 'xml2json/xml2jsonParker.php';
require_once 'xml2json/xml2jsonSpark.php';
require_once 'xml2json/xml2jsonGData.php';
require_once 'xml2json/xml2jsonAbdera.php';
require_once 'xml2json/xml2jsonJSONML.php';

$db = new MongoDBStream ("127.0.0.1","test");
$db->openDB();
$db->insertXml("testXml.xml","test");

?>
