/**
 * 
 */
loadXsdManagerHandler = function()
{
	$('.add').on('click', setCurrentModel);
	
}

/**
 * 
 */
setCurrentModel = function()
{
	var modelName = $(this).parent().siblings(':first').text();
	console.log('[setCurrentModel] Loading '+modelName+'...');
	
	$.ajax({
        url: 'inc/ajax.new/schemaLoader.php',
        type: 'GET',
        success: function(data) {
        	// Destroy and remove the dialog to avoid to rewrite on it        	
        	/*$( "#dialog" ).dialog("destroy");
        	$( "#dialog" ).remove();
        	
        	$('.content').children().remove();
        	
        	// Change content
        	$('.content').html(data);
        	
        	console.log('[loadPage] '+url+' loaded');*/
        	
        	
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

