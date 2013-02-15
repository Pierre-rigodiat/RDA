$(document).ready(function(){
	// Linking the event on all the + buttons
	//$('.addItem').on('click', addItem);

	// Adding the event on all the - buttons
	//$('.removeItem').on('click', removeItem);
	/*$('#tostep1').on('click', {page: 1}, moveTo); xxx not needed anymore... */
	
	$('.autogen').on('click', generateRandomValue);
	
	$('.reset').on('click', resetForm);
});

resetForm = function() {
	alert("Not yet implemented");
};

// TODO make it server-side
function generate(length, number, lower, upper, special) {
	var result = "";
	
	if(number || lower || upper || special)
	{
		var iteration = 0;
		var randomNumber;
		
		if(special == undefined)
		{
			var special = false;
		}
		
		while(iteration < length)
		{
			randomNumber = (Math.floor((Math.random() * 100)) % 94) + 33;
			
			if(!special){
				if ((randomNumber >=33) && (randomNumber <=47)) { continue; }
				if ((randomNumber >=58) && (randomNumber <=64)) { continue; }
				if ((randomNumber >=91) && (randomNumber <=96)) { continue; }
				if ((randomNumber >=123) && (randomNumber <=126)) { continue; }
			}
			
			if(!number) 
			{
				if ((randomNumber >=48) && (randomNumber <=57)) { continue; }
			}
			
			if(!lower)
			{
				if ((randomNumber >=97) && (randomNumber <=122)) { continue; }
			}
			
			if(!upper)
			{
				if ((randomNumber >=65) && (randomNumber <=90)) { continue; }
			}
			
			iteration++;
			result += String.fromCharCode(randomNumber);
		}
	}
	
	return result;
}

generateRandomValue = function() {
	var inputs = $(this).parent().children('input');
	//console.log(inputs);
	
	var inputClass = $(this).attr('class').split(' ');
	//console.log(inputClass[1]);
	
	var nbr = true;
	var chr = false;
	var spe = false;
	
	if(inputClass[1]=='string') chr = true;
	
	var value = generate(10, nbr, chr, chr);
	
	// Modify the 2 first inputs
	inputs.each(function(index) {
		if(index<2)
		{
			$(this).attr('value', value);
		}
	});
};

/**
 * Remove item function
 */
/*removeItem = function()
{	
	if($(this).css("color")!='rgb(128, 128, 128)') // XXX Not really reliable...
	{
		//console.log('-- Remove item --');

		// XXX We need to add the + button

		var htmlToRemove = $(this).parent().parent();
		
		// Parse the xpath to get to the ajax script
		var clickXpath = getElementXPath(htmlToRemove.get(0));
		clickXpath = clickXpath.split("/form")[1];
		
		var treeArray = clickXpath.split('/ul/li');
		
		for(index in treeArray)
		{
			if(treeArray[index]=='') treeArray[index]=0;
			else
			{
				treeArray[index] = parseInt(treeArray[index].slice(1, treeArray[index].length-1))-1;
			}
		}
		
		var clickPath = treeArray.toString().replace(/,/g, '/');
		
		//console.log(htmlToRemove[0]);

		var maxoccurs = 1;
		var minoccurs = 1;

		$(this).parent().find(':hidden').each(function() {
			switch($(this).attr('name'))
			{
				case 'minoccurs':
					minoccurs = $(this).attr('value');
					break;
				case 'maxoccurs':
					if($(this).attr('value') == 'unbounded') maxoccurs = -1;
					else maxoccurs = $(this).attr('value');
					break;
				default:
					break;
			}			
		});

		console.log('minoccurs: '+minoccurs+'; maxoccurs: '+maxoccurs);

		var elementXPath = getElementXPath(htmlToRemove.get(0));
		var elementId = $(this).parent().attr('class');

		/*console.log('Element ID = '+elementId);
		console.log('Element XPath = '+elementXPath);*/

		/*var previousElement = null;
		var previousId = -1;
		var nextElement = null;
		var nextId = -1;

		if(elementXPath.match(/\[[0-9]+\]$/))
		{
			// The element is not the first one of the list
			// We compute the next and previous XPath to get the next and previous element
			var index0 = elementXPath.lastIndexOf('[');
			var index1 = elementXPath.lastIndexOf(']');

			var elementIndex = parseInt(elementXPath.slice(index0+1, index1));			
			//console.log('Element is the '+elementIndex+' one of the list');

			var previousXPath = elementXPath.slice(0, index0)+'['+(elementIndex-1)+']';
			var nextXPath = elementXPath.slice(0, index0)+'['+(elementIndex+1)+']';

			/*console.log('Previous XPath: '+previousXPath);
			console.log('Next XPath: '+nextXPath);*/

			/*previousElement = $(getElementsByXPath($(document).get(0), previousXPath));
			nextElement = $(getElementsByXPath($(document).get(0), nextXPath));

			allElement = $(getElementsByXPath($(document).get(0), elementXPath.slice(0, index0)));
		}
		else
		{
			// For the first element of the list we only need to check the next element
			//console.log('This is the first element of the list');

			nextElement = $(getElementsByXPath($(document).get(0), elementXPath+'[2]'));

			allElement = $(getElementsByXPath($(document).get(0), elementXPath));
		}

		/*console.log(previousElement);
		console.log(nextElement);*/

		/*var siblingElementNumber = allElement.find('.'+elementId).length;

		//console.log(siblingElementNumber+' brother(s) before deleting');

		if(siblingElementNumber > minoccurs)
		{
			if(previousElement!=null)
			{
				previousId = previousElement.children().attr('class');
				//console.log('Previous ID = '+previousId);
			}

			if(nextElement!=null)
			{
				nextId = nextElement.children().attr('class');
				//console.log('Next ID = '+nextId);
			}

			if(nextId == elementId || previousId == elementId)
			{
				//console.log('Another similar element exists');

				if(siblingElementNumber - 1 == minoccurs)
				{
					console.log('Min element reached, remove button will be deleted');

					allElement.find('.'+elementId).each(function() {
						$(this).find('.removeItem').remove();
						/*var removeButton = $(this).find('.removeItem');

						removeButtons.push(removeButton.clone(true));
						removeButton.remove();*/
					/*});
				}

				htmlToRemove.remove();
			}
			else
			{
				var parent = $(this).parent();

				if(parent.find('.addItem').length==0)
				{
					//console.log('Adding the + button...');

					parent.append(' <img src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACUUlEQVQokZWSX2hScRTHz9W5uZlzms02nH82wv3PKFeO5qAYQqOHHlrPg156ihZE0J/XInqKvQhBDwU9VC+VyCzb+rNyNEJxstqmd7pdU3N679V7U3/3Tw+7SMIe6rwd+J7z+XK+BxNFEf6nGv5uSDYXTS2Hk0GSLfACr1So7CbnEZNTrzbUNFiNsJYOz0Wf6zTttg57c+O+Kl/Nlogv64Eyg84fmz5qcdYNrKXDr8KPD3ePHjIMx6i1NLuNBKRp1LS3GBd/+NY34xddl0e6T0qWSDbnjz4bsDis7f2BbS/LsEjklMomBpU2i7Eh8/Hib/rRh1nT/u6Dmk4ZAKwQXxuUSsuBvk+pt2VUZhF7ZeTWpeFrVCWfp9LB1PwJ2ykSZRdW/QAgA4BwcslssH0vRHJ0jmYpiins2iXwZLXMMPTONoWP9o75V7ySpTyT61eoEjSOhPJ1593aQWanngLAjHeKIGODekeaCkgEjucYRJeqFJKjPW8v8gIGIsdzEqGlSU3kE6omNcnmZ95NM79oz4UXu7sBQIbJO1vNyQyubdFJBLvJGcKDJpVVRBWM57RtqtpugQdMxLo0Vl/ozcTgpJRDrpi557upVMsdPeOLuI8XOF7gBB4DEBVy+XjP5FzodZxIeaafGHUmKbhl/LNn/r5e3zbWO7FF4gQZFwXBqO0xasy+0MvIxsbtc3dOD7jrXmMp9vHh+wc7lYyrz2Vo7QCArXzC/y3QiKmunrmxq64bAICfJLGw6p+LeLN0hhdQa7PWPXTWPTzZpTPv8Xz/WH8AA8ItNSarPAgAAAAASUVORK5CYII=" alt="add" class="addItem">');
					parent.find('.addItem').on('click', addItem);
				}

				htmlToRemove.wrapInner('<div class="unavailable">');
				htmlToRemove.find(':input').attr('disabled', true);

				//removeButtons.push($(this).clone(true));
				$(this).remove();
			}
			
			console.log('Register new - click -> '+clickPath);
			registerAction('r', clickPath);
		}
		else
		{
			console.log('You can\'t delete this element');
		}
	}
	else
	{
		var unavailableElement = $(this).parent().parent().parent();
		//var unavailableElement = $(this).parent().parent().parent().parent();

		while(!unavailableElement.hasClass('unavailable'))
		{
			console.log(unavailableElement);
			unavailableElement = unavailableElement.parent();
		}

		console.log(unavailableElement);

		//var elementId = unavailableElement.children().attr('class'));

		var index = unavailableElement.text().indexOf(' ');

		editionUnavailableBox(unavailableElement.text().slice(0, index), unavailableElement);
	}
};

/**
 * Edition unavailable for an element
 */
editionUnavailableBox = function(elementName, element)
{
	dhtmlx.modalbox({ 
		type:"confirm",
		title:"Element unavailable", 
		text:"<img src='alert_medium.png'>Element <strong>"+elementName+"</strong> is disabled.<br/>Adding or removing any of its children is forbidden !",
		buttons:["Cancel", "Enable "+elementName],
		callback:function(index){
			if(index==1)
			{
				console.log(element.find('.addItem:first'));
				element.find('.addItem:first').trigger('click');				
				dhtmlx.message(/*{
							type:"error",
							text:*/"Element "+elementName+" was enabled"
				/*}*/);
			}
		}
	});
};

/**
 * Register the number of element in a session variable
 */
registerAction = function(actionTag, clickPath)
{
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
	
	//xmlhttp.open("GET","inc/ajax/registerAction.php?id="+elementId+"&action="+actionTag+"&parent_path="+parentXPath+"&current_path="+currentXPath, true);
	xmlhttp.open("GET","inc/ajax/registerAction.php?action="+actionTag+"&path="+clickPath, true);
	xmlhttp.send();
};