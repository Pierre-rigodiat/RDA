/**
 * 
 */
loadPaginationController = function()
{
	$('.begin').live('click', loadFormPage);
	$('.end').live('click', loadFormPage);
	$('.previous').live('click', loadFormPage);
	$('.next').live('click', loadFormPage);
	$('.ctx_menu.button').live('click', loadFormPage);
}

loadFormPage = function()
{
	var page='';
	
	if($(this).attr('class')!='ctx_menu button')
		page = $(this).attr('class');
	else
		page = $(this).text();
	
	console.log('[loadFormPage] Changing page: '+page+'...');
		
	$.ajax({
        url: 'parser/controllers/php/changePage.php',
        type: 'GET',
        success: function(data) {
        	var jsonObject = $.parseJSON(data);
        	
        	// 
        	if(jsonObject.code>=0)
        	{
        		$(".paginator").replaceWith(htmlspecialchars_decode(jsonObject.result));
        		//$("#page_content").replaceWith('<div id="page_content">[loadFormPage] Page '+page+' set</div>');
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
        data: 'p='+page,
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
