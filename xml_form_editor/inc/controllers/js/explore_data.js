/**
 * 
 */
loadExploreDataController = function()
{
	//TODO Remove the live for a on to manage events
	$('.xsdman.choice').live('change', changeChoiceQuery);
	$('.submit.query').on('click', retrieveQuery);
	$('.add').live('click', {action: 0}, addRemoveItem);
	$('.remove').live('click', {action: 1}, addRemoveItem);
	$(document).on('click', '.download', downloadXML);
	
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
	
	inputs.each(function()
	{
		var element = $(this),
			match = $(this).val(),
			range = $(this).hasClass('less') ? 'lte' : ($(this).hasClass('greater') ? 'gte' : ''),
			option = ($(this).hasClass('radio') ? ($(this).attr('checked') ? match : null) : ''),
			elementId = null;
		
		//console.log(range);
		if (option != '') {
			while (elementId == null) {
				element = element.next();
				elementId = element.attr('id');
			}
			//console.log(elementId);
		}
		else if (range == '') {
			elementId = $(this).parent().attr('id');
		}
		else {
			elementId = $(this).parent().parent().attr('id');
		}
		
		
		if(match != '' && match != 'empty' && option != null)
		{
			if (range != '') {
				switch (range) {
				case 'lte':
					qString += range+elementId+'='+match+'&';
					console.log('less');
					break;
				case 'gte':
					qString += range+elementId+'='+match+'&';
					console.log('greater');
					break;
				default:
					console.error("Undefined range "+range);
					break;
				}
			}
			else if (option != '') {
				qString += match+'='+elementId+'&';
			}
			else {
				qString += elementId+'='+match+'&';
			}
		}
	});
	
	qString = qString.substring(0, qString.length-1);
	
	$.ajax({
        url: 'inc/controllers/php/queryData.php',
        type: 'GET',
        success: function(data) {
        	var xmlHolderElement = GetParentElement('XMLContainer');
    		while (xmlHolderElement.childNodes.length) { 
    			xmlHolderElement.removeChild(xmlHolderElement.childNodes.item(xmlHolderElement.childNodes.length-1));
    		}
        	if (data != "empty") {
        		var jsonObject = $.parseJSON(data);
        		$.each(jsonObject, function(index) {
        			$('#XMLContainer').append('<div id="XMLHolder'+index+'"></div>');
        			LoadXMLString('XMLHolder'+index, htmlspecialchars_decode($(this).get(0).data));
        		});
        		$('#download').html("<button class='btn download pull-right'><i class='icon-arrow-down'></i> Download XML</button>");
        	}
        	else {
        		$('#XMLContainer').html("<div class='icon invalid'></div><span>Empty result for the query</span>");
        	}
        },
        error: function() {
            console.error("[retrieveQuery] Problem with the AJAX call");
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
        		console.error('[changeChoiceQuery] Error '+jsonObject.code+' ('+jsonObject.result+')')
        },
        error: function() {
            console.error("[changeChoiceQuery] Problem with ID "+elementId);
        },
        // Form data
        data: 'parent='+choiceId+'&child='+chosenElementId,
        // AJAX options
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
downloadXML = function() {
	
	console.log('[downloadXML] Downloading XML for the previous query...');
	
	window.location = 'inc/controllers/php/downloadQuery.php';
	
	console.log('[downloadXML] XML downloaded');
}

