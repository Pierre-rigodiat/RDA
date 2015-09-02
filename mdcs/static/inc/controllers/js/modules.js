//loadModule = function($module) {
//    var moduleURL = $module.find('.moduleURL').text();
//
//    if(moduleURL === '') {
//        return;
//    }
//
//    $.ajax({
//        url : '/modules'+moduleURL,
//        type : "GET",
//        dataType: "json",
//        success: function(data){
//            if('module' in data) {
//                $module.find(".moduleContent").html(data.module);
//
//                if('moduleDisplay' in data && 'moduleResult' in data) {
//                    $module.find('.moduleDisplay').html(data.moduleDisplay);
//                    $module.find('.moduleResult').html(data.moduleResult);
//                }
//            } else {
//                //raise error, no module provided
//            }
//        },
//        error: function() {
//            // Raise error
//        }
//    });
//}

loadModuleResources = function(moduleURLList) {
//    var modulesResources = {
//        'scripts': [],
//        'styles': []
//    };

//    $.each(moduleURLList, function(index, moduleURL) {
//        $.ajax({
//            url : '/modules'+moduleURL,
//            type : "GET",
//            async: false,
//            dataType: "json",
//            data: {
//                'type': 'resources',
//            },
//            success: function(data){
//                /*if('moduleStyle' in data && 'moduleScript' in data) {
//                    // Update style
//                    $('head').append(data.moduleStyle);
//
//                    // Update moduleScript
//                    $('body').append(data.moduleScript);
//                }*/
//
//                modulesResources.scripts = modulesResources.scripts.concat(data.moduleScript);
//                modulesResources.styles = modulesResources.styles.concat(data.moduleStyle);
//            },
//            error: function() {
//                // Raise error
//            }
//        });
//    });

    //console.log(modulesResources);

    $.ajax({
        url: '/modules/resources',
        type: "GET",
        dataType: "json",
        data: {
            'urls': JSON.stringify(moduleURLList)
        },
        success: function(data){
            $('head').append(data.styles);
            $('body').append(data.scripts);
        },
        error: function() {
            // Raise error
        }
    });
}

saveModuleData = function($module, modData, asyncOpt=true) {
	var moduleId = $module.parents('.element').attr('id'); //TODO: test if id always class element (could it be choice or sequence?)
    var moduleURL = $module.find('.moduleURL').text();

    if(moduleURL === '') {
        return;
    }
    
    modData['htmlId'] = moduleId;

    var ajaxOptions = {
        url : '/modules'+moduleURL,
        type : "POST",
        dataType: "json",
        data: modData,
        async: asyncOpt,
        success: function(data){

            var moduleDisplay = $(data.html).find('.moduleDisplay').html();
            var moduleResult = $(data.html).find('.moduleResult').html();
//            var $moduleDisplay = $(data).find('.moduleDisplay').text();
//            console.log($moduleDisplay);

            $module.find('.moduleDisplay').html(moduleDisplay);
            $module.find('.moduleResult').html(moduleResult);     
            
            if ('xpath_accessor' in data){
            	xpath_accessor(data.xpath_accessor);
            }

            /*if('moduleDisplay' in data && 'moduleResult' in data) {
            	$module.find('.moduleDisplay').html(data.moduleDisplay);
                $module.find('.moduleResult').html(data.moduleResult);
            }*/
        },
        error: function(data) {
            console.error("Error when saving data");
        }
    }

    if(modData instanceof FormData) {
        ajaxOptions.processData = false;
        ajaxOptions.contentType = false;
    }

    $.ajax(ajaxOptions);   
};

// Modules initialisation
initModules = function() {
    var moduleList = $('.module');
    var moduleURLList = [];
    console.log(moduleList);

    $.each(moduleList, function(index, value) {
//        console.log($(value));
//        loadModule($(value));

        var moduleURL = $(value).find('.moduleURL').text();
        if(moduleURL !== "" && moduleURLList.indexOf(moduleURL) === -1) {
            moduleURLList.push(moduleURL);
        }
    });

    console.log(moduleURLList);
    loadModuleResources(moduleURLList)
};


xpath_accessor = function(data){
	
	for (id in data){
		console.log(id + " -> " + data[id]);
		if ($("#" + id).children("input").length == 1){
			$($("#" + id).children("input")[0]).val(data[id]);
		}
		
	}
}
