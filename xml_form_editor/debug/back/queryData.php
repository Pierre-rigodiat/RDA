<?php

require_once '../../MongoDB/mongodb.php';
require_once '../../MongoDB/xml2json/parker.php';
require_once '../../MongoDB/xml2json/badgerFish.php';
require_once '../../MongoDB/xml2json/spark.php';
require_once '../../MongoDB/xml2json/gData.php';
require_once '../../MongoDB/xml2json/jsonML.php';

$db = new MongoDBStream ("127.0.0.1","xsdmgr");
$db->openDB();

$match = $_GET['match'];
if (is_numeric($match)) {
	$match += 0;
}

$query = array("reports.entry" => array('$elemMatch' => array("content.report_id.$" => $match)));
$cursor = $db->queryData($query, "test");

$echo = '';

if (is_string($cursor)) {
	echo $cursor;
}
elseif (get_class($cursor) == 'MongoCursor' && $cursor != null) {
	foreach ($cursor as $doc) {
		$echo .= '<br/>'.nl2br(htmlspecialchars(decodeBadgerFish($doc)->saveXml()));
	}
	echo $echo;
}

?>