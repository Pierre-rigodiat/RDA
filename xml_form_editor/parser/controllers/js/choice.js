/**
 * 
 */
loadChoiceController = function()
{
	$('.xsdman.choice').on('change', changeChoiceElement);
}

/**
 * 
 */
changeChoiceElement = function()
{
	var choiceId = $(this).parent().attr('id'),
		chosenElementId = $(this).find(':selected').val();
	
	console.log('Choice ID '+choiceId+' change to display elementId '+chosenElementId);
}
