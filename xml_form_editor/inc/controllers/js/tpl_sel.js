loadTemplateSelectionControllers = function()
{
	$('.btn.set-template').on('click', setCurrentTemplate);
}

setCurrentTemplate = function()
{
	var templateName = $(this).parent().parent().children(':first').text(),
		tdElement = $(this).parent();
		
	tdElement.html('<img src="resources/img/ajax-loader.gif" alt="Loading..."/>');
	$('.btn.set-template').off('click');
	
	console.log('[setCurrentTemplate] Setting '+templateName+' as current template...');
	
	$.ajax({
        url: 'inc/controllers/php/schemaLoader.php',
        type: 'GET',
        success: function(data) {
      		/* Generate additional trees for the form */
        	generateTrees(tdElement);
        	console.log('[setCurrentTemplate] '+templateName+' loaded');
        },
        error: function() {
            console.error("[setCurrentTemplate] A problem occured during template loading");
        },
        // Form data
        data: 'n='+templateName,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

generateTrees = function(notifElement)
{
	var trElement = notifElement.parent(),
		trElementClass = trElement.attr('class');
	
	$.ajax({
        url: 'parser/controllers/php/generateReferenceTrees.php',
        type: 'GET',
        success: function(data) {
        	try
        	{
        		var jsonObject = $.parseJSON(data);
        		
        		if(jsonObject.code>=0)
	        	{
					console.log('[generateReferenceTrees] Trees generated');
					
					loadPage($(location).attr('href'));
	        	}
	        	else
	        	{
	        		console.error('[generateReferenceTrees] Error '+jsonObject.code+'  ('+jsonObject.result+') occured while toggle module');
	        		
	        		trElement.attr('class', (trElementClass?trElementClass+' error':'error'));
            		notifElement.html('<span style="font-weight:bold;color:red">Ajax call error</span>');
	        	}
        	}
        	catch(ex)
        	{
        		console.error('[generateReferenceTrees] JSON parsing error');
        		
        		trElement.attr('class', (trElementClass?trElementClass+' error':'error'));
            	notifElement.html('<span style="font-weight:bold;color:red">Ajax call error</span>');
        	}
        },
        error: function() {
            console.error("[generateReferenceTrees] Problem with the AJAX call");
            
            trElement.attr('class', (trElementClass?trElementClass+' error':'error'));
            notifElement.html('<span style="font-weight:bold;color:red">Ajax call error</span>');
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}
