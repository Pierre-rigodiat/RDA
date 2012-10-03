$(document).ready(function(){
	// Linking the event on all the + buttons
	$('#download').on('click', download);
	
	$('#tostep2').on('click', {page: 2}, moveTo);
});

download = function()
{
	/*if (window.XMLHttpRequest)
	{
		// Code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{
		// Code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	xmlhttp.open("GET","download.php", true);
	xmlhttp.send();*/
	
	window.location = 'inc/ajax/download.php';

};