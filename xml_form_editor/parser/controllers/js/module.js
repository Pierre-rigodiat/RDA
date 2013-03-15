/**
 *	Event handler for the schema configuration.
 * 	Handles:
 * 		- Adding/Removing modules
 * 		- Save current modification on the schema
 * 		- Reload the original file
 *  
 * 
 */
loadModuleController = function()
{
	$('.module').on('click', toggleModule);
}

toggleModule = function()
{
	var iconClass = $(this).children(':first').attr('class');
	var clickLocation = $(this);
	var moduleName = $(this).text();
	
	
	console.log('[toggleModule] Clicked on '+moduleName+' (class: '+iconClass+')');
	
	if(iconClass.indexOf('disable')==-1)
	{
		console.log('[toggleModule] Toggling '+moduleName+'...');
		
		$.ajax({
	        url: 'parser/controllers/php/toggleModule.php',
	        type: 'GET',
	        success: function(data) {
	        	var jsonObject = $.parseJSON(data);
	        	
	        	// 
	        	if(jsonObject.code>=0)
	        	{
	        		clickLocation.children(':first').attr('class', 'icon legend '+jsonObject.result);
					console.log('[toggleModule] Module '+moduleName+' successfully toggled');
	        	}
	        	else
	        	{
	        		console.error('[toggleModule] Error '+jsonObject.code+'  ('+jsonObject.result+') occured while toggle module');
	        	}
	        },
	        error: function() {
	            console.error("[toggleModule] Problem with module "+moduleName);
	        },
	        // Form data
	        data: 'm='+moduleName,
	        //Options to tell JQuery not to process data or worry about content-type
	        cache: false,
	        contentType: false,
	        processData: false
	    });
	}
	else
	{
		console.log('[toggleModule] Module '+moduleName+' is disable, it cannot be loaded!');
	}
}