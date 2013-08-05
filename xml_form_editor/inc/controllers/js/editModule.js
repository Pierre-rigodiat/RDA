/**
 * JS to edit the module to use in the query configuration view.
**/
loadQueryEditController = function()
{
	/* Remove the editController to avoid multi-event */
	removeQueryEditController();
	
	/**
	 * Dialog basic configuration 
	 */
	$( "#dialog" ).dialog({
        autoOpen: false,
        show: "blind",
        hide: "blind",
        height: 360,
        width: 300,
        modal: true,
        resizable: false,
        /*position: {my: "center", at: "right top", of: window},*/
        /*open: function(event, ui){
     		setTimeout("$('#dialog').dialog('close')",3000);
    	},*/
        buttons: {
            "Save element": function() {
            	var module = $('#module').val();
            	
        		allFields = new Array();
        		
        		allFields['module'] = module;
        		
        		console.log(allFields);
        		saveQueryConfiguration($('.elementId').text(), allFields);
        		  		
        		$( this ).dialog("close");
        		
            },
            Cancel: function() {
                $(this).dialog("close");
            }
        }
    });
	
	// Linking the event on all the edit buttons
	$(document).on('click', '.edit', editQueryElement);

}

/**
 * 
 */
removeQueryEditController = function()
{	
	$(document).off('click', '.edit');
	
	if($('#dialog').is(':ui-dialog')) $('#dialog').dialog("destroy");
}

/**
 * Function to call the PHP script and replace the current element 
 * @param event Handle the JSON string put in parameter
 * 
 */
editQueryElement = function()
{
	var elementId = $(this).parent().attr('id');
	var elementName = $(this).siblings('.element_name').text();
	var elementAttr = $(this).siblings('.attr').text();

	console.log('[editQueryElement] Editing ID '+elementId);

	// Title configuration	
	$('.ui-dialog-title').text('Edit '+elementName);
	$('.elementId').text(elementId);
	
	console.log('[editQueryElement] Element ID set '+$('.elementId').text());
	
	/*
	 * Module configuration
	 */
	if((module = elementAttr.indexOf('MODULE'))==-1)
	{
		$('#module').val('false');
	}
	else
	{
		var moduleValue = elementAttr.substring(module+8);
		
		$('#module').val(moduleValue);
	}
	
	// Opens the dialog
	$("#dialog").dialog( "open" );
}

/**
 * Saves the new configuration of the element edited
 * This function is called when the user clicks on "Save element"
 */
saveQueryConfiguration = function(elementId, fieldArray)
{
	qString = '';
	var length = Object.keys(fieldArray).length;
	
	for(var fieldName in fieldArray)
	{
		length--;
		
		qString += fieldName+'='+fieldArray[fieldName];
		if(length>0) qString += '&';
	}
	
	console.log('[saveQueryConfiguration] editSchema.php called with query string '+qString);
	
	$.ajax({
        url: 'inc/controllers/php/editQueryDisplay.php',
        type: 'GET',
        success: function(data) {
        	var jsonObject = $.parseJSON(data);
        	
        	// Copy the new data inside the current form (after where we clicked)
        	if(jsonObject.code==0)
        	{
        		$('li#'+elementId).children().not('ul').remove();
        		
        		$('li#'+elementId).html(htmlspecialchars_decode(jsonObject.result));
        		
        		console.log('[saveQueryConfiguration] Element '+elementId+' successfully modified');
        	}
        	else if(jsonObject.code<0)
        	{
        		console.error('[saveQueryConfiguration] Error '+jsonObject.code+' ('+jsonObject.result+') occured while saving configuration of ID'+elementId);
        	}
        },
        error: function() {
            console.error("[saveQueryConfiguration] Problem with ID "+elementId);
        },
        // Form data
        data: 'id='+elementId+'&'+qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}
