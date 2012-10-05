$(document).ready(function(){
	// Linking the event on all the + buttons
	$('.addItem').on('click', addItem);

	// Adding the event on all the - buttons
	$('.removeItem').on('click', removeItem);
	
	$('#tostep1').on('click', {page: 1}, moveTo);
});

/**
 * Add item function
 */
addItem = function()
{
	var htmlToCopy = $(this).parent().parent();
	var maxoccurs = 1;
	var minoccurs = 1;
	
	console.log($(this).parent());

	$(this).parent().find(':hidden').each(function() {
		switch($(this).attr('name'))
		{
		case 'minoccurs':
			minoccurs = $(this).val();
			break;
		case 'maxoccurs':
			if($(this).val() == 'unbounded')
			{
				maxoccurs = -1;
			}
			else
			{
				maxoccurs = $(this).val;
			}
			break;
		default:
			break;
		}			
	});

	console.log('maxoccurs='+maxoccurs+'; minoccurs='+minoccurs);

	// XXX If we have reached the max occurs allowed all the + button need to disappear
	//htmlToCopy.find('.')

	if($(this).css("color")!='rgb(128, 128, 128)' || (htmlToCopy.hasClass("unavailable") && htmlToCopy.parent().css("color")!='rgb(128, 128, 128)')) // XXX Color is not really reliable...
	{	
		console.log('-- Add item --');		
		console.log(htmlToCopy);

		var elementId = htmlToCopy.children().attr('class');
		var siblingsNumber = htmlToCopy.parent().find('.'+elementId).length;

		console.log(siblingsNumber+' brother(s) before adding');

		if((siblingsNumber < maxoccurs || (siblingsNumber == maxoccurs && htmlToCopy.hasClass("unavailable"))) || maxoccurs == -1)
		{
			// XXX We need to add the - button
			if($(this).parent().find('.removeItem').length==0)
			{
				console.log('The - button need to be add');

				// TODO Figure out how to store the base64 into a variable
				$(this).after(' <img src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACJ0lEQVQokZVSS28SYRS9MzDQwgAVEhBoS9Q2JkRpF7UGWkWNj4XUP+CiC2Ncd92dGxNXxrgxLnysfC9MbdKa4INgIjRpusEQoQgIFjqD5TWvj+/7XEhqIV3o3d3knJxzzz0MpRT+Z/R7FyRst9aS9cRnVBMJJToLbw3O2E6EjM6DuxhmV6G9sb794qnZ4+InJlmblSoKqpbF6LsmJsNXrx2YCvUQ2hvr1SeP7LMzfCDQyaVopQCaxvB2dmRUWH5b+lk8dH3BMX2qawkJgvD8mWN6ynzcjz68lmSFwcho4BipiX+kh0JBbbW5+fieyXdk0OVhAaCV/GI0603H/Ci2jFWZqBInNciOiBs1okhafNUZPsdWypXYStdS/uaiY8Kv7yhSIY1S2b5YjE4b6xxt1+XvQjZ496UeANQdUW8ywbc0qKrrwas+Qnk+wrXQwGRQ/hoHABYAqIZwo0GadQNW9s2+0yEAQBjUPZq12eRCbtBs7RTF8nykH86yRq+vnts0WOxdBevJkLCWAPc4bqgcz+0FY0ox1XG+8Xwq6j4b6RKGgrOa2y18ihovRIjGMjodAGBgMKZA9Lbzc/n3Sx2e95y58vdxtWQ8e/+2neOd4YtaPqPmsgSRgbExw/DhYvRNsVUILNzyhC71VENMxDIP70Bta+Ro0ODyAoBUzmdSH4nV4r+x+AfdQwAAeatUia2UYkvqryrVkM5h94bnPKcvm92+fcr3j/MbY+YNcy1xI5AAAAAASUVORK5CYII=" alt="remove" class="removeItem">');
				$(this).parent().find('.removeItem').on('click', removeItem);
			}

			if(htmlToCopy.hasClass("unavailable"))
			{
				console.log('Element has to be set available');
				console.log(htmlToCopy.find(':input').length + ' input(s) to enable');

				// Displaying the remove button
				// XXX This is done up
				/*$(this).after(' ', removeButtons[0]);
				removeButtons.splice(0,1);*/

				// Input are enabled
				htmlToCopy.find(':input').removeAttr('disabled');
				htmlToCopy.replaceWith(htmlToCopy.contents());
			}
			else
			{
				// TODO Increment the of id and name in the input
				var newHTMLCode = htmlToCopy.clone(true);

				newHTMLCode.find(':input').each(function(){
					if($(this).attr('name').match(/[0-9\/]+\-[0-9]+/))
					{
						console.log($(this).attr('name')+' needs to be upgraded');

						var index = $(this).attr('name').lastIndexOf('-');
						var elementId = $(this).attr('name').slice(0, index);

						var maxId = -1;

						$('body :input[name|="'+elementId+'"]').each(function(){
							var iterationNumber = parseInt($(this).attr('name').slice(index+1));

							if(iterationNumber > maxId)
							{
								maxId = iterationNumber;
							}
						});

						maxId += 1;

						console.log('new id='+maxId);

						$(this).attr('name',elementId + '-' + maxId);
						$(this).attr('id',elementId + '-' + maxId);
					}
				});			

				console.log('A new element has to be added');
				htmlToCopy.after(newHTMLCode[0]); // clone(true) also copy all the events into the new variable
			}

			if(siblingsNumber + 1 >= maxoccurs && maxoccurs != -1)
			{
				$(this).parent().parent().find('.'+elementId).each(function() {
					$(this).find('.addItem').remove();

				});
			}
			
			registerAction(elementId, 'add');
		}
		else
		{
			console.log('Max limit reached. You cannot add more items');
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
		
		//registerAction(51, 'add');
	}
};

/**
 * Remove item function
 */
removeItem = function()
{	
	if($(this).css("color")!='rgb(128, 128, 128)') // XXX Not really reliable...
	{
		console.log('-- Remove item --');

		// XXX We need to add the + button

		var htmlToRemove = $(this).parent().parent();
		console.log(htmlToRemove[0]);

		var maxoccurs = 1;
		var minoccurs = 1;

		$(this).parent().find(':hidden').each(function() {
			switch($(this).attr('name'))
			{
			case 'minoccurs':
				minoccurs = $(this).val();
				break;
			case 'maxoccurs':
				if($(this).val() == 'unbounded')
				{
					maxoccurs = -1;
				}
				else
				{
					maxoccurs = $(this).val;
				}
				break;
			default:
				break;
			}			
		});

		console.log('minoccurs: '+minoccurs+'; maxoccurs: '+maxoccurs);

		var elementXPath = getElementXPath(htmlToRemove.get(0));
		var elementId = $(this).parent().attr('class');

		console.log('Element ID = '+elementId);
		console.log('Element XPath = '+elementXPath);

		var previousElement = null;
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
			console.log('Element is the '+elementIndex+' one of the list');

			var previousXPath = elementXPath.slice(0, index0)+'['+(elementIndex-1)+']';
			var nextXPath = elementXPath.slice(0, index0)+'['+(elementIndex+1)+']';

			console.log('Previous XPath: '+previousXPath);
			console.log('Next XPath: '+nextXPath);

			previousElement = $(getElementsByXPath($(document).get(0), previousXPath));
			nextElement = $(getElementsByXPath($(document).get(0), nextXPath));

			allElement = $(getElementsByXPath($(document).get(0), elementXPath.slice(0, index0)));
		}
		else
		{
			// For the first element of the list we only need to check the next element
			console.log('This is the first element of the list');

			nextElement = $(getElementsByXPath($(document).get(0), elementXPath+'[2]'));

			allElement = $(getElementsByXPath($(document).get(0), elementXPath));
		}

		console.log(previousElement);
		console.log(nextElement);

		var siblingElementNumber = allElement.find('.'+elementId).length;

		console.log(siblingElementNumber+' brother(s) before deleting');

		if(siblingElementNumber > minoccurs)
		{
			if(previousElement!=null)
			{
				previousId = previousElement.children().attr('class');
				console.log('Previous ID = '+previousId);
			}

			if(nextElement!=null)
			{
				nextId = nextElement.children().attr('class');
				console.log('Next ID = '+nextId);
			}

			if(nextId == elementId || previousId == elementId)
			{
				console.log('Another similar element exists');

				if(siblingElementNumber - 1 == minoccurs)
				{
					console.log('Min element reached, remove button will be deleted');

					allElement.find('.'+elementId).each(function() {
						$(this).find('.removeItem').remove();
						/*var removeButton = $(this).find('.removeItem');

						removeButtons.push(removeButton.clone(true));
						removeButton.remove();*/
					});
				}

				htmlToRemove.remove();
			}
			else
			{
				var parent = $(this).parent();

				if(parent.find('.addItem').length==0)
				{
					console.log('Adding the + button...');

					parent.append(' <img src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACUUlEQVQokZWSX2hScRTHz9W5uZlzms02nH82wv3PKFeO5qAYQqOHHlrPg156ihZE0J/XInqKvQhBDwU9VC+VyCzb+rNyNEJxstqmd7pdU3N679V7U3/3Tw+7SMIe6rwd+J7z+XK+BxNFEf6nGv5uSDYXTS2Hk0GSLfACr1So7CbnEZNTrzbUNFiNsJYOz0Wf6zTttg57c+O+Kl/Nlogv64Eyg84fmz5qcdYNrKXDr8KPD3ePHjIMx6i1NLuNBKRp1LS3GBd/+NY34xddl0e6T0qWSDbnjz4bsDis7f2BbS/LsEjklMomBpU2i7Eh8/Hib/rRh1nT/u6Dmk4ZAKwQXxuUSsuBvk+pt2VUZhF7ZeTWpeFrVCWfp9LB1PwJ2ykSZRdW/QAgA4BwcslssH0vRHJ0jmYpiins2iXwZLXMMPTONoWP9o75V7ySpTyT61eoEjSOhPJ1593aQWanngLAjHeKIGODekeaCkgEjucYRJeqFJKjPW8v8gIGIsdzEqGlSU3kE6omNcnmZ95NM79oz4UXu7sBQIbJO1vNyQyubdFJBLvJGcKDJpVVRBWM57RtqtpugQdMxLo0Vl/ozcTgpJRDrpi557upVMsdPeOLuI8XOF7gBB4DEBVy+XjP5FzodZxIeaafGHUmKbhl/LNn/r5e3zbWO7FF4gQZFwXBqO0xasy+0MvIxsbtc3dOD7jrXmMp9vHh+wc7lYyrz2Vo7QCArXzC/y3QiKmunrmxq64bAICfJLGw6p+LeLN0hhdQa7PWPXTWPTzZpTPv8Xz/WH8AA8ItNSarPAgAAAAASUVORK5CYII=" alt="add" class="addItem">');
					parent.find('.addItem').on('click', addItem);
				}

				htmlToRemove.wrapInner('<div class="unavailable">');
				htmlToRemove.find(':input').attr('disabled', true);

				//removeButtons.push($(this).clone(true));
				$(this).remove();
			}
			
			registerAction(elementId, 'delete');
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
		
		//registerAction(51, 'delete');
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
registerAction = function(elementId, actionTag)
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
	
	/*xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			document.getElementById("txtHint").innerHTML=xmlhttp.responseText;
		}
	}*/
	
	xmlhttp.open("GET","inc/ajax/registerAction.php?id="+elementId+"&action="+actionTag, true);
	xmlhttp.send();
};