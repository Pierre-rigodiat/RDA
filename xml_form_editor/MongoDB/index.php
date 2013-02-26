<?php

require_once 'mongodb.php';
require_once 'xml2json/parker.php';
require_once 'xml2json/badgerFish.php';
require_once 'xml2json/spark.php';
require_once 'xml2json/gData.php';
require_once 'xml2json/xml2jsonIBM.php';
require_once 'xml2json/xml2jsonAbdera.php';
require_once 'xml2json/xml2jsonJSONML.php';

$db = new MongoDBStream ("127.0.0.1","test");
$db->openDB();
$db->retrieveXml("testBadgerFish.json","test");

?>
