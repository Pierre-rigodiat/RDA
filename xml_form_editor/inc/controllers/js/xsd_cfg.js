/**
 *	Event handler for the schema configuration.
 * 	Handles:
 * 		- Adding/Removing modules
 * 		- Save current modification on the schema
 * 		- Reload the original file
 *  
 * 
 */
loadXsdConfigHandler = function()
{
	$('.refresh').on('click', cancelChanges);
	$('.save').on('click', saveChanges);
	$('.clickable').on('click', goToPage);
}

/**
 * 
 */
// TODO put this function in the main configuration
goToPage = function()
{
	var defaultName = "clickable ",
		baseUrl = $(location).attr('href'),
		pageName = $(this).attr('class').substr(defaultName.length);
	
	pageName = pageName.split('-');
	//console.log(pageName[0]+' '+pageName[1]);
	
	if((index = baseUrl.indexOf('/'+pageName[0]))==-1 || index!=baseUrl.length-(pageName[0].length+1))
	{		
		//console.log('Need to rewrite '+index+' '+(baseUrl.length-pageName[0].length));
		var lastPathIndex = baseUrl.lastIndexOf('/');
		baseUrl = baseUrl.substr(0, lastPathIndex) + pageName[0];
	}
	
	loadPage(baseUrl + '?' + pageName[1]);
}

/**
 * 
 * 
 * 
 */
cancelChanges = function()
{
	console.warn('[cancelChanges] Not yet implemented');
}

/**
 *
 * 
 *  
 */
saveChanges = function()
{
	console.log('[saveChanges] Saving configuration...');
	$("#main").prepend('<div></div>');
	
	var successMessage = '<div class="success"><span class="icon valid"></span>Schema successfully saved!</div>',
		errorMessage = '<div class="error"><span class="icon invalid"></span>An error occured during the save</div>',
		messageSite = $("#main").children(":first");
	
	
	$.ajax({
        url: 'inc/controllers/php/saveConfig.php',
        type: 'GET',
        success: function(data) {
        	messageSite.hide().html(successMessage).fadeIn(500);
        	messageSite.delay(2000).fadeOut(500);
        	        	
        	console.log('[saveChanges] Configuration saved');
        },
        error: function() {
        	messageSite.hide().html(errorMessage).fadeIn(500);
        	messageSite.delay(2000).fadeOut(500);   
        	   
            console.error("[saveChanges] A problem occured during the save");
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}