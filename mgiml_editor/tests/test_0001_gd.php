<h3>GD lib image cut</h3>
<?php
	echo "Starting test... (PHP display OK)<br/>";

	require_once _ROOT_ . '/inc/global/images.php';
	
	echo 'Result: <img src="data:image/gif;base64,' . getIconBase64(0, 1) . '" alt="Test image" />';
?>
<hr/>