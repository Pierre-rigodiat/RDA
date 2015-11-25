$('body').on('click', '.mod_checkboxes input:checkbox', function(event) {
	$checkboxes = $(this).parent();
	
	var values = [];
	$checkboxes.children("input:checked").each(function() {
		  values.push($(this).val());
	});

	
	// Collect data
    var data = {
        'data': values
    }

    var module = $(this).parent().parent().parent()
    saveModuleData(module, data);
});