/**
 * JS to add or remove items in the html form
 * Script version: 1.0
 * Author: P.Dessauw
 * 
 */
$(document).ready(function(){
	// We need to use .live() method here because of the newly created elements
	// Linking the event on all the + buttons
	$('.add').live('click', {action: 0}, addRemoveItem);

	// Linking the event on all the - buttons
	$('.remove').live('click', {action: 1}, addRemoveItem);
});

/**
 * Function to call the PHP script and replace the current element 
 * @param event Handle the JSON string put in parameter
 * 
 */
addRemoveItem = function(event)
{
	var elementId = $(this).parent().attr('id');
	var clickedElement = $(this).parent().parent().parent();
	var clickedElementParent = clickedElement.parent();
	
	var actionType = 'a';
	if(event.data.action==1) actionType = 'r';
	
	console.log('[addRemoveItem] Function has been called with actionType "'+actionType+'" and ID '+elementId);
	
	//TODO Save the current values in the form
	
	$.ajax({
        url: 'parser/controllers/php/treeAction.php',
        type: 'GET',
        success: function(data) {
        	var jsonObject = $.parseJSON(data);
        	
        	// Copy the new data inside the current form (after where we clicked)
        	if(jsonObject.code>=0)
        	{
        		clickedElement.remove();
        		clickedElementParent.html(htmlspecialchars_decode(jsonObject.result));
        		
        		if(jsonObject.code>0) alert('Another object (ID '+jsonObject.code+') is inactive. Please activate it to use the current object');
        	}
        	
        	console.log('[addRemoveItem] Element '+elementId+' successfully modified');
        },
        error: function() {
            console.error("[addRemoveItem] Problem with ID "+elementId);
        },
        // Form data
        data: 'action='+actionType+'&id='+elementId,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}
