$(document).ready(function(){
	// Linking the click event the refresh button
	$('.refresh.form').on('click', refreshForm);
	$('.refresh.file').on('click', refreshFile);
});

refreshForm = function()
{
	var htmlFormTitle = $(this).parent();
	
	$.ajax({
        url: 'debug/back/generateForm.php',
        type: 'GET',
        success: function(data) {
        	htmlFormTitle.next().remove();
        	htmlFormTitle.after(data);
        },
        error: function() {
            console.error("[refreshForm] Problem with the AJAX call");
        },
        // Form data
        //data: 'id='+elementId+'&'+qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

refreshFile = function()
{
	var fileName = $(this).prev().children(':selected').text();
	console.log('[refreshFile] Loading '+fileName+'...');
	
	$.ajax({
        url: 'debug/back/loadFile.php',
        type: 'GET',
        success: function(data) {
        	$('#cfg_view').children(':first').next().remove();
        	$('#cfg_view').children('h3').after(data);
        	loadEditController();
        },
        error: function() {
            console.error("[refreshFile] Problem with the AJAX call");
        },
        // Form data
        data: 'f='+fileName,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}
