loadModuleResources = function(moduleURLList) {
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

saveModuleData = function($module, modData, asyncOpt) {
    if(typeof asyncOpt === 'undefined') {
        asyncOpt = true;
    }

    //TODO: test if id always class element (could it be choice or sequence?)
	var moduleId = $module.parents('.element').attr('id');
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
            if(!'html' in data) {
                console.error('No data sent back by the server');
                return;
            }

            var moduleDisplay = $(data.html).find('.moduleDisplay').html();
            var moduleResult = $(data.html).find('.moduleResult').html();

            $module.find('.moduleDisplay').html(moduleDisplay);
            $module.find('.moduleResult').html(moduleResult);     
            
            /* look at extra data received from the server */
            if ('xpath_accessor' in data){
            	xpath_accessor(data.xpath_accessor);
            }
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


// set sibling nodes with values from the server
xpath_accessor = function(data){
	for (id in data){
		console.log(id + " -> " + data[id]);
		if ($("#" + id).children("input").length == 1){ /* input */
			$("#" + id).children("input").val(data[id]);
		}else if($("#" + id).children("select").length == 1){ /* select */
			$("#" + id).children("select").val(data[id]);
		}else if($("#" + id).children("div.module").length == 1){ /* module */
			var module = $("#" + id).children("div.module");		
			saveModuleData(module, data[id]);
		}else{ /* other */
			console.log("Unable to set " + id + " with value " + data[id]);
		}
	}
}
