loadModule = function($module) {
    var moduleURL = $module.find('.moduleURL').text();

    if(moduleURL === '') {
        return;
    }

    $.ajax({
        url : '/modules'+moduleURL,
        type : "GET",
        dataType: "json",
        success: function(data){
            if('module' in data) {
                $module.find(".moduleContent").html(data.module);

                if('moduleDisplay' in data && 'moduleResult' in data) {
                    $module.find('.moduleDisplay').html(data.moduleDisplay);
                    $module.find('.moduleResult').html(data.moduleResult);
                }
            } else {
                //raise error, no module provided
            }
        },
        error: function() {
            // Raise error
        }
    });
}

loadModuleResources = function(moduleURLList) {
    $.each(moduleURLList, function(index, moduleURL) {
         console.log(moduleURL);

        $.ajax({
            url : '/modules'+moduleURL,
            type : "GET",
            dataType: "json",
            data: {
                'type': 'resources',
            },
            success: function(data){
                if('moduleStyle' in data && 'moduleScript' in data) {
                    // Update style
                    $('head').append(data.moduleStyle);

                    // Update moduleScript
                    $('body').append(data.moduleScript);
                }
            },
            error: function() {
                // Raise error
            }
        });
    });
}

saveModuleData = function($module, modData) {
    var moduleURL = $module.find('.moduleURL').text();

    if(moduleURL === '') {
        return;
    }
    
    $.ajax({
        url : '/modules'+moduleURL,
        type : "POST",
        dataType: "json",
        data: modData,
        success: function(data){
            if('moduleDisplay' in data && 'moduleResult' in data) {
                $module.find('.moduleDisplay').html(data.moduleDisplay);
                $module.find('.moduleResult').html(data.moduleResult);
            }
        },
        error: function() {

        }
    });
};

// Modules initialisation
initModules = function() {
    var moduleList = $('.module');
    var moduleURLList = [];
    console.log(moduleList);

    $.each(moduleList, function(index, value) {
        console.log($(value));
        loadModule($(value));

        var moduleURL = $(value).find('.moduleURL').text();
        if(moduleURL !== "" && moduleURLList.indexOf(moduleURL) === -1) {
            moduleURLList.push(moduleURL);
        }
    });

    console.log(moduleURLList);
    loadModuleResources(moduleURLList)
};

