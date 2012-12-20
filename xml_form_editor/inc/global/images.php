<?php
	// XXX File status must be displayed by the caller
	//echo 'Start including <i>images.php</i> ('.__FILE__.')...<br/>';

	require_once _ROOT_ . '/inc/lib/ImageFunctions.php';

	define('ICON_FILENAME', _ROOT_ . "/resources/img/icons.png");
	define('CROPPED_ICON', _ROOT_ . "/temp/.icon.png");
	define('ICON_WIDTH', 16);
	define('ICON_WIDTH_PADDING', 4);
	define('ICON_HEIGHT', 16);
	define('ICON_HEIGHT_PADDING', 4);
	
	// TODO Do not cropped if the base 64 already exists (temp folder)
	function getIconBase64($row, $column)
	{
		$start = array($column * (ICON_WIDTH + ICON_WIDTH_PADDING), $row * (ICON_HEIGHT + ICON_WIDTH_PADDING));
		
		cropPNGImage(ICON_FILENAME, CROPPED_ICON, $start[0], $start[1], ICON_WIDTH, ICON_HEIGHT);
		
		$base64 = base64_encode(file_get_contents(CROPPED_ICON));
		
		unlink(CROPPED_ICON);
		
		return $base64;
	}
	
	//echo 'File <i>images.php</i> included<br/>.';
?>