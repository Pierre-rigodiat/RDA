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
	$('.module').on('click', toggleModule);
	$('.refresh').on('click', cancelChanges);
	$('.save').on('click', saveChanges);
}

toggleModule = function()
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
}

cancelChanges = function()
{
	console.warn('[cancelChanges] Not yet implemented');
}

saveChanges = function()
{
	console.warn('[saveChanges] Not yet implemented');
}

