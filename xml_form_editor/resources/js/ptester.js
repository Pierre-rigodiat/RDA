$(document).ready(function(){
	// Linking the click event the refresh button
	$('.refresh').on('click', refreshForm);
});

refreshForm = function()
{
	var htmlFormTitle = $(this).parent();
	
	$.ajax({
        url: 'inc/ajax/generateForm.php',
        type: 'GET',
        success: function(data) {
        	htmlFormTitle.next().remove();
        	htmlFormTitle.after(data);
        },
        error: function() {
            console.error("[refreshForm] Problem with the AJAX call");
        },
        // Form data
        //data: 'id='+elementId+'&'+qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}
