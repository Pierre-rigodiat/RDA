/**
 * 
 * File Name: module_mgr.js
 * Author: Sharief Youssef
 * 		   sharief.youssef@nist.gov
 *
 *        Guillaume SOUSA AMARAL
 *        guillaume.sousa@nist.gov
 * 
 * Sponsor: National Institute of Standards and Technology (NIST)
 * 
 */

/**
 * Load modules controllers
 */
loadModuleManagerHandler = function()
{
    console.log('BEGIN [loadModuleManagerHandler]');    
    $('.delete.module').on('click', deleteModule);
    console.log('END [loadModuleManagerHandler]');
}

/**
 * Delete a module
 */
deleteModule = function(){
	var objectid = $(this).attr("objectid");
	$(function() {
        $( "#dialog-delete" ).dialog({
            modal: true,
            buttons: {
            	Yes: function() {	
            		$( this ).dialog( "close" );
            		delete_module(objectid);
                },
                No:function() {	
            		$( this ).dialog( "close" );
                }
            }
        });
    });
}



/**
 * AJAX call, deletes a module
 * @param objectid
 */
delete_module = function(objectid){
    $.ajax({
        url : "/admin/delete_module",
        type : "POST",
        dataType: "json",
        data : {
        	objectid : objectid,
        },
        success: function(data){
            $('#model_selection').load(document.URL +  ' #model_selection', function() {
            	loadModuleManagerHandler();
            });
        }
    });
}


/**
 * Load controllers for module addition
 */
loadAddModuleHandler = function()
{
    console.log('BEGIN [loadAddModuleHandler]');
    document.getElementById('moduleResource').addEventListener('change',handleModuleResourceUpload, false);
    init_module_manager();
    console.log('END [loadAddModuleHandler]');
}


/**
 * AJAX call, inits the module manager
 */
init_module_manager = function(){
    $.ajax({
        url : "/admin/init_module_manager",
        type : "POST",
        dataType: "json",
        success: function(data){
            
        }
    });
}


/**
 * Handler for reading of resources files
 * @param evt
 */
function handleModuleResourceUpload(evt) {
	var files = evt.target.files; // FileList object
    reader = new FileReader();
    reader.onload = function(e){
    	resourceContent = reader.result;
    	resourceFilename = files[0].name;
    	add_module_resource(resourceContent, resourceFilename);
    }
    reader.readAsText(files[0]);
}


/**
 * AJAX call, add a resource to a module
 * @param resourceContent content of the resource
 * @param resourceFilename name of the resource file
 */
add_module_resource = function(resourceContent, resourceFilename){
    $.ajax({
        url : "/admin/add_module_resource",
        type : "POST",
        dataType: "json",
        data : {
        	resourceContent : resourceContent,
        	resourceFilename : resourceFilename,
        },
        success: function(data){
            
        }
    });
}


/**
 * Upload a resource
 */
uploadResource = function()
{
	upload_resource();
}


/**
 * AJAX call, uploads a resource
 */
upload_resource = function(){
    $.ajax({
        url : "/admin/upload_resource",
        type : "GET",
        dataType: "json",
        success: function(data){
        	if("filename" in data){
            	$("#uploadedResources").append(data.filename + "<br/>");
            	$("#moduleResource").val("");
        	}
        }
    });
}


/**
 * Add a module
 */
addModule = function()
{
	var templates = $("#module-templates").val();
	var name = $("#module-name").val();
	var tag = $("#module-tag").val();
	var HTMLTag = $("#module-HTMLTag").val();
	
	errors = "";
	if (templates == null || templates.length == 0){
		errors += "Please select at least one template. <br/>"
	}
	if (name.trim().length == 0){
		errors += "Please enter a valid name for the module. <br/>"
	}
	if (tag.trim().length == 0){
		errors += "Please enter a valid tag name. <br/>"
	}
	if (HTMLTag.trim().length == 0){
		errors += "Please enter a valid HTML tag. <br/>"
	}
	if (errors == ""){
		add_module(templates, name, tag, HTMLTag);
	}else{
		$("#errors").html(errors);
		$(function() {
	        $( "#dialog-errors" ).dialog({
	            modal: true,
	            buttons: {
	            	Ok: function() {	
	            		$( this ).dialog( "close" );
	                }
	            }
	        });
	    });
	}	
}


/**
 * AJAX call, adds a module
 * @param templates list of selected templates 
 * @param name name of the module
 * @param tag XML tag to replace
 * @param HTMLTag HTML tag to appear in the form
 */
add_module = function(templates, name, tag, HTMLTag){
    $.ajax({
        url : "/admin/add_module",
        type : "POST",
        dataType: "json",
        data : {
        	templates : templates,
        	name: name,
        	tag: tag,
        	HTMLTag: HTMLTag
        },
        success: function(data){
        	addModuleCallback();
        }
    });
}


/**
 * Display a message when the module is added.
 */
addModuleCallback = function(){
	$(function() {
        $( "#dialog-added" ).dialog({
            modal: true,
            close: function(){
            	window.location = "module-management"
            },
            buttons: {
            	Ok: function() {	
            		$( this ).dialog( "close" );
                }
            }
        });
    });
}

