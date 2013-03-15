generateCompleteTree = function()
{	
	console.log('[generateCompleteTree] Generating complete tree...');
	$('#schema_notif').html(
		'<img alt"Loading..." src="resources/img/loader-circle.gif"/> Generating complete form...'
	);
	
	$.ajax({
        url: 'parser/controllers/php/generateCompleteTree.php',
        type: 'GET',
        success: function(data) {
        	try
        	{
        		var jsonObject = $.parseJSON(data);
        		
        		if(jsonObject.code>=0)
	        	{
					console.log('[generateCompleteTree] Complete tree generated');
					
					$('#schema_notif').html(
						'<span class="icon valid legend long">'+jsonObject.result+'</span>'
					);
	        	}
	        	else
	        	{
	        		console.error('[generateCompleteTree] Error '+jsonObject.code+'  ('+jsonObject.result+') occured while toggle module');
	        		
	        		$('#schema_notif').html(
						'<span class="icon invalid legend long">Impossible to generate form: '+jsonObject.result+'</span>'
					);
	        	}
        	}
        	catch(ex)
        	{
        		console.error('[generateCompleteTree] JSON parsing error');
        		
        		$('#schema_notif').html(
					'<span class="icon invalid legend long">Impossible to generate form: cannot parse response.</span>'
				);
        	}
        },
        error: function() {
            console.error("[generateCompleteTree] Problem with the AJAX call");
            
            $('#schema_notif').html(
				'<span class="icon invalid legend long">Impossible to generate form: background call error</span>'
			);
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}