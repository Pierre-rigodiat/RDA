$('body').on('change', '.mod_options select', function(event) {
    // Collect data
    var data = {
        'value': $(this).val()
    }

    var module = $(this).parent().parent().parent()
    saveModuleData(module, data);
});