/**
 * Add item function
 */
/*addItem = function()
{
	var htmlToCopy = $(this).parent().parent();
	console.log(htmlToCopy.get(0));

	// Defining MINOCCURS and MAXOCCURS as it appear in the HTML file
	var maxoccurs = 1;
	var minoccurs = 1;	
	$(this).parent().find(':hidden').each(function() { // Check every hidden field to get the values
		//console.log($(this));
		
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

	console.log('maxoccurs='+maxoccurs+'; minoccurs='+minoccurs);

	// XXX If we have reached the max occurs allowed all the + button need to disappear
	//htmlToCopy.find('.')
	// todo with multiple input it does not work

	if($(this).css("color")!='rgb(128, 128, 128)' || (htmlToCopy.hasClass("unavailable") && htmlToCopy.parent().css("color")!='rgb(128, 128, 128)')) // XXX Color is not really reliable...
	{
		var elementId = htmlToCopy.children().attr('class');
		console.log('Item to add has id '+elementId);
		
		var siblingsNumber = htmlToCopy.parent().find('.'+elementId).length;
		//console.log(siblingsNumber+' brother(s) before adding');

		if((siblingsNumber < maxoccurs || (siblingsNumber == maxoccurs && htmlToCopy.hasClass("unavailable"))) || maxoccurs == -1)
		{
			// Adding minus button if needed
			if($(this).parent().find('.removeItem').length==0)
			{
				//console.log('The - button need to be add');

				// TODO Use CSS sprites
				$(this).after(' <img src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACJ0lEQVQokZVSS28SYRS9MzDQwgAVEhBoS9Q2JkRpF7UGWkWNj4XUP+CiC2Ncd92dGxNXxrgxLnysfC9MbdKa4INgIjRpusEQoQgIFjqD5TWvj+/7XEhqIV3o3d3knJxzzz0MpRT+Z/R7FyRst9aS9cRnVBMJJToLbw3O2E6EjM6DuxhmV6G9sb794qnZ4+InJlmblSoKqpbF6LsmJsNXrx2YCvUQ2hvr1SeP7LMzfCDQyaVopQCaxvB2dmRUWH5b+lk8dH3BMX2qawkJgvD8mWN6ynzcjz68lmSFwcho4BipiX+kh0JBbbW5+fieyXdk0OVhAaCV/GI0603H/Ci2jFWZqBInNciOiBs1okhafNUZPsdWypXYStdS/uaiY8Kv7yhSIY1S2b5YjE4b6xxt1+XvQjZ496UeANQdUW8ywbc0qKrrwas+Qnk+wrXQwGRQ/hoHABYAqIZwo0GadQNW9s2+0yEAQBjUPZq12eRCbtBs7RTF8nykH86yRq+vnts0WOxdBevJkLCWAPc4bqgcz+0FY0ox1XG+8Xwq6j4b6RKGgrOa2y18ihovRIjGMjodAGBgMKZA9Lbzc/n3Sx2e95y58vdxtWQ8e/+2neOd4YtaPqPmsgSRgbExw/DhYvRNsVUILNzyhC71VENMxDIP70Bta+Ro0ODyAoBUzmdSH4nV4r+x+AfdQwAAeatUia2UYkvqryrVkM5h94bnPKcvm92+fcr3j/MbY+YNcy1xI5AAAAAASUVORK5CYII=" alt="remove" class="removeItem">');
				$(this).parent().find('.removeItem').on('click', removeItem);
			}

			if(htmlToCopy.hasClass("unavailable")) // The code just need to be set as available
			{
				/*console.log('Element has to be set available');
				console.log(htmlToCopy.find(':input').length + ' input(s) to enable');*/

				// Input are enabled
				// xxx Not working well when we have an unable element inside
		/*		htmlToCopy.find(':input').removeAttr('disabled');
				htmlToCopy.replaceWith(htmlToCopy.contents());
			}
			else // A whole new part has to be written
			{
				var newHTMLCode = htmlToCopy.clone(true);
				var inputArray = new Array();

				newHTMLCode.find(':input').each(function(){ // Each input in the new HTML code is parsed
					var attr = $(this).attr('name');
					
					if(attr && attr.match(/[0-9\/]+\[[0-9]+\]/)) // If the input name is like 1/2/3/4[0]
					{
						//console.log('Input '+$(this).attr('name')+' needs to be upgraded');
						
						/* Step 1: Upgrade name and id of the input */
			/*			var index = $(this).attr('name').lastIndexOf('[');
						var elementPath = $(this).attr('name').slice(0, index);
						
						var regexp = new RegExp('/'+elementId+'[/\[]');
						var updateClass = false;
						if($(this).attr('class') && $(this).attr('class').match(regexp)) updateClass = true;
						
						if(updateClass)
						{
							var parentPath = $(this).attr('class').split(" ")[1];
							var parentElementArray = parentPath.split("/");
							var parentId = parentElementArray.reverse()[0].split("[")[0]; // Take the last element of the array and separate the id from the occurence
						}
						
						if(!inputArray[elementPath]) inputArray[elementPath] = 0;
						
						
						var maxId = -1;
						var maxParentId = -1;

						$('body :input[name^="'+elementPath+'"]').each(function(){ // For each existing input for the same tree (ie 1/2/3/4[x])
							//console.log($(this));
							
							// Checking the iteration number of the attribute
							var iterationNumber = parseInt($(this).attr('name').slice(index+1));
							if(iterationNumber > maxId)
							{
								maxId = iterationNumber;
							}
							
							// Checking the class number of the attribute
							if(updateClass)
							{
								var parentIterationNumber = parseInt($(this).attr('class').split('[')[1].split(']')[0]); // The value between [ and ] is set as the iteration number
								if(parentIterationNumber > maxParentId)
								{
									maxParentId = parentIterationNumber;
								}
							}
						});

						maxId += 1 + inputArray[elementPath];
						//console.log('New name index='+maxId);
						
						if(updateClass)
						{
							maxParentId += 1;
							//console.log('New class index='+maxParentId);
						}
						
						$(this).attr('name', elementPath + '[' + maxId + ']');
						$(this).attr('id', elementPath + '[' + maxId + ']');
						inputArray[elementPath] += 1; 
						
						if(updateClass)
						{
							var newClass = 'text ';
							parentElementArray.reverse();
							for(var i=0; i<parentElementArray.length-1; i++)
							{
								newClass += parentElementArray[i] + '/';
							}
							
							newClass += parentId + "["+maxParentId+"]";
							
							$(this).attr('class', newClass);
						
							//console.log('Register new input parent -> {'+$(this).attr('class')+','+$(this).attr('name')+'}');
						}
					}
				});			

				//console.log('A new element has to be added');
				htmlToCopy.after(newHTMLCode[0]); // clone(true) also copy all the events into the new variable
			}

			// Removing the plus button if needed
			if(siblingsNumber + 1 >= maxoccurs && maxoccurs != -1)
			{
				$(this).parent().parent().find('.'+elementId).each(function() {
					$(this).find('.addItem').remove();
				});
			}
			
			// Parse the xpath to get to the ajax script
			var clickXpath = getElementXPath(htmlToCopy.get(0));
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
			
			console.log('Register new + click -> '+clickPath);
			registerAction('a', clickPath);
		}
		else
		{
			console.log('Max limit reached. You cannot add more items');
		}
	}
	else // An element has been set unavailable above
	{
		// Searching the unavailable element
		var unavailableElement = $(this).parent().parent().parent();
		while(!unavailableElement.hasClass('unavailable'))
		{
			//console.log(unavailableElement);
			unavailableElement = unavailableElement.parent();
		}
		//console.log(unavailableElement);

		var index = unavailableElement.text().indexOf(' ');
		editionUnavailableBox(unavailableElement.text().slice(0, index), unavailableElement);
	}
};*/