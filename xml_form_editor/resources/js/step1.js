$(document).ready(function(){
	// Moving to the next page
	// TODO Write generic function with AJAX loading...
	$('#tostep2').on('click', {page: 2}, moveTo);
	$('#tostep4').on('click', {page: 4}, moveTo);
	
	$('.edit').on('click', popup);
	
	$('#invisible_message').on('change', null);
});

parseAttr = function(attrString)
{
	console.log('Parsing attributes list...');
		
	resultArray = new Array();
	
	elementsArray = attrString.split(' | ');
	
	elementsArray.forEach(function(element, index, array) {
		console.log('  Attribute '+index+': '+element);
		
		elementInfoArray = element.split(': ');
		resultArray[elementInfoArray[0]] = elementInfoArray[1];
	});
	
	console.log('Attributes parsed');
	
	return resultArray;
};

popup = function()
{
	var elementName = $(this).parent().children(':first-child').text();
	
	var elementId = $(this).parent().children('.hide').text();
	var attributesLocation = $(this).parent().children('.attr');
	
	var attributes = attributesLocation.text();
	var attrArray = parseAttr(attributes);
	
	//console.log(attrArray);
	
	/**
	 * Modalbox configuration 
	 * 
	 */
	// todo add a default attribute
	// todo more configuration available
	// todo recheck data with the current schema (to not alterate datas)
	
	var min_value = 1;
	if(attrArray['MINOCCURS'])
	{
		min_value = attrArray['MINOCCURS'];
	}
	var minOccursField = '<label class="main" for="min">MinOccurs </label><input type="number" class="inform" min="0" value="'+min_value+'" id="min" name="min"/>';
	
	var max_value = 1;
	if(attrArray['MAXOCCURS'])
	{
		max_value = attrArray['MAXOCCURS'];
	}	
	var maxOccursField = '<label class="main" for="max">MaxOccurs </label>';
	var maxOccursUnbounded = '<label class="inform" for="unbounded">Unbounded ? </label>';
	
	if(max_value=='unbounded')
	{
		maxOccursField += '<input type="number" class="inform" min="0" value="1" id="max" name="max" disabled="disabled"/>';
		maxOccursUnbounded += '<input type="checkbox" id="unbounded" name="unbounded" checked="checked" onclick="changeEditionStatus(\'max\')"/>';
	}
	else
	{
		maxOccursField += '<input type="number" class="inform" min="0" value="'+max_value+'" id="max" name="max"/>';
		maxOccursUnbounded += '<input type="checkbox" id="unbounded" name="unbounded" onclick="changeEditionStatus(\'max\')"/>';
	}
	
	
	var dataTypeSelect = '<label class="main" for="type">Data type </label><select id="type" name="type"><option value="integer">Integer</option><option value="double">Double</option><option value="string">String</option></select>';
	var autoGenerateCheckbox = '<label class="main" for="ai">Auto-generate? </label><input type="checkbox" id="ai" name="ai"/>';
	
	var boxForm = '<div id="form_in_box"><div>'+
		minOccursField+'</div><div>'+
		maxOccursField+maxOccursUnbounded+'</div>';
		
	var attrTypeIndex = attributes.indexOf('TYPE: ')
	var typeValue = null;
		
	if(attrTypeIndex!=-1) // There is a TYPE defined in the attributes section 
	{
		// Get the TYPE attribute currently displayed
		var attrSubstr = attributes.substring(attrTypeIndex+6);
		var separatorIndex = attrSubstr.indexOf('|');
		
		typeValue = separatorIndex==-1?attrSubstr:attrSubstr.substring(0, separatorIndex);
		typeValue = $.trim(typeValue);		
		
		//console.log('type value ='+typeValue);
		
		boxForm = boxForm + '<div>' + dataTypeSelect+'</div><div>'+
			autoGenerateCheckbox+'</div>';	
	}	
	
	boxForm = boxForm + 
		'<div><span class="dhtmlx_button"><input type="button" value="Save element" onclick="callback(this,'+elementId+')" style="width:250px;"></span></div>' + 
		'<div><span class="dhtmlx_button"><input type="button" value="Cancel" onclick="callback(this, -1)" style="width:250px;"></span></div></div>';
	
	dhtmlx.modalbox({
		title:"Modifying "+elementName, 
		text:boxForm
	});
	
	if(typeValue!=null)
	{
		//console.log('type value not null');
		
		$('#type option').each(function(index)
		{
			if($(this).attr('value') == typeValue)
				$(this).attr('selected', 'selected');
		});
	}
	
};

callback = function(button, elementId) 
{	
	if(button.value!='Cancel')
	{
		var elementForm = button.parentNode.parentNode.parentNode;
		var formInputs = elementForm.getElementsByTagName('input');
		var formSelects = elementForm.getElementsByTagName('select');
		
		var formValues = new Array();
				
		console.log('Saving...');
		
		for(var inputIndex in formInputs)
		{
			if(!formInputs[inputIndex].disabled && formInputs[inputIndex].outerHTML)
			{				
				switch(formInputs[inputIndex].type)
				{
					case 'number':
						//console.log(formInputs[inputIndex].id+' == '+formInputs[inputIndex].value);
						formValues[formInputs[inputIndex].id] = formInputs[inputIndex].value;
						break;
					case 'checkbox':
						//console.log(formInputs[inputIndex].id+' == '+formInputs[inputIndex].checked);
						formValues[formInputs[inputIndex].id] = formInputs[inputIndex].checked;
						break;
					case 'text':
						// TODO implement this element and other existing input.type
					default:
						break;
				}
			}
		}
		
		for(var selectIndex in formSelects)
		{
			if(!formSelects[selectIndex].disabled && formSelects[selectIndex].outerHTML)
			{				
				//console.log(formSelects[selectIndex].id+' == '+formSelects[selectIndex].value);
				formValues[formSelects[selectIndex].id] = formSelects[selectIndex].value;
			}
		}
		
		console.log(formValues);
		
		// Convert the array into a query string
		var qString = '';		
		for(var key in formValues)
		{
			qString += '&'+key+'='+formValues[key];
		}
		
		//console.log(qString);
		
		// Perform an AJAX reload of the code
		// Update the $_SESSION array in the same time
		changeElement(elementId, qString);	
		
		
		dhtmlx.message(
			"Element successfully saved"
		);
	}
	else
	{
		console.log('Action cancelled');
	}
	
	dhtmlx.modalbox.hide(button);
	
};

/**
 * Save new attributes into the $_SESSION array and display the good values
 */
changeElement = function(elementId, queryString)
{
	var idList = $('.hide')/*.find('.hide')*/;
	//console.log(idList);
	var attrDisplayLocation = null;
	
	idList.each(function(index)
	{
		//console.log($(this).text()+' == '+elementId);
		if($(this).text() == elementId)
		{
			attrDisplayLocation = $(this).parent().children('.attr');
			console.log(attrDisplayLocation);
		}
	});
	
	
	if (window.XMLHttpRequest)
	{
		// Code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{
		// Code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			attrDisplayLocation.html(xmlhttp.responseText);
		}
	};
	
	xmlhttp.open("GET","inc/ajax/changeElement.php?id="+elementId+queryString, true);
	xmlhttp.send();
};

// todo improve code implementation
moveTo = function(event)
{
	if(event.data.page==3)
	{
		//console.log('--step2');
		window.location = 'index.php?step=3';
	}
	
	if(event.data.page==4)
	{
		//console.log('--step2');
		window.location = 'index.php?step=4';
	}
	
	if(event.data.page==2)
	{
		//console.log('--step2');
		window.location = 'index.php?step=2';
	}
	
	if(event.data.page==1)
	{
		//console.log('--step1');
		window.location = 'index.php?step=1';
	}
};