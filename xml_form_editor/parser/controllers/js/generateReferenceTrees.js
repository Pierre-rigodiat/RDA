generateReferenceTrees = function()
{	
	console.log('[generateReferenceTrees] Generating complete and query trees...');
	$('#schema_notif').html(
		'<img alt"Loading..." src="resources/img/loader-circle.gif"/> Generating complete form...'
	);
	
	$.ajax({
        url: 'parser/controllers/php/generateReferenceTrees.php',
        type: 'GET',
        success: function(data) {
        	try
        	{
        		var jsonObject = $.parseJSON(data);
        		
        		if(jsonObject.code>=0)
	        	{
					console.log('[generateReferenceTrees] Reference trees generated');
					
					$('#schema_notif').html(
						'<span class="icon valid legend long">'+jsonObject.result+'</span>'
					);
	        	}
	        	else
	        	{
	        		console.error('[generateReferenceTrees] Error '+jsonObject.code+'  ('+jsonObject.result+') occured while toggle module');
	        		
	        		$('#schema_notif').html(
						'<span class="icon invalid legend long">Impossible to generate form: '+jsonObject.result+'</span>'
					);
	        	}
        	}
        	catch(ex)
        	{
        		console.error('[generateReferenceTrees] JSON parsing error');
        		
        		$('#schema_notif').html(
					'<span class="icon invalid legend long">Impossible to generate form: cannot parse response.</span>'
				);
        	}
        },
        error: function() {
            console.error("[generateReferenceTrees] Problem with the AJAX call");
            
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