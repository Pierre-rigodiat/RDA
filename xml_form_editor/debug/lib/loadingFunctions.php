<?php
function setUpChildrenToPage($pHandler, $tree, $elementId, $pageId)
{		
	$children = $tree -> getChildren($elementId);
	
	foreach($children as $child)
	{
		$pHandler -> removePagesForId($child);
		$pHandler -> setPageForId($pageId, $child);
		setUpChildrenToPage($pHandler, $tree, $child, $pageId);
	}
}

function setUpChildrenToModule($manager, $tree, $elementId, $moduleName)
{
	$children = $tree -> getChildren($elementId);
	
	foreach($children as $child)
	{
		$manager -> assignIdToModule($child, $moduleName);
		setUpChildrenToModule($manager, $tree, $child, $moduleName);
	}
}