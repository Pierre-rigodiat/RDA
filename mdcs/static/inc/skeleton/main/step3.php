<center><h2>Tables</h2></center>

<form id="file_upload" enctype="multipart/form-data">
	<input type="file" name="file[0]" id="file[0]"/><span id="info[0]"></span>
	<br/>
	
	<input type="button" class="button" id="tostep2" value="Go back" />
	<input type="button" class="button reset" value="Remove all files" />
	<input type="button" class="button" id="tostep4" value="Next step"><?php //todo disable this button until  ?>
</form>
<?php 
	if(isset($_SESSION['app']['xml']['tables'])) echo count($_SESSION['app']['xml']['tables']).' table(s) registered';
	else echo 'No tables registered';
?>
