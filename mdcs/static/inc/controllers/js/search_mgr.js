/**
 * 
 */
loadQueryManagerController = function()
{
	$('.add.id').on('click', retrieveAdminQueryIds);
}

/**
 * 
 */
retrieveAdminQueryIds = function()
{
	console.log("[retrieveQuery] Query send...");
	
	var inputs = $('input:checked'),
		count = 0,
		qString = '';
	
	inputs.each(function()
	{
		var id = $(this).parent().attr('id');
			
		qString += count + '=' + id + '&';
		count++;
	});
	
	qString = qString.substring(0, qString.length-1);
	
	$.ajax({
        url: 'inc/controllers/php/addQueryIds.php',
        type: 'GET',
        success: function(data) {
        	
        },
        error: function() {
            console.error("[saveData] Problem with the AJAX call");
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
