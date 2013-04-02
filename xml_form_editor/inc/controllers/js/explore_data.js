/**
 * 
 */
loadExploreDataController = function()
{
	$('.xsdman.choice').live('change', changeChoiceQuery);
	$('.retrieve.query').on('click', retrieveQuery);
	$('.add').live('click', {action: 0}, addRemoveItem);
	$('.remove').live('click', {action: 1}, addRemoveItem);
}

/**
 * 
 */
addRemoveItem = function(event)
{
	var elementId = $(this).parent().attr('id');
	var clickedElement = $(this).parent().parent().parent();
	clickedElement = clickedElement.attr('id')=='page_content'?clickedElement.children(':first'):clickedElement;
	
	var clickedElementParent = clickedElement.parent();
	
	var actionType = 'a';
	if(event.data.action==1) actionType = 'r';
	
	console.log('[addRemoveItem] Function has been called with actionType "'+actionType+'" and ID '+elementId);
	
	//TODO Save the current values in the form
	
	$.ajax({
        url: 'inc/controllers/php/addRemoveItems.php',
        type: 'GET',
        success: function(data) {
        	var jsonObject = $.parseJSON(data);
        	
        	// Copy the new data inside the current form (after where we clicked)
        	if(jsonObject.code>=0)
        	{
        		clickedElement.remove();
        		clickedElementParent.html(htmlspecialchars_decode(jsonObject.result));
        		
        		if(jsonObject.code>0) alert('Another object (ID '+jsonObject.code+') is inactive. Please activate it to use the current object');
        		console.log('[addRemoveItem] Element '+elementId+' successfully modified');
        	}
        	else // An error happened
        		console.error('[addRemoveItem] Error '+jsonObject.code+' ('+jsonObject.result+')')
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

/**
 * 
 */
retrieveQuery = function()
{
	console.log("[retrieveQuery] Query send...");
	
	var inputs = $('.query_element'),
		qString = '';
	
	function unCapitaliseFirstLetter(string)
	{
		if (string != null)
			return string.charAt(0).toLowerCase() + string.slice(1);
		else
			return '';
	}
	
	inputs.each(function()
	{
		var queryPath = unCapitaliseFirstLetter($(this).prev().text()),
		match = $(this).val(),
		currentElement = $(this).prev();
		
		if(match != '' && match != 'empty')
		{
			while (currentElement.parent().parent().siblings(':first').length) {
				currentElement = currentElement.parent().parent().siblings(':first');
				if (currentElement.next().attr('class') != 'xsdman choice')
					queryPath = unCapitaliseFirstLetter(currentElement.text())+'.'+queryPath;
			}
			
			qString += queryPath+'.$='+match+'&';
		}
	});
	
	qString = qString.substring(0, qString.length-1);
	
	$.ajax({
        url: 'inc/controllers/php/queryData.php',
        type: 'GET',
        success: function(data) {
        	$('#query_result').html(data);
        },
        error: function() {
            console.error("[saveData] Problem with the AJAX call");
        },
        // Form data
        data: qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
	
	console.log('qString = '+qString);
}

/**
 * 
 */
changeChoiceQuery = function()
{
	var choiceId = $(this).parent().attr('id'),
		chosenElementId = $(this).find(':selected').val(),
		elementToModified = $(this).next();
	
	console.log('Choice ID '+choiceId+' has changed to display elementId '+chosenElementId+' (orig)...');
	
	$.ajax({
        url: 'inc/controllers/php/changeDisplayedQuery.php',
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