/**
 *
 * File Name: dashboard.js
 * Author: Sharief Youssef
 * 		   sharief.youssef@nist.gov
 *
 *		   Xavier SCHMITT
 *		   xavier.schmitt@nist.gov
 *
 * Sponsor: National Institute of Standards and Technology (NIST)
 *
 */

/**
* Allows to check or uncheck all checkboxs by their id.
*/

function countChecked() {
      var numberChecked = $( "input:checked" ).length;
      if (numberChecked == 0) {
        $("#id_actions").fadeTo(200, 0)
        document.getElementById("dropdownMenu1").disabled=true;
      } else {
        $("#id_actions").fadeTo(200, 1)
        document.getElementById("dropdownMenu1").disabled=false;
      }
};

function selectAll(source, id) {
    var checked = source.checked;
    var cb = document.getElementsByName(id);
    for (var i=0; i<cb.length; i++) {
        cb[i].checked=checked;
    }
}

function resetAdminCheckBox() {
    var cb = document.getElementsByName('admin');
    for (var i=0; i<cb.length; i++) {
        cb[i].checked=false;
    }
    $('#select_all_admin').prop('checked', false);
    countChecked();
}

function resetOtherCheckBox() {
    var cb = document.getElementsByName('other');
    for (var i=0; i<cb.length; i++) {
        cb[i].checked=false;
    }
    $('#select_all_other').prop('checked', false);
    countChecked();
}

function initForm() {
    $('#table-forms-admin').DataTable({
    "scrollY": "226px",
    "iDisplayLength": 5,
    "scrollCollapse": true,
    "lengthMenu": [ 5, 10, 15, 20 ],
    "columnDefs": [
            {"className": "dt-center", "targets": 0}
          ],
    order: [[2, 'asc']],
    "columns": [ { "orderable": false }, null, null, null, { "orderable": false } ],
    "fnInfoCallback": function( oSettings, iStart, iEnd, iMax, iTotal, sPre ) {
        resetAdminCheckBox();
        $( "input[type=checkbox]" ).on( "change", countChecked );
      }
    });

    $('#table-forms-other').DataTable({
    "scrollY": "226px",
    "iDisplayLength": 5,
    "scrollCollapse": true,
    "lengthMenu": [ 5, 10, 15, 20 ],
    "columnDefs": [
            {"className": "dt-center", "targets": 0}
          ],
    order: [[2, 'asc']],
    "columns": [ { "orderable": false }, null, null, null, { "orderable": false } ],
    "fnInfoCallback": function( oSettings, iStart, iEnd, iMax, iTotal, sPre ) {
        resetOtherCheckBox();
        $( "input[type=checkbox]" ).on( "change", countChecked );
      }
    });
}

function initRecord() {
    $('#table-records-admin').DataTable({
    "scrollY": "226px",
    "iDisplayLength": 5,
    "scrollCollapse": true,
    "lengthMenu": [ 5, 10, 15, 20 ],
    "columnDefs": [
            {"className": "dt-center", "targets": 0}
          ],
    order: [[2, 'asc']],
    "columns": [ { "orderable": false }, null, null, null, { "orderable": false } ],
    "fnInfoCallback": function( oSettings, iStart, iEnd, iMax, iTotal, sPre ) {
        resetAdminCheckBox();
        $( "input[type=checkbox]" ).on( "change", countChecked );
      }
    });

    $('#table-records-other').DataTable({
    "scrollY": "226px",
    "iDisplayLength": 5,
    "scrollCollapse": true,
    "lengthMenu": [ 5, 10, 15, 20 ],
    "columnDefs": [
            {"className": "dt-center", "targets": 0}
          ],
    order: [[2, 'asc']],
    "columns": [ { "orderable": false }, null, null, null, { "orderable": false } ],
    "fnInfoCallback": function( oSettings, iStart, iEnd, iMax, iTotal, sPre ) {
        resetOtherCheckBox();
        $( "input[type=checkbox]" ).on( "change", countChecked );
      }
    });
}

/**
* Count the number of checked boxes to control visibility of action dropdown
*/
function initAdmin() {

    countChecked();
    $( "input[type=checkbox]" ).on( "change", countChecked );

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $.fn.dataTable
            .tables( { visible: true, api: true } )
            .columns.adjust();
    })
}

/**
 * Load controllers for template/type upload management
 */
loadUploadManagerHandler = function()
{
    console.log('BEGIN [loadUploadManagerHandler]');
    $('.result').on('click',viewInformation);
    $('.edit').on('click',editInformation);
    $('.modules').on('click', manageModules);
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
        url : "/dashboard/toXML",
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
        url : "/dashboard/edit_information",
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
    var url = $(this).attr("url");

    document.getElementById("object-to-delete").innerHTML = objectName;
    $(function() {
        $( "#dialog-deleteconfirm-message" ).dialog({
            modal: true,
            buttons: {
		Yes: function() {
					delete_object(objectID, objectType, url);
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
 * @param url mdcs url
 */
delete_object = function(objectID, objectType, url){
    $.ajax({
        url : "/dashboard/delete_object",
        type : "POST",
        dataType: "json",
        data : {
        	objectID : objectID,
        	objectType : objectType,
        	url : url,
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
 * Redirects to module management page
 */
manageModules = function()
{
    var modelName = $(this).parent().siblings(':first').text();
    var modelFilename = $(this).parent().siblings(':nth-child(2)').text();
    var tdElement = $(this).parent();
    var objectID = $(this).attr("objectid");
    var objectType = $(this).attr("objectType");

    window.location = "modules?id=" + objectID  + '&type=' + objectType
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

/**
 * Delete a curated document
 * @param result_id
 */
deleteResult = function(result_id){
    var selected = []
    selected.push(result_id)
	$(function() {
        $( "#dialog-delete-result" ).dialog({
            modal: true,
            buttons: {
            	Cancel: function() {
                    $( this ).dialog( "close" );
                },
            	Delete: function() {
                    $( this ).dialog( "close" );
                    delete_result(selected);
                },
            }
        });
    });
}

/**
 * AJAX call, delete a curated document
 * @param result_id
 */
delete_result = function(result_id){
	$.ajax({
        url : "/dashboard/delete_result",
        type : "POST",
        dataType: "json",
        data : {
        	result_id: result_id,
        },
		success: function(data){
		        location.reload(true);
	    }
    });
}


/**
 * Publish a curated document
 * @param result_id
 */
updatePublish = function(result_id){
	$(function() {
        $( "#dialog-publish" ).dialog({
            modal: true,
            buttons: {
            	Cancel: function() {
                    $( this ).dialog( "close" );
                },
            	Publish: function() {
                    $( this ).dialog( "close" );
                    update_publish(result_id);
                },
            }
        });
    });
}

/**
 * AJAX call, update the publish state and date of a XMLdata
 * @param result_id
 */
update_publish = function(result_id){
	$.ajax({
        url : "/dashboard/update_publish",
        type : "GET",
        dataType: "json",
        data : {
        	result_id: result_id,
        },
		success: function(data){
		    location.reload();
	    }
    });
}

/**
 * Unpublish a curated document
 * @param result_id
 */
updateUnpublish = function(result_id){
	$(function() {
        $( "#dialog-unpublish" ).dialog({
            modal: true,
            buttons: {
            	Cancel: function() {
                    $( this ).dialog( "close" );
                },
            	Unpublish: function() {
                    $( this ).dialog( "close" );
                    update_unpublish(result_id);
                },
            }
        });
    });
}

/**
 * AJAX call, update the publish state of a XMLdata
 * @param result_id
 */
update_unpublish = function(result_id){
	$.ajax({
        url : "/dashboard/update_unpublish",
        type : "GET",
        dataType: "json",
        data : {
        	result_id: result_id,
        },
		success: function(data){
            $("#" + result_id).load(document.URL +  " #" + result_id);
	    }
    });
}

/**
 * Change record owner
 * @param recordID
 */
changeOwnerRecord = function(recordID){
    var selected = []
    selected.push(recordID)
    $("#banner_errors").hide();
    $(function() {
        $( "#dialog-change-owner-record" ).dialog({
            modal: true,
            buttons: {
                Cancel: function() {
                    $( this ).dialog( "close" );
                },
                "Change": function() {
                    if (validateChangeOwner()){
                        var formData = new FormData($( "#form_start" )[0]);
                        change_owner_record(selected);
                    }
                },
            }
        });
    });
}

/**
 * Validate fields of the start curate form
 */
validateChangeOwner = function(){
    errors = ""

    $("#banner_errors").hide()
    // check if a user has been selected
    if ($( "#id_users" ).val().trim() == ""){
        errors = "Please provide a user."
    }

    if (errors != ""){
        $("#form_start_errors").html(errors);
        $("#banner_errors").show(500)
        return (false);
    }else{
        return (true);
    }
}


/**
 * AJAX call, change record owner
 * @param recordID
 */
change_owner_record = function(recordID){
    var userId = $( "#id_users" ).val().trim();
    $.ajax({
        url : "/dashboard/change-owner-record",
        type : "POST",
        dataType: "json",
        data : {
            recordID: recordID,
            userID: userId,
        },
		success: function(data){
			window.location = "/dashboard/records"
	    },
        error:function(data){
            $("#form_start_errors").html(data.responseText);
            $("#banner_errors").show(500)
        }
    });
}

/**
* JS script that allows to do the action on the user dashboard
*/
action_dashboard = function(selectValue) {

    var selected = [];
    $('#actionCheckbox input:checked').each(function() {
        selected.push($(this).attr('id'));
    });

    // Delete record
    if (selectValue == 1) {
        $(function() {
            $( "#dialog-delete-result" ).dialog({
                modal: true,
                buttons: {
                    Cancel: function() {
                        $( this ).dialog( "close" );
                    },
                    Delete: function() {
                        $( this ).dialog( "close" );
                        delete_result(selected);
                    },
                }
            });
        });
    // Change owner record
    } else if (selectValue == 2) {
        $("#banner_errors").hide();
        $(function() {
            $( "#dialog-change-owner-record" ).dialog({
                modal: true,
                buttons: {
                    Cancel: function() {
                        $( this ).dialog( "close" );
                    },
                    "Change": function() {
                        if (validateChangeOwner()) {
                            var formData = new FormData($( "#form_start" )[0]);
                            change_owner_record(selected);
                        }
                    },
                }
            });
        });
    // Delete form
    } else if (selectValue == 3) {
        $("#banner_errors").hide();
        $(function() {
            $( "#dialog-delete-form" ).dialog({
                modal: true,
                buttons: {
                    Cancel: function() {
                        $( this ).dialog( "close" );
                    },
                    Delete: function() {
                        $( this ).dialog( "close" );
                        delete_forms(selected);
                    },
                }
            });
        });
    // Change owner form
    } else if (selectValue == 4) {
        $("#banner_errors").hide();
        $(function() {
            $( "#dialog-change-owner-form" ).dialog({
                modal: true,
                buttons: {
                    Cancel: function() {
                        $( this ).dialog( "close" );
                    },
                    "Change": function() {
                        if (validateChangeOwner()) {
                            var formData = new FormData($( "#form_start" )[0]);
                            change_owner_forms(selected);
                        }
                    },
                }
            });
        });
    }
}


/**
 * AJAX call, delete selected forms
 * @param formID
 */
delete_forms = function(formsID){
    $.ajax({
        url : "/dashboard/delete-forms",
        type : "POST",
        dataType: "json",
        data : {
            formsID: formsID,
        },
		success: function(data){
			window.location = "/dashboard/forms"
	    },
        error:function(data){
        	window.location = "/dashboard/forms"
        }
    });
}

/**
 * AJAX call, change selected forms owner
 * @param formID
 */
change_owner_forms = function(formID){
    var userId = $( "#id_users" ).val().trim();
    $.ajax({
        url : "/dashboard/change-owner-forms",
        type : "POST",
        dataType: "json",
        data : {
            formID: formID,
            userID: userId,
        },
		success: function(data){
			window.location = "/dashboard/forms"
	    },
        error:function(data){
        	window.location = "/dashboard/forms"
        }
    });
}