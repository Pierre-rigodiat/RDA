<?php

require_once 'encode.php';
require_once '../../MongoDB/mongodb.php';
require_once '../../MongoDB/xml2json/parker.php';
require_once '../../MongoDB/xml2json/badgerFish.php';
require_once '../../MongoDB/xml2json/spark.php';
require_once '../../MongoDB/xml2json/gData.php';
require_once '../../MongoDB/xml2json/jsonML.php';

$db = new MongoDBStream ("127.0.0.1","test");
$db->openDB();

$type = '';
$jsonArray = encodeToJSON($type);

//Include the translation name into the JSON array to push in MongoDB
$jsonArray = json_decode($jsonArray);

$db->insertJson($jsonArray, "test");

?>