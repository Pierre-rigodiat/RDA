async_input = function(input, callback){	
    // Collect data
    var data = {
        'value': $(input).val()
    }

    var module = $(input).parent().parent().parent();
    saveModuleData(module, data, async=false);
    callback(input);
}