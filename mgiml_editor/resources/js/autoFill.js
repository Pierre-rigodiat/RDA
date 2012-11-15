autoClick = function(path, buttonType)
{
	var jObj = $('form');
	var indexes = path.split('/');
	
	//console.log(indexes);
	
	for(i in indexes)
	{
		if(i!=0)
		{
			jObj = getListElement(jObj, indexes[i]);
			//console.log(jObj);
		} 
	}
	
	if(buttonType=='add') jObj.find('.addItem:eq(0)').trigger('click');
	else jObj.find('.removeItem:eq(0)').trigger('click');
};

autoFill = function(path, valueList)
{
	var indexValue = 0;
	$('form').find('input[name^="'+path+'"]').each(function()
	{		
		$(this).attr('value', valueList[indexValue]);
		
		if($(this).attr('type')=='hidden')
		{
			$(this).parent().find('.text:eq(0)').attr('value', valueList[indexValue]);
		}
		
		
		indexValue += 1;	
		
		console.log($(this));			
	});
}

getListElement = function(object, pathIndex)
{
	return object.children('ul:eq(0)').children(':eq('+pathIndex+')');
}
