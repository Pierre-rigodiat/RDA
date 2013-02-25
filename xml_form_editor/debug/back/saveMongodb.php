<?php

require_once 'encode.php';
require_once '../../MongoDB/mongodb.php';
require_once '../../MongoDB/xml2json/parker.php';
require_once '../../MongoDB/xml2json/badgerFish.php';
require_once '../../MongoDB/xml2json/spark.php';
require_once '../../MongoDB/xml2json/gData.php';

$db = new MongoDBStream ("127.0.0.1","test");
$db->openDB();

$jsonString = encodeToJSON();

$db->insertJson($jsonString, "test");

?>