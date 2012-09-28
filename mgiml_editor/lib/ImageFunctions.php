<?php
	// TODO Make a generic function handling all format type (png, jpg, jpeg...)
	function cropPNGImage($originalFile, $destinationFile, $startX, $startY, $width, $height)
	{
		$originalImage = imagecreatefrompng($originalFile);
		$destImage = imagecreatetruecolor($width, $height);
		
		imagecopyresampled($destImage, $originalImage, 0, 0, /*60, 0, 20, 20, 20, 20*/$startX, $startY, $width, $height, $width, $height);
		
		imagepng($destImage, $destinationFile);
		
		return true; // TODO Check every function return in case of a problem
	}
?>