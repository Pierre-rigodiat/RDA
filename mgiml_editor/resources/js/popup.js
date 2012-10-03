/*
 * TODO Use JQuery and the JMessage lib to generate pop-ups
 */

function configurePopUp(attributes)
{
	maxValue=1;
	minValue=1;
	elementId=-1;
	type=null;
	
	attrArray = unserialize(attributes);
	
	/**
	 * Reads the attribute list and store element into propers value
	 */
	for(attrName in attrArray)
	{
		attrValue = attrArray[attrName];

		console.log(attrName+'='+attrValue);
		
		if(attrName=='NAME')
		{
			console.log('Modifying pop-up name...');
			changePopUpName(attrValue);
		}
		else if(attrName=='TYPE' && attrValue.split(':')[0]=="xsd")
		{
			type=attrValue.split(':')[1];
			console.log('type='+type);
		}
		else if(attrName=='MAXOCCURS')
		{
			if(attrValue=="unbounded")
			{
				maxValue=-1;
			}
			else
			{
				maxValue=attrValue;
			}
		}
		else if(attrName=='MINOCCURS')
		{
			minValue=attrValue;
		}
		else if(attrName=='id')
		{
			id=attrValue;
		}
		
	}

	console.log('min='+minValue);
	console.log('max='+maxValue);
	
	document.getElementById('elementId').value = id;
	document.getElementById('min').setAttribute("value", minValue);

	if(maxValue=="-1")
	{
		document.getElementById('unbounded').checked=true;
		document.getElementById('max').setAttribute("disabled", "disabled");
	}
	else
	{
		document.getElementById('max').setAttribute("value", maxValue);
	}

	if(type!=null)
	{
		console.log('type='+type);

		document.getElementById('type').removeAttribute("disabled");
		document.getElementById('ai').removeAttribute("disabled");

		switch(type)
		{
			case 'string':
				document.getElementById('type').value = 'str';
				break;
			case 'integer':
				document.getElementById('type').value = 'int';
				break;
			case 'double':
				document.getElementById('type').value = 'dbl';
				break;
			default:
				document.getElementById('type').value = '';
				break;
		}
	}
	else
	{
		console.log('type null - uneditable content');
		
		document.getElementById('type').setAttribute("disabled", "disabled");
		document.getElementById('ai').setAttribute("disabled", "disabled");
	}
}


function changePopUpName(name)
{
	document.getElementById('popup_title').innerHTML=name+' configuration';
}

function changeEditionStatus(elementId)
{
	if(document.getElementById(elementId).hasAttribute("disabled"))
	{
		document.getElementById(elementId).removeAttribute("disabled");
	}
	else
	{
		document.getElementById(elementId).setAttribute("disabled", "disabled");
	}
}