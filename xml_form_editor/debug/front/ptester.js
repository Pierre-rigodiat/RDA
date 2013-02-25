$(document).ready(function(){
	// Linking the click event the refresh button
	$('.refresh.form').on('click', refreshForm);
	$('.save.file').on('click', saveFile);
	$('.refresh.conf').on('click', refreshConf);
	$('.save.data').on('click', saveData);
});

/**
 * 
 */
refreshForm = function()
{
	var htmlFormTitle = $(this).parent();
	console.log('[refreshForm] Refreshing form ...');
	
	$.ajax({
        url: 'debug/back/generateForm.php',
        type: 'GET',
        success: function(data) {
        	htmlFormTitle.next().next().remove();
        	htmlFormTitle.next().after(data);
        	
        	console.log('[refreshForm] Form successfully refreshed...');
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

/**
 * 
 */
saveFile = function()
{
	var fileName = $('#schema_file').find(':selected').text();
	var pageNumber = $('#page_number').attr('value');
	
	console.log('[refreshFile] Loading '+fileName+' (in '+pageNumber+' page(s))...');
	
	$.ajax({
        url: 'debug/back/loadFile.php',
        type: 'GET',
        success: function(data) {
        	// Destroy and remove the dialog to avoid to rewrite on it
        	$( "#dialog" ).dialog("destroy");
        	$( "#dialog" ).remove();
        	// Destroy all element written
			$('#cfg_view').children(':first').next().remove();
        	
        	// Write the new content after the header  	
        	$('#cfg_view').children('h3').after(data);
        	
        	loadEditController();
        	
        	alert('Configuration saved!');
        },
        error: function() {
            console.error("[refreshFile] Problem with the AJAX call");
        },
        // Form data
        data: 'f='+fileName+'&p='+pageNumber,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
refreshConf = function()
{
	console.log('[refreshConf] Refreshing configuration...');
	
	$.ajax({
        url: 'debug/back/loadFile.php',
        type: 'GET',
        success: function(data) {
        	// Destroy and remove the dialog to avoid to rewrite on it
        	$( "#dialog" ).dialog("destroy");
        	$( "#dialog" ).remove();
        	// Destroy all element written
			$('#cfg_view').children(':first').next().remove();
        	
        	// Write the new content after the header  	
        	$('#cfg_view').children('h3').after(data);
        	
        	loadEditController();
        },
        error: function() {
            console.error("[refreshConf] Problem with the AJAX call");
        },
        // Form data
        //data: 'f='+fileName,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
saveData = function()
{
	console.log("[saveData] Saving fields...");
	
	var inputs = $('input.text'),
		qString = '';
	
	inputs.each(function()
	{
		var inputId = $(this).parent().attr('id'),
			inputValue = $(this).attr('value');
		
		if(inputValue != '' && !isNaN(parseInt(inputId)))
		{
			console.log('Id '+parseInt(inputId)+' = '+inputValue);
			qString += parseInt(inputId)+'='+inputValue+'&';
		}	
	});
	
	qString = qString.substring(0, qString.length-1);
	
	$.ajax({
        url: 'debug/back/saveData.php',
        type: 'GET',
        success: function(data) {
        	
        },
        error: function() {
            console.error("[saveData] Problem with the AJAX call");
        },
        // Form data
        data: qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
	
	console.log('qString = '+qString);
}