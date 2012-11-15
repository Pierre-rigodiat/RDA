$(document).ready(function(){	
	$('#loadXsd').on('click', function() {
		loadSchema($(this));
	});
	$('#importXsd').on('click', importSchema);
	$('#setRoot').on('click', continueLoading);
	
	$('#currentModel').on('click', {part: '1'}, loadSubPage);
	$('#manageSchemas').on('click', {part: '2'}, loadSubPage);
});

loadSubPage = function(event)
{
	var pageUrl = "";
	
	if(event.data.part==1)
	{
		pageUrl = "inc/skeleton/main/xsd_cfg.inc.php";
	}
	else
	{
		console.log('click');
		pageUrl = "inc/skeleton/main/admin/xsd_mgr.inc.php";
	}
	
	$.ajax({
	        url: pageUrl,  //server script to process data
	        type: 'GET',
	        /*xhr: function() {  // custom xhr
	            myXhr = $.ajaxSettings.xhr();
	            /*if(myXhr.upload){ // if upload property exists
	                myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // progressbar
	            }*/
	            /*return myXhr;
	        },*/
	        //Ajax events
	        success: function(data) {
	        	$("#main").html(data);
	        	//todo link events
	        },
	        error: function() {
	            console.error("Problem importing the file");
	        },
	        // Form data
	        /*data: qString,*/
	        //Options to tell JQuery not to process data or worry about content-type
	        cache: false,
	        contentType: false,
	        processData: false
    });
}

loadSchema = function(caller, rootElement)
{
	var list=caller.prev();
	var button=caller;
	var schemaName=list.find(':selected').text();
	var loadSchemaURL="inc/ajax/loadSchema.php";
	var qString="file="+schemaName;
	if(typeof rootElement !== 'undefined' && rootElement!=null) qString += "&root="+rootElement;
	
	$("#cfg_content").html(
			'<span class="center">Loading '+schemaName+'...</span><span class="center"><img src="resources/img/ajax-loader.gif" alt="Loading..."/></span>'
	);
	
	// Disabling schema list and the load button
	list.attr('disabled', 'disabled');
	button.attr('disabled', 'disabled');
	
	$.ajax({
	        url: loadSchemaURL,  //server script to process data
	        type: 'GET',
	        xhr: function() {  // custom xhr
	            myXhr = $.ajaxSettings.xhr();
	            /*if(myXhr.upload){ // if upload property exists
	                myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // progressbar
	            }*/
	            return myXhr;
	        },
	        //Ajax events
	        success: function(data) {
	        	// Starting the conversion
	        	list.removeAttr('disabled');
				button.removeAttr('disabled');
	        	
	        	// Copying the stuffs and keeping the events
	        	// todo to this for the editing events
	        	$("#cfg_content").html(data);
	        	if(data.indexOf("setRoot")>=0)
	        	{
	        		$("#setRoot").on('click', continueLoading);
	        	}
	        },
	        error: function() {
	            console.error("Problem importing the file");
	        },
	        // Form data
	        data: qString,
	        //Options to tell JQuery not to process data or worry about content-type
	        cache: false,
	        contentType: false,
	        processData: false
    });
}

importSchema = function() {
	// TODO implement it
	alert('Not yet implemented');
}

continueLoading = function() {
	console.log($('#root :selected').text()+'('+$('#root :selected').attr('value')+') is the root of the file');
	
	loadSchema($('#root :selected').attr('value').get(0));
	
	alert('Not yet implemented');
}
