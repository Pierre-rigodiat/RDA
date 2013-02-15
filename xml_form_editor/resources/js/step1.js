$(document).ready(function(){
	// Moving to the next page
	//  Write generic function with AJAX loading...
	//$('#tostep2').on('click', {page: 2}, moveTo);
	//$('#tostep4').on('click', {page: 4}, moveTo);
	
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

// todo improve code implementation
/*moveTo = function(event)
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
};*/