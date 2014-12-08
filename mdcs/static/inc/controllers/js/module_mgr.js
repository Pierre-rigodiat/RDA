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
            		Dajaxice.admin.deleteModule(deleteModuleCallback,{"objectid":objectid});
                },
                No:function() {	
            		$( this ).dialog( "close" );
                }
            }
        });
    });
}

/**
 * Update the list of modules
 */
deleteModuleCallback = function(){
    $('#model_selection').load(document.URL +  ' #model_selection', function() {
    	loadModuleManagerHandler();
    });
}

/**
 * Load controllers for module addition
 */
loadAddModuleHandler = function()
{
    console.log('BEGIN [loadAddModuleHandler]');
    document.getElementById('moduleResource').addEventListener('change',handleModuleResourceUpload, false);
    Dajaxice.admin.initModuleManager(Dajax.process);
    console.log('END [loadAddModuleHandler]');
}

/**
 * Handler for reading of resources files
 * @param evt
 */
function handleModuleResourceUpload(evt) {
	var files = evt.target.files; // FileList object
    reader = new FileReader();
    reader.onload = function(e){
    	Dajaxice.admin.addModuleResource(Dajax.process,{"resourceContent":reader.result, "resourceFilename":files[0].name});
    }
    reader.readAsText(files[0]);
}

/**
 * Upload a resource
 */
uploadResource = function()
{
	Dajaxice.admin.uploadResource(Dajax.process);
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
		Dajaxice.admin.addModule(addModuleCallback, {"templates":templates, "name":name, "tag":tag, "HTMLTag": HTMLTag});
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

