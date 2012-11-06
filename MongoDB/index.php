<?php

require_once 'mongodb.php';
require_once 'xml2json/xml2json.php';

$db = new MongoDBStream ("127.0.0.1","test");
$db->openDB();
$db->insertJson("jsontest.json","test");

?>