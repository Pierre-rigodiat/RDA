<?php
require_once "../parser/core/ClosureTable.php";

$time = microtime(TRUE);
$mem = memory_get_usage();

$closureTable = new ClosureTable("testClosureTable");

$elemRoot = "root";
$elem1 = "A";
$elem2 = "B";
$elem3 = "C";
$elem4 = "D";
$elem5 = "E";

$rootId = $closureTable -> insertElement($elemRoot);
$e1Id = $closureTable -> insertElement($elem1, $rootId);
$e2Id = $closureTable -> insertElement($elem2, $rootId);
$e3Id = $closureTable -> insertElement($elem5, $rootId);
$e4Id = $closureTable -> insertElement($elem3, $rootId);
$e5Id = $closureTable -> insertElement($elem4, $e4Id);

// Attach C to A
$closureTable -> setParent($e4Id, $e1Id);
$childrenArray = $closureTable -> getChildrenId($rootId);

// Attach C' to B
$e4_1Id = $closureTable -> duplicateElement($e4Id, true);
$closureTable -> setParent($e4_1Id, $e2Id);

// Attach A' to E
$e1_1Id = $closureTable -> duplicateElement($e1Id, true);
$closureTable -> setParent($e1_1Id, $e3Id);

$closureTable -> delete($e1_1Id/*, true*/);

$closureTable -> setElement($e3Id, "F");

$cArrayId = $closureTable ->getIds("C"); 
$cArrayId = $closureTable ->getIds("D"); 
echo 'Memory: '.round((memory_get_usage() - $mem) / (1024 * 1024), 2).' Mb<br/>';
echo 'Time: '.round(microtime(TRUE) - $time, 1). ' sec';

echo $closureTable;
var_dump($childrenArray);
var_dump($cArrayId);
