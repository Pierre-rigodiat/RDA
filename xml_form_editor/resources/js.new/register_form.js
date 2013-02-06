/**
 * 
 */
loadRegisterFormController = function()
{
	$('.blank').on('click', clearFields);
	$('.save').on('click', saveFields);
}

clearFields = function()
{
	console.warn("[clearFields] Not yet implemented");
}

saveFields = function()
{
	console.log("[saveFields] Saving fields...");
	
	var inputs = $('input.text'),
		qString = '';
	
	inputs.each(function()
	{
		var inputId = $(this).parent().attr('id'),
			inputValue = $(this).attr('value');
		
		if(inputValue != '' && !isNaN(parseInt(inputId)))
		{
			console.log('Id '+parseInt(inputId)+' = '+inputValue);
			qString += parseInt(inputId)+'='+inputValue+'&';
		}	
	});
	
	qString = qString.substring(0, qString.length-1);
	
	$.ajax({
        url: 'inc/ajax.new/saveData.php',
        type: 'GET',
        success: function(data) {
        	
        },
        error: function() {
            console.error("[saveFields] Problem with the AJAX call");
        },
        // Form data
        data: qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
	
	console.log('qString = '+qString);
}

