/**
 * 
 */
loadAddRemoveFileController = function()
{
	$(':file').live('change', importFile);
	$('.remove.input').live('click', removeFile);
}

/**
 * 
 */
importFile = function()
{
	var browserFileName = $(this).val(),
		splitFileName, fileName = '';
	
	if(browserFileName.indexOf('/')!=-1) // UNIX file system
	{
		splitFileName = browserFileName.split('/');
		fileName = splitFileName.pop();
	}
	else if(browserFileName.indexOf('\\')!=-1) // Windows file system
	{
		splitFileName = browserFileName.split('\\');
		fileName = splitFileName.pop();
	}
	else // No path separator
	{
		fileName = browserFileName;
	}
	
	var statusField = $(this).siblings('.table_import_status');
	
	console.log('[importFile] Importing '+fileName+' ...');	
	statusField.text('Importing file...');
	
	// todo more controls on the file (see if content really is xls or xlsx)
	if(fileName.indexOf('.xls', fileName.length - 4)==-1 && fileName.indexOf('.xlsx', fileName.length - 5)==-1)
	{
		statusField.text('File format is not good. Please upload a different file.');
		return;
	}
	
	console.log($("#file_upload")[0].files);
	
	var formData = new FormData($("#file_upload")[0]),
		newFileInput = $(this).parent().clone(true),
		parent = $(this).parent();
	
	//formData.append('file', $('#file_upload')[0]);
	
	$.ajax({
        url: 'parser/_plugins/table/controllers/php/addRemoveFile.php',  //server script to process data
        type: 'POST',
        //xhr: function() {  // custom xhr
            /*myXhr = $.ajaxSettings.xhr();
	       	if(myXhr.upload){ // check if upload property exists
	                myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // for handling the progress of the upload
            }
            return myXhr;*/
        //},
        //Ajax events
        success: function(data) {
        	data = $.parseJSON(data);
        	
        	if(data.code == 0)
        	{
        		// Display the new file input
	        	newFileInput.find('.table_import_status').text('');
	        	parent.after(newFileInput);
	        	
	        	
	        	// Starting the conversion           	
	           	statusField.text('Converting file...');
	           	convertFile(fileName, statusField);
        	}
        	else
        	{
        		statusField.text('Impossible to save the file on the server. Try later or contact a system administrator');
        		console.error("[importFile] Error "+data.code+" :"+data.result);
        	}
        },
        error: function() {
            console.error("[importFile] Problem uploading the file");
        },
        // Form data
        data: formData,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
convertFile = function(file, statusField)
{	
	// Converting the file in xml
    $.ajax({
            url: 'parser/_plugins/table/controllers/php/parseFile.php',  //server script to process data
            type: 'GET',
            /*xhr: function() {  // custom xhr
                myXhr = $.ajaxSettings.xhr();*/
                /*if(myXhr.upload){ // if upload property exists
                    myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // progressbar
                }*/
                /*return myXhr;
            },*/
            //Ajax events
            success: function(data) {
            	var jsonData = $.parseJSON(data);
            	
            	statusField.html(htmlspecialchars_decode(jsonData.result));
            },
            error: function() {
                console.error("Problem converting the file");
            },
            // Form data
            data: 't_file='+file,
            //Options to tell JQuery not to process data or worry about content-type
            cache: false,
            contentType: false,
            processData: false
    });
}

/**
 * 
 */
removeFile = function()
{
	var htmlToRemove = $(this).parent().parent(),
		inputFileName = htmlToRemove.children('input').val(),
		fileName;
	
	if(inputFileName.indexOf('/')!=-1) // UNIX file system
	{
		var splitFileName = inputFileName.split('/');
		fileName = splitFileName.pop();
	}
	else if(inputFileName.indexOf('\\')!=-1) // Windows file system
	{
		var splitFileName = inputFileName.split('\\');
		fileName = splitFileName.pop();
	}
	else // No path separator
	{
		fileName = inputFileName;
	}
	
	htmlToRemove.remove();
}
