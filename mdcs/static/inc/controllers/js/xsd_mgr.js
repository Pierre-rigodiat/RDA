/**
 * 
 */
loadUploadManagerHandler = function()
{
    console.log('BEGIN [loadUploadManagerHandler]');
    $('.retrieve').on('click',restoreObject);
    $('.edit').on('click',editInformation);
    $('.version').on('click', manageVersions);    
    $('.delete').on('click', deleteObject);
    $('.copy').on('click', copyObject);
    $('.upload').on('click', uploadObject);
    console.log('END [loadUploadManagerHandler]');
}

manageVersions = function()
{
    var modelName = $(this).parent().siblings(':first').text();
    var modelFilename = $(this).parent().siblings(':nth-child(2)').text();
    var tdElement = $(this).parent();
    var objectID = $(this).attr("objectid");
    var objectType = $(this).attr("objectType");
    
    Dajaxice.curate.manageVersions(Dajax.process, {"objectID": objectID, "objectType": objectType});    
}

function handleSchemaVersionUpload(evt) {
	var files = evt.target.files; // FileList object
    reader = new FileReader();
    reader.onload = function(e){
    	Dajaxice.curate.setSchemaVersionContent(Dajax.process,{"versionContent":reader.result, "versionFilename":files[0].name});
    }
    reader.readAsText(files[0]);
  }

function handleOntologyVersionUpload(evt) {
	var files = evt.target.files; // FileList object
    reader = new FileReader();
    reader.onload = function(e){
    	Dajaxice.curate.setOntologyVersionContent(Dajax.process,{"versionContent":reader.result, "versionFilename":files[0].name});
    }
    reader.readAsText(files[0]);
  }

uploadVersion = function()
{
	var objectVersionID = $("#updateVersionBtn").attr("versionid");
	var objectType = $("#updateVersionBtn").attr("objectType");	
	
	Dajaxice.curate.uploadVersion(Dajax.process,{"objectVersionID":objectVersionID, "objectType": objectType})
}

showUploadErrorDialog = function()
{
	$(function() {
        $( "#dialog-upload-error" ).dialog({
            modal: true,
            buttons: {
            	Ok: function() {	
            		$( this ).dialog( "close" );
                }
            }
        });
    });
}

setCurrentVersion = function(setCurrent)
{
	var objectid = $(setCurrent).attr("objectid");
	var objectType = $(setCurrent).attr("objectType");
	
	Dajaxice.curate.setCurrentVersion(Dajax.process,{"objectid":objectid, "objectType":objectType});
}

deleteVersion = function(toDelete)
{			
	var objectid = $(toDelete).attr("objectid");
	var objectType = $(toDelete).attr("objectType");
	Dajaxice.curate.assignDeleteCustomMessage(Dajax.process,{"objectid":objectid, "objectType":objectType});
	$(function() {
	        $( "#dialog-deleteversion-message" ).dialog({
	            modal: true,
	            buttons: {
			Yes: function() {	
						var newCurrent = ""
						try{
							var idx = $("#selectCurrentVersion")[0].selectedIndex
							newCurrent = $("#selectCurrentVersion")[0].options[idx].value
						}
						catch(e){}
						Dajaxice.curate.deleteVersion(Dajax.process,{"objectid":objectid, "objectType":objectType,"newCurrent":newCurrent});
	                    $( this ).dialog( "close" );
	                },
			No: function() {
	                    $( this ).dialog( "close" );
	                }
		    }
	        });
	    });
}

restoreObject = function()
{
    var objectID = $(this).attr("objectid");
    var objectType = $(this).attr("objectType");
    
    Dajaxice.curate.restoreObject(Dajax.process,{'objectid':objectID, 'objectType':objectType});
}

restoreVersion = function(toRestore)
{
	var objectID = $(toRestore).attr("objectid");
	var objectType = $(toRestore).attr("objectType");
	
	Dajaxice.curate.restoreVersion(Dajax.process,{'objectid':objectID, 'objectType':objectType});
}

editInformation = function()
{
    var objectName = $(this).parent().siblings(':first').text();
    var objectFilename = $(this).parent().siblings(':nth-child(2)').text();
    var objectID = $(this).attr("objectid");
    var objectType = $(this).attr("objectType");
    
    $("#edit-name")[0].value = objectName;
    $("#edit-filename")[0].value = objectFilename;
    
	$(function() {
        $( "#dialog-edit-info" ).dialog({
            modal: true,
            buttons: {
            	Ok: function() {	
					var newName = $("#edit-name")[0].value;
					var newFilename = $("#edit-filename")[0].value;
					Dajaxice.curate.editInformation(Dajax.process,{'objectid':objectID, 'objectType':objectType, 'newName':newName,'newFilename':newFilename});
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}

/**
 * 
 */
displayModelSelectedDialog = function()
{
 $(function() {
    $( "#dialog-message" ).dialog({
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });
}

/**
 * 
 */
//setCurrentModel = function()
//{
//    console.log('BEGIN [setCurrentModel]');
//    var modelName = $(this).parent().siblings(':first').text();
//    var modelFilename = $(this).parent().siblings(':nth-child(2)').text();
//    var tdElement = $(this).parent();
//	
//    $('.add').off('click');
//		
//    tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
//		
//    console.log('[setCurrentModel] Loading '+modelName+' with filename '+modelFilename+' as current model...');
//
//    Dajaxice.curate.setCurrentModel(setCurrentModelCallback,{'modelFilename':modelFilename});
//	
////    $.ajax({
////        url: 'inc/controllers/php/schemaLoader.php',
////        type: 'GET',
////        success: function(data) {
////        	// Refresh the page
////        	loadPage($(location).attr('href')+'?manageSchemas');
////        	console.log('[setCurrentModel] '+modelName+' loaded');
////        },
////        error: function() {
////            console.error("[setCurrentModel] A problem occured during schema loading");
////        },
////        // Form data
////        data: 'n='+modelName,
////        //Options to tell JQuery not to process data or worry about content-type
////        cache: false,
////        contentType: false,
////        processData: false
////    });
//
//    console.log('END [setCurrentModel]');
//}

setCurrentModelCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [setCurrentModelCallback]');
//    location.reload();

//    var messageLocation = $("#main").children(":first");
//    messageLocation.hide().html("Template Successfully Selected").fadeIn(500);
//    messageLocation.delay(2000).fadeOut(500);

    $('#model_selection').load(document.URL +  ' #model_selection', function() {
	loadUploadManagerHandler();
	//displayModelSelectedDialog();
    });
    console.log('END [setCurrentModelCallback]');
}

/**
 * 
 */
deleteObject = function()
{
    console.log('BEGIN [deleteObject]');
    var objectName = $(this).parent().siblings(':first').text();
    var objectFilename = $(this).parent().siblings(':nth-child(2)').text();
    var objectID = $(this).attr("objectid");
    var objectType = $(this).attr("objectType");

    document.getElementById("object-to-delete").innerHTML = objectName;

    $(function() {
        $( "#dialog-deleteconfirm-message" ).dialog({
            modal: true,
            buttons: {
		Yes: function() {
                    deleteObjectConfirmed(objectID, objectType);
                    $( this ).dialog( "close" );
                },
		No: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [deleteObject]');
}

/**
 * 
 */
deleteObjectConfirmed = function(objectID, objectType)
{
    console.log('BEGIN [deleteObjectConfirmed('+objectID+')]');

    Dajaxice.curate.deleteObject(deleteObjectCallback,{'objectID':objectID, "objectType":objectType});

    console.log('END [deleteObjectConfirmed('+objectID+')]');
}

/**
 * 
 */
deleteObjectCallback = function(data)
{
    console.log('BEGIN [deleteObjectCallback]');

    Dajax.process(data);

    $('#model_selection').load(document.URL +  ' #model_selection', function() {
	loadUploadManagerHandler();
    });

    console.log('END [deleteObjectCallback]');
}

/**
 * 
 */
copyObject = function()
{
    console.log('BEGIN [copyObject]');

    $(function() {
        $( "#dialog-copied-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [copyObject]');
}

/**
 * 
 */
uploadObject = function()
{
    console.log('BEGIN [uploadObject]');

    document.getElementById('object_name').value = ""
    document.getElementById('files').value = ""
    document.getElementById('list').innerHTML = ""
    document.getElementById('objectNameErrorMessage').innerHTML = ""

    $(function() {
        $( "#dialog-upload-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                },
		Cancel: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [uploadObject]');
}

