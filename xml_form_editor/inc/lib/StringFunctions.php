<?php
// XXX Avoid infinite includes in lib
define("DEBUG_LIB_STR", false);

// TODO Add the endWith function if needed
// TODO lastIndexOf function ? (it is the strrpos function but the name is not really explicit)

function startsWith($string, $needle)
{
	$length = strlen($needle);
	return (substr($string, 0, $length) === $needle);
}

function endsWith($string, $needle)
{
	$length = strlen($needle);
    if ($length == 0) return true;

    return (substr($string, -$length) === $needle);
}
?>