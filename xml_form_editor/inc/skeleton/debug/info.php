<h2>
	Debug info
	<!-- img src="resources/img/debug-loader.gif" alt="Loading..."/-->
</h2>
<ul>
	<li><?php echo '<u>Root folder:</u> <b>' . _ROOT_ . '</b><br/>'; ?>
	</li>
	<li id="php_mem_debug"></li>
	<li id="exec_time"></li>
	<li>
		<u>Server Info:</u>
		<b>
			<?php
				print_r($_SERVER); // TODO improve data display
				echo '<br/>';
			?>
		</b>
	</li>
</ul>