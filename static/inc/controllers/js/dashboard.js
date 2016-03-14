/**
 *
 * File Name: dashboard.js
 * Author: Sharief Youssef
 * 		   sharief.youssef@nist.gov
 *
 *		  Xavier SCHMITT
 *		  xavier.schmitt@nist.gov
 *
 * Sponsor: National Institute of Standards and Technology (NIST)
 *
 */

/**
 * Load controllers for template/type upload management
 */
loadUploadManagerHandler = function()
{
    console.log('BEGIN [loadUploadManagerHandler]');
    $('.view').on('click',viewInformation);
    $('.edit').on('click',editInformation);
    $('.delete').on('click', deleteObject);
    console.log('END [loadUploadManagerHandler]');
}

/**
 * View general information of a template or a type
 */
viewInformation = function(objectContent)
{
    var objectContent = $(this).attr("content");
    $.ajax({
        url : "/my-profile/my-dashboard/toXML",
        type : "POST",
        dataType: "json",
        data : {
        	xml : objectContent,
        },
        success: function(data){
            $("#XMLHolder").html(data.XMLHolder);
            $(function() {
                $( "#dialog-view-info" ).dialog({
                    modal: true,
                    height: 430,
                    width: 500,
                    buttons: {
                        Ok: function() {
                            $( this ).dialog( "close" );
                        }
                    }
                });
            });
        }
    });
}

/**
 * Edit general information of a template or a type
 */
editInformation = function()
{
    var objectID = $(this).attr("objectid");
    var objectType = $(this).attr("objecttype");
    var objectFilename = $(this).attr("objectfilename");
    var objectName = $(this).attr("objectname");

    $("#edit-name")[0].value = objectName;
    $("#edit-filename")[0].value = objectFilename;

	$(function() {
        $( "#dialog-edit-info" ).dialog({
            modal: true,
            buttons: {
            	Ok: function() {
					var newName = $("#edit-name")[0].value;
					var newFilename = $("#edit-filename")[0].value;
					edit_information(objectID, objectType, newName, newFilename);
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
 * @param objectType type of the object
 * @param newName new name of the object
 * @param newFilename new filename of the object
 */
edit_information = function(objectID, objectType, newName, newFilename){
    $.ajax({
        url : "/my-profile/my-dashboard/edit_information",
        type : "POST",
        dataType: "json",
        data : {
        	objectID : objectID,
        	objectType : objectType,
        	newName : newName,
        	newFilename : newFilename,
        },
        success: function(data){
            if ('name' in data){
            	showErrorEditType(true);
            }else if ('filename' in data){
            	showErrorEditType(false);
            }else{
                $("#dialog-edit-info").dialog( "close" );
                location.reload();
            }
        }
    });
}


/**
 * Delete a template or a type
 */
deleteObject = function()
{
    console.log('BEGIN [deleteObject]');
    var objectID = $(this).attr("objectid");
    var objectType = $(this).attr("objecttype");
    var objectFilename = $(this).attr("objectfilename");
    var objectName = $(this).attr("objectname");

    document.getElementById("object-to-delete").innerHTML = objectName;
    $(function() {
        $( "#dialog-deleteconfirm-message" ).dialog({
            modal: true,
            buttons: {
		Yes: function() {
					delete_object(objectID, objectType);
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
 * AJAX call, delete an object
 * @param objectID id of the object
 * @param objectType type of the object
 */
delete_object = function(objectID, objectType){
    $.ajax({
        url : "/my-profile/my-dashboard/delete_object",
        type : "POST",
        dataType: "json",
        data : {
        	objectID : objectID,
        	objectType : objectType,
        },
        success: function(data){
            if ('Type' in data) {
                var text = 'You cannot delete this Type because it is used by at least one template or type: '+data['Type'];
                showErrorDelete(text);
            } else if('Template' in data) {
                var text = 'You cannot delete this Template because it is used by at least one resource or form: '+data['Template'];
                showErrorDelete(text);
            } else {
                location.reload();
            }

        }
    });
}

/**
 * Display error message when you have an error while deleting
 */
showErrorDelete = function(text){
	$(function() {
	    $( "#dialog-error-delete" ).html(text);
        $( "#dialog-error-delete" ).dialog({
            modal: true,
            buttons: {
			Ok: function() {
                $( this ).dialog( "close" );
	          },
		    }
        });
    });
}


/**
 * Display error message when bad edition of type
 */
showErrorEditType = function(name){
	$(function() {
	    if (name) {
	        $( "#dialog-error-edit" ).html('A type with this name already exists.');
	    } else {
	        $( "#dialog-error-edit" ).html('A type with this filename already exists.');
	    }
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

initBanner = function()
{
    $("[data-hide]").on("click", function(){
        $(this).closest("." + $(this).attr("data-hide")).hide(200);
    });
}