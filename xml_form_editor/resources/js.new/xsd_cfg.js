/**
 *	Event handler for the schema configuration.
 * 	Handles:
 * 		- Adding/Removing modules
 * 		- Save current modification on the schema
 * 		- Reload the original file
 *  
 * 
 */
loadXsdConfigHandler = function()
{
	//$('.module').on('click', toggleModule);
	$('.refresh').on('click', cancelChanges);
	$('.save').on('click', saveChanges);
	
	$('.clickable').on('click', goToPage);
}

goToPage = function()
{
	var defaultName = "clickable ",
		baseUrl = $(location).attr('href'),
		pageName = $(this).attr('class').substr(defaultName.length);
	
	pageName = pageName.split('-');
	//console.log(pageName[0]+' '+pageName[1]);
	
	if((index = baseUrl.indexOf('/'+pageName[0]))==-1 || index!=baseUrl.length-(pageName[0].length+1))
	{		
		//console.log('Need to rewrite '+index+' '+(baseUrl.length-pageName[0].length));
		var lastPathIndex = baseUrl.lastIndexOf('/');
		baseUrl = baseUrl.substr(0, lastPathIndex) + pageName[0];
	}
	
	loadPage(baseUrl + '?' + pageName[1]);
	
	//console.log(pageName);
}

/*toggleModule = function()
{
	var iconClass = $(this).children(':first').attr('class');
	
	console.log('[toggleModule] Clicked element class: '+iconClass);
	
	if(iconClass.indexOf('disable')==-1)
	{
		console.log('[toggleModule] Toggling '+$(this).text()+'...');
		if(iconClass.indexOf('off')!=-1) // Enabling module
		{
			$(this).children(':first').attr('class', 'icon legend on');
		}
		else // Disabling module
		{
			$(this).children(':first').attr('class', 'icon legend off');
		}
	}
}*/

cancelChanges = function()
{
	console.warn('[cancelChanges] Not yet implemented');
}

saveChanges = function()
{
	console.warn('[saveChanges] Not yet implemented');
}

