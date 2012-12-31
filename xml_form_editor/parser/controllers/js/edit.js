/**
 * JS to edit element in the configuration view
 * Script version: 1.0
 * Author: P.Dessauw
 * 
 */


loadEditController = function()
{
	/**
	 * Dialog basic configuration 
	 */
	$( "#dialog" ).dialog({
        autoOpen: false,
        show: "blind",
        hide: "blind",
        height: 330,
        width: 300,
        modal: true,
        resizable: false,
        /*position: {my: "center", at: "right top", of: window},*/
        /*open: function(event, ui){
     		setTimeout("$('#dialog').dialog('close')",3000);
    	},*/
        buttons: {
            "Save element": function() {
            	var minOccurs = $('#minoccurs').val(),
					maxOccurs = $('#maxoccurs').is(':disabled')?'-1':$('#maxoccurs').val(),
					dataType = $('#datatype').val(),
					autoGen = $('#autogen').val(),
					pattern = $('#pattern').val();
            	        	            	
            	valid = checkOccurence(parseInt(minOccurs), parseInt(maxOccurs));
            	/*console.log(minOccurs+' <= '+maxOccurs+' ? '+valid);
            	console.log(dataType+' '+autoGen+' '+pattern);*/
            	
            	if(valid)
            	{
            		allFields = new Array();
            		allFields['minOccurs'] = minOccurs;
            		allFields['maxOccurs'] = maxOccurs;
            						
            		if(!$('#datatype-part').is(':hidden'))
            		{
            			allFields['dataType'] = dataType;
            			allFields['autoGen'] = autoGen;
            			allFields['pattern'] = pattern;
            		}
            		
            		//console.log(allFields);
            		saveConfiguration($('.elementId').text(), allFields);
            		  		
            		$( this ).dialog("close");
            	}
            },
            Cancel: function() {
                $(this).dialog("close");
            }
        },
        close: clearFormData
    });
	
	// Linking the event on all the edit buttons
	$('.edit').live('click', editElement);
	
	// Event on the dialog element
	$('#unbounded').on('click', changeUnboundedState);
	$('#minoccurs').on('focus', removeErrorDisplay);
	$('#maxoccurs').on('focus', removeErrorDisplay);
}

/**
 * Function to call the PHP script and replace the current element 
 * @param event Handle the JSON string put in parameter
 * 
 */
editElement = function()
{
	var elementId = $(this).parent().attr('id');
	var elementName = $(this).siblings('.element_name').text();
	var elementAttr = $(this).siblings('.attr').text();

	// Title configuration	
	$('.ui-dialog-title').text('Edit '+elementName);
	$('.elementId').text(elementId);
	
	/*
	 * Datatype configuration
	 */
	if((typeIndex = elementAttr.indexOf('TYPE'))==-1)
	{
		$('#datatype-part').hide();
		$('#autogen-part').hide();
		
		$("#dialog").dialog( "option", "height", 260 );
	}
	else
	{
		$('#datatype-part').show();
		$('#autogen-part').show();
		
		// Set the data type value
		var dataTypeValue = elementAttr.substring(typeIndex+5);
		var separatorIndex = dataTypeValue.indexOf(' |');
		if(separatorIndex!=-1) dataTypeValue = dataTypeValue.substring(0, separatorIndex);
		
		$('#datatype').val(dataTypeValue);
		
		$("#dialog").dialog( "option", "height", 330 );
	}
	
	/*
	 * MinOccurs input configuration
	 */
	if((min = elementAttr.indexOf('MINOCCURS'))==-1)
	{
		$('#minoccurs').val(1);
	}
	else
	{
		var minValue = elementAttr.substring(min+11);
		var separatorIndex = minValue.indexOf(' |');
		if(separatorIndex!=-1) minValue = minValue.substring(0, separatorIndex);
		
		//console.log('MINOCCURS: '+minValue);
		
		$('#minoccurs').val(minValue);
	}
	
	/*
	 * MaxOccurs input configuration
	 */
	if((max = elementAttr.indexOf('MAXOCCURS'))==-1)
	{
		$('#maxoccurs').val('1');
	}
	else
	{
		var maxValue = elementAttr.substring(max+11);
		var separatorIndex = maxValue.indexOf(' |');
		if(separatorIndex!=-1) maxValue = maxValue.substring(0, separatorIndex);
		
		//console.log('MAXOCCURS: '+maxValue);
		
		if(maxValue=='unbounded')
		{
			$('#maxoccurs').val('1');
			$('#maxoccurs').attr('disabled', 'disabled');
			$('#unbounded').attr('checked', 'checked');
		}
		else 
		{
			$('#maxoccurs').val(maxValue);
		}
	}
	
	/*
	 * Auto-generate configuration
	 */
	if(elementAttr.indexOf('AUTO_GENERATE')==-1)
	{
		$('#autogen').val('false');
	}
	
	// Opens the dialog
	$("#dialog").dialog( "open" );
}

/**
 * Function to disabled the maxOccurs input if the unbounded checkbox is checked and to re-enable it when it is unchecked 
 */
changeUnboundedState = function()
{
	if($(this).is(':checked'))
	{
		if($("#maxoccurs").is(':enabled')) $("#maxoccurs").attr('disabled', 'disabled');
	}
	else
	{
		if($("#maxoccurs").is(':disabled')) $("#maxoccurs").removeAttr('disabled');
	}
}

/**
 * Function to remove the error classes and display the form as it originally was
 */
removeErrorDisplay = function()
{
	$(this).removeClass('ui-state-error');
	$(this).siblings('label').removeClass('ui-state-error-text');
}

/**
 * Clear the form errors
 */
clearFormData = function()
{
	$('.tip').removeClass('ui-state-error');
	$('.tip').html('');
	
	$('label[for=minoccurs]').removeClass('ui-state-error-text');
	$('label[for=maxoccurs]').removeClass('ui-state-error-text');
	$('#minoccurs').removeClass('ui-state-error');
	$('#maxoccurs').removeClass('ui-state-error');
}

/**
 *
 */
saveConfiguration = function(elementId, fieldArray)
{
	qString = '';
	var length = Object.keys(fieldArray).length;
	
	for(var fieldName in fieldArray)
	{
		length--;
		
		qString += fieldName+'='+fieldArray[fieldName];
		if(length>0) qString += '&';
	}
	
	//console.log(qString);
	
	$.ajax({
        url: 'parser/controllers/php/editSchema.php',
        type: 'GET',
        success: function(data) {
        	var jsonObject = $.parseJSON(data);
        	
        	// Copy the new data inside the current form (after where we clicked)
        	if(jsonObject.code==0)
        	{
        		$('li#'+elementId).children().not('ul').remove();
        		
        		if($('li#'+elementId).children(':first').length!=0) $('li#'+elementId).children(':first').before(htmlspecialchars_decode(jsonObject.result));
        		else $('li#'+elementId).html(htmlspecialchars_decode(jsonObject.result));
        		
        		console.log('[saveConfiguration] Element '+elementId+' successfully modified');
        	}
        	else if(jsonObject.code<0)
        	{
        		console.error('[saveConfiguration] Error '+jsonObject.code+' ('+jsonObject.result+') occured while saving configuration of ID'+elementId);
        	}
        },
        error: function() {
            console.error("[saveConfiguration] Problem with ID "+elementId);
        },
        // Form data
        data: 'id='+elementId+'&'+qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}


/**
 * Change the tip at the top of the form
 */
updateTip = function (tipText) {
	if($('.tip').text()=='')
	{
		var height = $("#dialog").dialog("option", "height");
		$("#dialog").dialog("option", "height", height+50);
	}
	
	$('.tip')
	    .html('<span class="ui-icon ui-icon-alert" style="display:inline-block"></span> '+tipText)
	    .addClass("ui-state-error");
}

/**
 * Control function to check if minOccurs et maxOccurs contains the right values 
 */
checkOccurence = function(min, max)
{
	var minInput = $('#minoccurs'),
		minLabel = $('label[for=minoccurs]'),
		maxInput = $('#maxoccurs'),
		maxLabel = $('label[for=maxoccurs]');
		
	//console.log('[edit.js][checkOccurence] min: '+min+';max: '+max);
	
	if(min>=0 && max>=-1)
	{
		if(max==-1) return true;
		else
		{
			if(max >= min) return true;
			else
			{
				minInput.addClass( "ui-state-error" );
				minLabel.addClass( "ui-state-error-text" );
				maxInput.addClass( "ui-state-error" );
				maxLabel.addClass( "ui-state-error-text" );
				updateTip('MinOccurs must be lower than MaxOccurs');
				
				return false;
			} 
		}
	}
	else
	{
		minInput.addClass( "ui-state-error" );
		minLabel.addClass( "ui-state-error-text" );
		maxInput.addClass( "ui-state-error" );
		maxLabel.addClass( "ui-state-error-text" );
		updateTip('MinOccurs and/or MaxOccurs do not contains the right values');
		
		return false;
	} 
}
