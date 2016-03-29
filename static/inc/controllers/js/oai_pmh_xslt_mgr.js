displayOaiImport = function()
{
 $(function() {
    $("#form_oai_pmh_start_errors").html("");
    $( "#dialog-oai-pmh-message" ).dialog({
      modal: true,
      width: 500,
      buttons:
    	  [
           {
               text: "Upload",
               click: function() {
                    if(validateOaiExport())
                    {
                       var formData = new FormData($( "#form_oai_pmh_start" )[0]);
	            	   $.ajax({
	            	        url: "/oai_pmh/admin/manage-xslt",
	            	        type: 'POST',
	            	        data: formData,
	            	        cache: false,
	            	        contentType: false,
	            	        processData: false,
	            	        async:false,
	            	   		success: function(data){
                                window.location = '/admin/xml-schemas/manage-xslt'
	            	        },
	            	        error:function(data){
	            	        	$("#form_oai_pmh_start_errors").html(data.responseText);
	            	        },
	            	    })
	            	    ;
                    }
               }
           }
          ]
    });
  });
}


validateOaiExport = function()
{
    errors = ""
    if ($( "#id_oai_name" ).val().trim() == ""){
        errors = "Please enter a name."
    }
	// check if an option has been selected
    else if ($( "#id_oai_pmh_xslt_file" ).val() == ""){
        errors = "Please select an XSLT file."
    }

	if (errors != ""){
		$("#form_oai_pmh_start_errors").html(errors);
		return (false);
	}else{
		return (true)
	}
}



deleteOaiXSLT = function(xslt_id)
{
 $(function() {
    $( "#dialog-deletexslt-message" ).dialog({
      modal: true,
      buttons:{
            	Delete: function() {
            		delete_OAI_XSLT(xslt_id);
            		$( this ).dialog( "close" );
            		},
				Cancel: function() {
	                $( this ).dialog( "close" );
		          },
		    }
    });
  });
}

/**
 * AJAX call, deletes an XSLT File
 * @param bucket_id id of the bucket
 */
delete_OAI_XSLT = function(elt){
    var xslt_id = $(elt).attr("objectid");
    var typeXSLT = $(elt).attr("typeXSLT");

    var urlDelete = "/oai_pmh/admin/delete-xslt"
    $.ajax({
        url : urlDelete,
        type : "POST",
        dataType: "json",
        data : {
        	xslt_id : xslt_id,
        },
        success: function(data){
            window.location = '/admin/xml-schemas/manage-xslt'
        },
        error:function(data){
            $("#form_start_errors").html(data.responseText);
            $( "#form_start_errors").dialog({
                modal: true,
                buttons: {
                Ok: function() {
                    $( this ).dialog( "close" );
                  },
                }
            });
	    }
    });
}

/**
 * Edit general information of a template or a type
 */
editOaiInformation = function(objectID)
{
    var objectName = $(this).parent().siblings(':first').text();
    var objectID = $(this).attr("objectid");
    var typeXSLT = $(this).attr("typeXSLT");
    $("#form_edit_errors").html("");
    $("#edit-name")[0].value = objectName;

	$(function() {
        $( "#dialog-edit-message" ).dialog({
            modal: true,
            width: 500,
            buttons: {
            	Ok: function() {
					var newName = $("#edit-name")[0].value;
					if (newName == ""){
                        $("#form_edit_errors").html("<font color='red'>Please enter a name.</font><br/>");
                    }
                    else
                    {
					    edit_oai_information(objectID, newName, typeXSLT);
					}
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}


/**
 * AJAX call, edit information of an object
 * @param objectID id of the object
 * @param newName new name of the object
 */
edit_oai_information = function(objectID, newName, typeXSLT){
    var urlEdit = "/oai_pmh/admin/edit-xslt"
    $.ajax({
        url : urlEdit,
        type : "POST",
        dataType: "json",
        data : {
        	object_id : objectID,
        	new_name : newName,
        },
        success: function(data){
            window.location = '/admin/xml-schemas/manage-xslt'
        },
        error:function(data){
            $("#form_edit_errors").html(data.responseText);
        }
    });
}



enterKeyPressSubscriptionOAI = function ()
{
    $('#id_oai_pmh_name').keypress(function(event) {
        if(event.which == $.ui.keyCode.ENTER){
            event.preventDefault();
            event.stopPropagation();
        }
    });
}


InitOai = function(){
    $('#EditOAI').on('click', editOaiInformation);
    enterKeyPressSubscriptionOAI();
}


saveMyTemplate = function ()
{
    if (validateSaveTemplate()){
       var formData = new FormData($( "#form_start" )[0]);
       $.ajax({
            url: "oai-pmh-conf-xslt",
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            async:false,
            success: function(data){
                saveTemplateCallback();
            },
            error:function(data){
                $("#form_start_errors").html(data.responseText);
            },
        })
        ;
   }
}

/**
 * Display success window
 */
saveTemplateCallback = function(){
	console.log('BEGIN [saveTemplate]');

	$(function() {
		$("#dialog-save").dialog({
		  modal: true,
		  buttons: {
			OK: function() {
					window.location = '/admin/xml-schemas/manage-schemas'
			   	}
		      }
		    });
	  });

	console.log('END [saveTemplate]');
}

/**
 * Validate fields of the start curate form
 */
validateSaveTemplate = function(){
//	errors = ""
//
//	$("#banner_errors").hide()
//
//	$("#").find("input:checked").each(function() {
//		  values.push($(this).val());
//	});
//
//	// check if an option has been selected
//	selected_option = $( "#form_start" ).find("input:radio[name='curate_form']:checked").val()
//	if (selected_option == undefined){
//		errors = "No option selected. Please check one radio button."
//		$("#form_start_errors").html(errors);
//		$("#banner_errors").show(500)
//		return (false);
//	}else{
//		if (selected_option == "new"){
//			if ($( "#id_document_name" ).val().trim() == ""){
//				errors = "You selected the option 'Create a new document'. Please provide a name for the document."
//			}
//		}else if (selected_option == "open"){
//			if ($( "#id_forms" ).val() == ""){
//				errors = "You selected the option 'Open a Form'. Please select an existing form from the list."
//			}
//		}else if (selected_option == "upload"){
//			if ($( "#id_file" ).val() == ""){
//				errors = "You selected the option 'Upload a File'. Please select an XML file."
//			}
//		}
//	}
//
//	if (errors != ""){
//		$("#form_start_errors").html(errors);
//		$("#banner_errors").show(500)
//		return (false);
//	}else{
//		return (true)
//	}
    return true;
}