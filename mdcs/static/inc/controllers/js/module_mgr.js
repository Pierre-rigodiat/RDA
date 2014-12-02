loadModuleManagerHandler = function()
{
    console.log('BEGIN [loadModuleManagerHandler]');    
    $('.delete.module').on('click', deleteModule);
    console.log('END [loadModuleManagerHandler]');
}

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

deleteModuleCallback = function(){
    $('#model_selection').load(document.URL +  ' #model_selection', function() {
    	loadModuleManagerHandler();
    });
}

loadAddModuleHandler = function()
{
    console.log('BEGIN [loadAddModuleHandler]');
    document.getElementById('moduleResource').addEventListener('change',handleModuleResourceUpload, false);
    Dajaxice.admin.initModuleManager(Dajax.process);
    console.log('END [loadAddModuleHandler]');
}

function handleModuleResourceUpload(evt) {
	var files = evt.target.files; // FileList object
    reader = new FileReader();
    reader.onload = function(e){
    	Dajaxice.admin.addModuleResource(Dajax.process,{"resourceContent":reader.result, "resourceFilename":files[0].name});
    }
    reader.readAsText(files[0]);
}

uploadResource = function()
{
	Dajaxice.admin.uploadResource(Dajax.process);
}

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

