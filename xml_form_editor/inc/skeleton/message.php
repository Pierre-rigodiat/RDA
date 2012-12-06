<?php
	$msg_class=null;

	if(isset($_GET['message']))
	{
		switch($_GET['message'])
		{
			case 'success':
				$msg_class="success";
				break;
			case 'warning':
				$msg_class="warn";
				break;
			case 'error':
				$msg_class="error";
				break;
			case 'info':
				$msg_class="info";
				break;
			default:
				break;
		}
	}

	if($msg_class)
	{
		echo '<div class="'.$msg_class.'">Schema named <i>mgiml_light.xsd</i> successfully uploaded !</div>';
	}
?>

