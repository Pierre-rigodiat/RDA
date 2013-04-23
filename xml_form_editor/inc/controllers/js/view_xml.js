/**
 * 
 */
loadViewXmlController = function()
{
	$('.btn.download-xml').on('click', downloadXml);
	$('.btn.save-to-repo').on('click', saveXml);	
}

downloadXml = function()
{
	console.log('[downloadXml] Downloading XML...');
	
	window.location = 'inc/controllers/php/downloadXml.php';
	
	console.log('[downloadXml] XML downloaded');
}

saveXml = function()
{
	var successMessage = '<div class="temp success"><span class="icon valid"></span>Document successfully saved!</div>',
		errorMessage = '<div class="temp error"><span class="icon invalid"></span>An error occured during the save</div>',
		messageLocation = $("#main").children(":first");
	
	console.log('[saveXml] Saving XML...');
	
	$.ajax({
        url: 'inc/controllers/php/saveExperiment.php',
        type: 'GET',
        success: function(data) {
        	messageLocation.hide().html(successMessage).fadeIn(500);
        	messageLocation.delay(2000).fadeOut(500);
        	        	
        	console.log('[saveXml] XML saved');
        },
        error: function() {
        	messageLocation.hide().html(errorMessage).fadeIn(500);
        	messageLocation.delay(2000).fadeOut(500);   
        	   
            console.error("[saveXml] A problem occured during the save");
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
	
	
}
