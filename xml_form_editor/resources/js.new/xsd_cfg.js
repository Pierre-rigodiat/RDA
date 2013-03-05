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
	$('.refresh').on('click', cancelChanges);
	$('.save').on('click', saveChanges);
		
	$('.clickable').on('click', goToPage);
}

/**
 * 
 */
// TODO put this function in the main configuration
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
}

/**
 * 
 * 
 * 
 */
cancelChanges = function()
{
	console.warn('[cancelChanges] Not yet implemented');
}

/**
 *
 * 
 *  
 */
saveChanges = function()
{
	console.warn('[saveChanges] Not yet implemented');
}