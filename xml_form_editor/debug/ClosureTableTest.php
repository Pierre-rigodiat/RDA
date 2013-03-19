<?php
session_start();
require_once "../inc/helpers/Logger.php";
require_once "../parser/core/Tree_.php";
require_once "../parser/core/ReferenceTree.php";

$time = microtime(TRUE);
$mem = memory_get_usage();

$closureTable = new Tree("testClosureTable");

$elemRoot = "root";
$elem1 = "A";
$elem2 = "B";
$elem3 = "C";
$elem4 = "D";
$elem5 = "E";

$rootId = $closureTable -> insert($elemRoot);
$e1Id = $closureTable -> insert($elem1, $rootId);
$e2Id = $closureTable -> insert($elem2, $rootId);
$e3Id = $closureTable -> insert($elem5, $rootId);
$e4Id = $closureTable -> insert($elem3, $rootId);
$e5Id = $closureTable -> insert($elem4, $e4Id);

// Attach C to A
$closureTable -> setParent($e4Id, $e1Id);
$childrenArray = $closureTable -> getChildren($rootId);

// Change E to F
$closureTable -> setElement($e3Id, "F");

// Delete A
$closureTable -> delete($e1Id);

$cArrayId = $closureTable ->find("C"); 
$cArrayId = $closureTable ->find("D"); 
echo 'Memory: '.round((memory_get_usage() - $mem) / (1024 * 1024), 2).' Mb<br/>';
echo 'Time: '.round(microtime(TRUE) - $time, 1). ' sec';

echo $closureTable;
var_dump($childrenArray);
var_dump($cArrayId);

$time = microtime(TRUE);
$mem = memory_get_usage();

$refTree = new ReferenceTree($closureTable);

$rtRootId = $refTree -> insert($rootId);
$rt1Id = $refTree -> insert($e2Id, $rtRootId);

// Attach C to A
/*$closureTable -> setParent($e4Id, $e1Id);
$childrenArray = $closureTable -> getChildren($rootId);

// Change E to F
$closureTable -> setElement($e3Id, "F");

// Delete A
$closureTable -> delete($e1Id);

$cArrayId = $closureTable ->find("C"); 
$cArrayId = $closureTable ->find("D"); */
echo 'Memory: '.round((memory_get_usage() - $mem) / (1024 * 1024), 2).' Mb<br/>';
echo 'Time: '.round(microtime(TRUE) - $time, 1). ' sec';

echo $refTree;
echo 'getElement('.$rt1Id.')';
var_dump($refTree -> getElement($rt1Id));
