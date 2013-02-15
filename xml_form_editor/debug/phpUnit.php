<?php
// Tests the Tree object
//require_once 'classes/Tree.php';

// Those should produce an error in the log file
/*$tree = new Tree('test');
$tree = new Tree(124);
$tree = new Tree(124, false);
$tree = new Tree(array(), 'test');

// Those should produce a warning in the log file
$tree->setDebug(array());
$tree->setDebug('test');
$tree->setDebug(-127);*/

// Should produce some log message
$tree = new Tree(true);

$rootIndex = $tree->insertElement(1);
$childIndex = $tree->insertElement(10, $rootIndex);

$tree->insertElement('100', $childIndex);
$removeIndex = $tree->insertElement(101, $childIndex);

$tree->insertElement(array(1010, '1010'), $removeIndex);
$tree->insertElement(1011, $removeIndex);

//$tree->removeElement($removeIndex, true);
$tree->removeElement(80);
//$tree->removeElement(0);

$tree->copyTreeBranch($removeIndex);
$tree->removeElement($removeIndex, true);

/* Displays the tree */
var_dump($tree->getTree());
echo '<hr/>';

/* Search an ID */
var_dump($tree->getId(10));

/* Additional functions test */
$children = $tree->getChildren($rootIndex);
echo 'Children of '.$rootIndex.' are ';
print_r($children);
echo '<br/>';

$parent = $tree->getParent($childIndex);
echo 'Parent of '.$childIndex.' is '.$parent.'<br/>';

$object = $tree->getObject($childIndex);
echo 'Object at index '.$childIndex.' is ';
var_dump($object);
?>