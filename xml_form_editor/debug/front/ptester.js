$(document).ready(function(){
	// Linking the click event the refresh button
	$('.refresh.form').on('click', refreshForm);
	$('.save.file').on('click', saveFile);
	$('.refresh.conf').on('click', refreshConf);
	$('.save.data').on('click', saveData);
	$('.encode.data').on('click', encodeData);
	$('.save.mongodb').on('click', saveMongodb);
	$('.retrieve.data').on('click', retrieveData);
	$('.xsdman.choice').live('change', changeChoiceQuery);
	$('.retrieve.query').on('click', retrieveQuery);
	$('.add').live('click', {action: 0}, addRemoveItem);
	$('.remove').live('click', {action: 1}, addRemoveItem);
});

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
        url: 'back/addRemoveItems.php',
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
	    return string.charAt(0).toLowerCase() + string.slice(1);
	}
	
	inputs.each(function()
	{
		var queryPath = unCapitaliseFirstLetter($(this).prev().text()),
			//match = '',
		match = $(this).val(),
			currentElement = $(this).prev();
		
		/*if ($(this).attr('class') == 'xsdman restriction query') {
			match = $(this).val();
		}
		
		if ($(this).attr('class') == 'text query') {
			match = $(this).val();
		}*/
		
		if(match != '' && match != 'empty')
		{
			while (currentElement.parent().parent().prev().length) {
				currentElement = currentElement.parent().parent().prev();
				if (currentElement.attr('class') != 'xsdman choice')
					queryPath = unCapitaliseFirstLetter(currentElement.text())+'.'+queryPath;
			}
			
			qString += queryPath+'.$='+match+'&';
		}
	});
	
	qString = qString.substring(0, qString.length-1);
	
	$.ajax({
        url: 'back/queryData.php',
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
        url: 'back/changeDisplayedQuery.php',
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

/**
 * 
 */
retrieveData = function()
{
	var match = $('#query_target').val();
	var query = $('#query_element').find(':selected').attr('value');
	$.ajax({
		url: 'back/queryData.php',
		type: 'GET',
		success: function(data) {
			$('#query_result').html(data);
		},
		error: function() {
			console.error("[retrieveData] Problem with AJAX call");
		},
		data: 'match='+match+'&query='+query,
		//Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
	});
}

/**
 * 
 */
saveMongodb = function()
{
	var encodeType = $('#encode_data').find(':selected').attr('value');
	$.ajax({
		url: 'back/saveMongodb.php',
		type: 'GET',
		success: function(data) {
		
		},
		error: function() {
			console.error("[saveMongodb] Problem with AJAX call");
		},
		data: 'encode='+encodeType,
		//Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
	});
}

/**
 * 
 */
encodeData = function()
{
	var encodeType = $('#encode_data').find(':selected').attr('value');
	$.ajax({
		url: 'back/encode.php',
		type: 'GET',
		success: function(data) {
			$('#encode_result').text(data);
		},
		error: function() {
			console.error("[encodeData] Problem with AJAX call");
		},
		data: 'encode='+encodeType,
		//Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
	});
}

/**
 * 
 */
refreshForm = function()
{
	var htmlFormTitle = $(this).parent();
	console.log('[refreshForm] Refreshing form ...');
	
	$.ajax({
        url: 'debug/back/generateForm.php',
        type: 'GET',
        success: function(data) {
        	htmlFormTitle.next().next().remove();
        	htmlFormTitle.next().after(data);
        	
        	console.log('[refreshForm] Form successfully refreshed...');
        },
        error: function() {
            console.error("[refreshForm] Problem with the AJAX call");
        },
        // Form data
        //data: 'id='+elementId+'&'+qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
saveFile = function()
{
	var fileName = $('#schema_file').find(':selected').text();
	var pageNumber = $('#page_number').attr('value');
	
	console.log('[refreshFile] Loading '+fileName+' (in '+pageNumber+' page(s))...');
	
	$.ajax({
        url: 'debug/back/loadFile.php',
        type: 'GET',
        success: function(data) {
        	// Destroy and remove the dialog to avoid to rewrite on it
        	$( "#dialog" ).dialog("destroy");
        	$( "#dialog" ).remove();
        	// Destroy all element written
			$('#cfg_view').children(':first').next().remove();
        	
        	// Write the new content after the header  	
        	$('#cfg_view').children('h3').after(data);
        	
        	loadEditController();
        	
        	alert('Configuration saved!');
        },
        error: function() {
            console.error("[refreshFile] Problem with the AJAX call");
        },
        // Form data
        data: 'f='+fileName+'&p='+pageNumber,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
refreshConf = function()
{
	console.log('[refreshConf] Refreshing configuration...');
	
	$.ajax({
        url: 'debug/back/loadFile.php',
        type: 'GET',
        success: function(data) {
        	// Destroy and remove the dialog to avoid to rewrite on it
        	$( "#dialog" ).dialog("destroy");
        	$( "#dialog" ).remove();
        	// Destroy all element written
			$('#cfg_view').children(':first').next().remove();
        	
        	// Write the new content after the header  	
        	$('#cfg_view').children('h3').after(data);
        	
        	loadEditController();
        },
        error: function() {
            console.error("[refreshConf] Problem with the AJAX call");
        },
        // Form data
        //data: 'f='+fileName,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
saveData = function()
{
	console.log("[saveData] Saving fields...");
	
	var inputs = $('input.text'),
		qString = '';
	
	inputs.each(function()
	{
		var inputId = $(this).parent().attr('id'),
			inputValue = $(this).attr('value');
		
		if(inputValue != '' && !isNaN(parseInt(inputId)))
		{
			console.log('Id '+parseInt(inputId)+' = '+inputValue);
			qString += parseInt(inputId)+'='+inputValue+'&';
		}	
	});
	
	qString = qString.substring(0, qString.length-1);
	
	$.ajax({
        url: 'debug/back/saveData.php',
        type: 'GET',
        success: function(data) {
        	
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