/**
 * 
 */
loadChoiceController = function()
{
	$('.xsdman.choice').live('change', changeChoiceElement);
}

/**
 * 
 */
changeChoiceElement = function()
{
	var choiceId = $(this).parent().attr('id'),
		chosenElementId = $(this).find(':selected').val(),
		elementToModified = $(this).next();
	
	console.log('Choice ID '+choiceId+' has changed to display elementId '+chosenElementId+' (orig)...');
	
	$.ajax({
        url: 'parser/controllers/php/changeDisplayedElement.php',
        type: 'GET',
        success: function(data) {
        	var jsonObject = $.parseJSON(data);
        	
        	// Copy the new data inside the current form (after where we clicked)
        	if(jsonObject.code>=0)
        	{
        		elementToModified.children().remove();
        		elementToModified.html(htmlspecialchars_decode(jsonObject.result));
        		
        		if(jsonObject.code>0) alert('Another object (ID '+jsonObject.code+') is inactive. Please activate it to use the current object');
        		console.log('[changeChoiceElement] Element '+choiceId+' successfully changed!');
        	}
        	else // An error happened
        		console.error('[changeChoiceElement] Error '+jsonObject.code+' ('+jsonObject.result+')')
        },
        error: function() {
            console.error("[changeChoiceElement] Problem with ID "+elementId);
        },
        // Form data
        data: 'parent='+choiceId+'&child='+chosenElementId,
        // AJAX options
        cache: false,
        contentType: false,
        processData: false
    });
}
