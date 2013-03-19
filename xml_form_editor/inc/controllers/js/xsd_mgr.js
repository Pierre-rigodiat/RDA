/**
 * 
 */
loadXsdManagerHandler = function()
{
	$('.add').on('click', setCurrentModel);
	$('.upload.schema').on('click', uploadSchema);
}

/**
 * 
 */
setCurrentModel = function()
{
	var modelName = $(this).parent().siblings(':first').text(),
		tdElement = $(this).parent();
	
	$('.add').off('click');
		
	tdElement.html('<img src="resources/img/ajax-loader.gif" alt="Loading..."/>');
		
	console.log('[setCurrentModel] Loading '+modelName+'...');
	
	$.ajax({
        url: 'inc/controllers/php/schemaLoader.php',
        type: 'GET',
        success: function(data) {
        	// Refresh the page
        	loadPage($(location).attr('href')+'?manageSchemas');
        	console.log('[setCurrentModel] '+modelName+' loaded');
        },
        error: function() {
            console.error("[setCurrentModel] A problem occured during schema loading");
        },
        // Form data
        data: 'n='+modelName,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
uploadSchema = function()
{
	console.warn("[uploadSchema] Not yet implemented");
}

