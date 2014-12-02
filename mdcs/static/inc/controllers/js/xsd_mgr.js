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
    
   
	versionDialog = $('<div title="Manage Versions" id="dialog-manage-versions">'+
			'<iframe id="version-upload-frame" style="width:500px;height:auto; min-height:400px;" src="/admin/manage-versions?id='+ objectID +'&type='+ objectType +'">'+
			'</iframe>'+	
	  '</div>' ).dialog({
        modal: true,
        width:520,
        height:510,
        resizable:false,
        close: function(event, ui){
        	$(this).dialog('destroy').remove();
        	$('#model_selection').load(window.parent.document.URL +  ' #model_selection', function() {
        	      loadUploadManagerHandler();
        	});  
        },
        buttons: {
        	OK: function() {
        		$(this).dialog('close');
                $('#model_selection').load(document.URL +  ' #model_selection', function() {
                    loadUploadManagerHandler();
                }); 
            },
            Cancel: function() {
            	$(this).dialog('close');
                $('#model_selection').load(document.URL +  ' #model_selection', function() {
                    loadUploadManagerHandler();
                }); 
            }
    }
    });   
}

function handleSchemaVersionUpload(evt) {
	console.log("test")
	var files = evt.target.files; // FileList object
    reader = new FileReader();
    reader.onload = function(e){
    	Dajaxice.admin.setSchemaVersionContent(Dajax.process,{"versionContent":reader.result, "versionFilename":files[0].name});
    }
    reader.readAsText(files[0]);
  }

function handleTypeVersionUpload(evt) {
	var files = evt.target.files; // FileList object
    reader = new FileReader();
    reader.onload = function(e){
    	Dajaxice.admin.setTypeVersionContent(Dajax.process,{"versionContent":reader.result, "versionFilename":files[0].name});
    }
    reader.readAsText(files[0]);
  }

uploadVersion = function()
{
	var objectVersionID = $("#updateVersionBtn").attr("versionid");
	var objectType = $("#updateVersionBtn").attr("objectType");	
	
	Dajaxice.admin.uploadVersion(Dajax.process,{"objectVersionID":objectVersionID, "objectType": objectType})
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
	current = document.getElementById(setCurrent);
	var objectid = $(current).attr("objectid");
	var objectType = $(current).attr("objectType");
	
	Dajaxice.admin.setCurrentVersion(Dajax.process,{"objectid":objectid, "objectType":objectType});
}

deleteVersion = function(toDelete)
{			
	current = document.getElementById(toDelete);
	var objectid = $(current).attr("objectid");
	var objectType = $(current).attr("objectType");
	Dajaxice.admin.assignDeleteCustomMessage(Dajax.process,{"objectid":objectid, "objectType":objectType});
	$(function() {
//			$(window.parent.document).find('#dialog-deleteversion-message').dialog({
			$('#dialog-deleteversion-message').dialog({
	            modal: true,
	            buttons: {
	            	Yes: function() {	
						var newCurrent = ""
						try{
							var idx = $("#selectCurrentVersion")[0].selectedIndex
							newCurrent = $("#selectCurrentVersion")[0].options[idx].value
						}
						catch(e){}
						Dajaxice.admin.deleteVersion(Dajax.process,{"objectid":objectid, "objectType":objectType,"newCurrent":newCurrent});
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
    
    Dajaxice.admin.restoreObject(Dajax.process,{'objectid':objectID, 'objectType':objectType});
}

restoreVersion = function(toRestore)
{
	current = document.getElementById(toRestore);
	var objectID = $(current).attr("objectid");
	var objectType = $(current).attr("objectType");
	
	Dajaxice.admin.restoreVersion(Dajax.process,{'objectid':objectID, 'objectType':objectType});
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
					Dajaxice.admin.editInformation(Dajax.process,{'objectid':objectID, 'objectType':objectType, 'newName':newName,'newFilename':newFilename});
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

    Dajaxice.admin.deleteObject(deleteObjectCallback,{'objectID':objectID, "objectType":objectType});

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


showErrorEditType = function(){
	$(function() {
        $( "#dialog-error-edit" ).dialog({
            modal: true,
            buttons: {
			Ok: function() {
                $( this ).dialog( "close" );
	          },
		    }
        });
    });
}
