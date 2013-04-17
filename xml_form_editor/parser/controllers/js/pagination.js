/**
 * 
 */
loadPaginationController = function()
{
	$(document).on('click', '.pagination>ul>li', loadFormPage);
}

loadFormPage = function(event)
{
	event.preventDefault(); // Prevent the "a" tag for doing its job
	
	console.log('[loadFormPage] Changing page...');
		
	$.ajax({
        url: 'parser/controllers/php/changePage.php',
        type: 'GET',
        success: function(data) {
        	var jsonObject = $.parseJSON(data);
        	
        	// 
        	if(jsonObject.code>=0)
        	{        		
        		$(".pagination").html(htmlspecialchars_decode(jsonObject.result));
        		updatePageContent();
        		console.log('[loadFormPage] Page '+page+' set');
        	}
        	else
        	{
        		console.error('[loadFormPage] Error '+jsonObject.code+'  ('+jsonObject.result+') occured');
        	}
        },
        error: function() {
            console.error("[loadFormPage] Problem with page "+page);
        },
        // Form data
        data: 'p='+$(this).text().toLowerCase(),
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

updatePageContent = function()
{
	console.log('[updatePageContent] Updating content...');
	$.ajax({
        url: 'parser/controllers/php/changePage.php',
        type: 'GET',
        success: function(data) {
        	var jsonObject = $.parseJSON(data);
        	
        	if(jsonObject.code>=0)
        	{
        		$("#page_content").replaceWith(htmlspecialchars_decode(jsonObject.result));
        		loadRegisterFormController();
        		loadAutoComplete();
        		console.log('[updatePageContent] Content updated');
        	}
        	else
        	{
        		console.error('[updatePageContent] Error '+jsonObject.code+'  ('+jsonObject.result+') occured');
        	}
        },
        error: function() {
            console.error("[updatePageContent] Problem with page "+page);
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}
