loadModuleManagerHandler = function()
{
    console.log('BEGIN [loadModuleManagerHandler]');    
    
    console.log('END [loadModuleManagerHandler]');
}


loadAddModuleHandler = function()
{
    console.log('BEGIN [loadAddModuleHandler]');
    document.getElementById('moduleResource').addEventListener('change',handleModuleResourceUpload, false);
    Dajaxice.curate.initModuleManager(Dajax.process);
    console.log('END [loadAddModuleHandler]');
}

function handleModuleResourceUpload(evt) {
	var files = evt.target.files; // FileList object
    reader = new FileReader();
    reader.onload = function(e){
    	Dajaxice.curate.addModuleResource(Dajax.process,{"resourceContent":reader.result, "resourceFilename":files[0].name});
    }
    reader.readAsText(files[0]);
}

uploadResource = function()
{
	Dajaxice.curate.uploadResource(Dajax.process);
}

addModule = function()
{
	var template = $("#module-template").val();
	var name = $("#module-name").val();
	var tag = $("#module-tag").val();
	var HTMLTag = $("#module-HTMLTag").val();
	Dajaxice.curate.addModule(Dajax.process, {"template":template, "name":name, "tag":tag, "HTMLTag": HTMLTag});
}