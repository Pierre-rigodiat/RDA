/*$(document).ready(function(){
	//$(':input[name^=file]').on('change', createNewInput);
	$('body').on('click', ".remove", removeFile);
});

removeFile = function() {
	$(this).prev().remove();
	$(this).prev().remove();
	$(this).next().remove();
	$(this).remove();
}*/

/*createNewInput = function()
{
	var formData = new FormData($("#file_upload")[0]);	
	var fileName = $(this)[0].files[0].name
	
	// todo more controls on the file (see if content really is xls or xlsx)
	
		
	var id = $(this).attr('id');
	id = id.replace('file[', '');
	id = id.replace(']', '');
	
	var infoTag = "#info\\["+id+"\\]";
	/*console.log("#info\\["+id+"\\]");
	console.log($("#info\\["+id+"\\]"));*/
	
	/*if(fileName.indexOf('.xls', fileName.length - 4)==-1 && fileName.indexOf('.xlsx', fileName.length - 5)==-1)
	{
		$(infoTag).append('File format is not good. Please upload a different file.');
		return;
	}
	
	$(infoTag).append('Uploading file...');	
	
	var newId = parseInt(id)+1;
		
	var clone = $(this).clone(true);
	clone.attr('id', 'file['+newId+']');
	clone.attr('name', 'file['+newId+']');
	clone.after('<span id="info['+newId+']"></span>');
	
	$(this).attr('disabled', 'disabled');	
	
	$(this).next().after(clone);
	$(this).next().after('<br/>');
	$(this).next().after('<span class="remove">Remove</span>');	

    var uploadFileURL = 'inc/ajax/saveFile.php';
    
    
    // Uploading the file on the server
    $.ajax({
            url: uploadFileURL,  //server script to process data
            type: 'POST',
            xhr: function() {  // custom xhr
                myXhr = $.ajaxSettings.xhr();
                /*if(myXhr.upload){ // if upload property exists
                    myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // progressbar
                }*/
               /* return myXhr;
            },
            //Ajax events
            success: function(data) {
            	// Starting the conversion
               	$(infoTag).text('Converting file...');
               	convertFile(fileName, infoTag);
            },
            error: function() {
                console.error("Problem uploading the file");
            },
            // Form data
            data: formData,
            //Options to tell JQuery not to process data or worry about content-type
            cache: false,
            contentType: false,
            processData: false
    });
};

convertFile = function(file, infoTag)
{
	var convertFileURL = 'inc/ajax/excelParser.php';
	
	// Converting the file in xml
    $.ajax({
            url: convertFileURL,  //server script to process data
            type: 'GET',
            xhr: function() {  // custom xhr
                myXhr = $.ajaxSettings.xhr();
                /*if(myXhr.upload){ // if upload property exists
                    myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // progressbar
                }*/
              /*  return myXhr;
            },
            //Ajax events
            success: function(data) {
            	if(data != '0')
            	{
            		$(infoTag).text('Problem during the conversion.');
            	}
            	else
            	{
            		$(infoTag).text('File converted');
            	}
            },
            error: function() {
                console.error("Problem converting the file");
            },
            // Form data
            data: 'xls_file='+file,
            //Options to tell JQuery not to process data or worry about content-type
            cache: false,
            contentType: false,
            processData: false
    });
};*/
