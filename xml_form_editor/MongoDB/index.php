<?php

require_once 'mongodb.php';
require_once 'xml2json/parker.php';
require_once 'xml2json/badgerFish.php';
require_once 'xml2json/spark.php';
require_once 'xml2json/gData.php';
require_once 'xml2json/jsonML.php';

$db = new MongoDBStream ("127.0.0.1","test");
$db->openDB();
$db->retrieveXml("testJSONML.json","test");
//$db->insertXml("testXml.xml","test");

?>
