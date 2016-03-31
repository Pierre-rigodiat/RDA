var emptyEntry = '----------'

clearAdd = function ()
{
    clearAddError();
    $( "#form_add" )[0].reset();
}

clearAddError = function ()
{
    $("#banner_add_errors").hide()
    $("#form_add_errors").html("");
}

clearEditError = function ()
{
    $("#banner_edit_errors").hide()
    $("#form_edit_errors").html("");
}

displayAddRegistry = function()
{
 $(function() {
    clearAdd();
//    $('#duration').durationPicker();

    $( "#dialog-registry" ).dialog({
      modal: true,
      width: 550,
      height: 'auto',
      buttons:
    	  [
    	  {
               text: "Cancel",
               click: function() {
                        $( this ).dialog( "close" );
                    }
           },
           {
               text: "Add",
               click: function() {
                    clearAddError();
                    if(validateRegistry())
                    {
                       $("#banner_add_wait").show(200);
                       var formData = new FormData($( "#form_add" )[0]);
	            	   $.ajax({
	            	        url: "add/registry",
	            	        type: 'POST',
	            	        data: formData,
	            	        cache: false,
	            	        contentType: false,
	            	        processData: false,
	            	        async:true,
	            	   		success: function(data){
                                window.location = 'oai-pmh'
	            	        },
	            	        error:function(data){
	            	            $("#banner_add_wait").hide(200);
	            	        	$("#form_add_errors").html(data.responseText);
                                $("#banner_add_errors").show(200)
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


validateRegistry = function()
{
    errors = ""

    if ($( "#id_url" ).val().trim() == ""){
        errors += "<li>Please enter a URL.</li>"
    }

    harvest = $( "#id_harvestrate" ).val();
    if (!(Math.floor(harvest) == harvest && $.isNumeric(harvest) && harvest > 0)){
        errors += "<li>Please enter a positive integer.</li>"
    }

	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_add_errors").html(errors);
		$("#banner_add_errors").show(200)
		return (false);
	}else{
		return (true)
	}
    return true;
}

validateRegistryEdit = function()
{
    errors = ""

    harvest = $( "#form_edit_current #id_harvestrate" ).val();
    if (harvest.trim() == ''){
        errors += "<li>Please enter an  harvest rate.</li>"
    }
    else if (!(Math.floor(harvest) == harvest && $.isNumeric(harvest) && harvest > 0)){
        errors += "<li>Please enter a positive integer.</li>"
    }

    if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_edit_errors").html(errors);
		$("#banner_edit_errors").show(200)
		return (false);
	}else{
		return (true)
	}
    return true;
}


/**
 * Show a dialog when a result is selected
 */
editRegistry = function(registryId)
{
    exist = load_edit_form(registryId);
    $(function() {
        $( "#dialog-edit" ).dialog({
          modal: true,
          width: 400,
          height: 'auto',
          buttons:
              [
               {
                   text: "Edit",
                   click: function() {
                        clearEditError();
                        if(validateRegistryEdit())
                        {
                            var formData = new FormData($( "#form_edit" )[0]);
                            $.ajax({
                                url: "update/registry",
                                type: 'POST',
                                data: formData,
                                cache: false,
                                contentType: false,
                                processData: false,
                                async:false,
                                success: function(data){
                                    window.location = 'oai-pmh'
                                },
                                error:function(data){
                                    $("#form_edit_errors").html(data.responseText);
                                    $("#banner_edit_errors").show(200)
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


load_edit_form = function(registryId){
	$.ajax({
        url : "update/registry",
        type : "GET",
        dataType: "json",
        data : {
            registry_id : registryId,
        },
        success: function(data){
            $("#form_edit_errors").html("");
            $("#form_edit_current").html(data.template);
//            $('#id_harvestrate').durationPicker();
            Reinit();
        }
    });
}

deleteRegistry = function(registry_id)
{
 $(function() {
    $( "#dialog-confirm-delete" ).dialog({
      modal: true,
      buttons:{
            	Delete: function() {
            		delete_registry(registry_id);
            		},
				Cancel: function() {
	                $( this ).dialog( "close" );
		          },
		    }
    });
  });
}

/**
 * AJAX call, deletes a Registry
 * @param registry_id id of the registry
 */
delete_registry = function(registry_id){
    $("#banner_delete_wait").show(200);
    $.ajax({
        url : 'delete/registry',
        type : "POST",
        dataType: "json",
        data : {
        	RegistryId : registry_id,
        },
        success: function(data){
            window.location = 'oai-pmh'
        },
        error:function(data){
            $("#banner_delete_wait").hide(200);
            $("#form_delete_errors").html(data.responseText);
            $("#banner_delete_errors").show(200);
	    }
    });
}

enterKeyPressSubscription = function ()
{
    $('#id_name').keypress(function(event) {
        if(event.which == $.ui.keyCode.ENTER){
            event.preventDefault();
            event.stopPropagation();
        }
    });

    $('#id_result_name').keypress(function(event) {
        if(event.which == $.ui.keyCode.ENTER){
            event.preventDefault();
            event.stopPropagation();
        }
    });

    $('#id_name').keypress(function(event) {
        if(event.which == $.ui.keyCode.ENTER){
            event.preventDefault();
            event.stopPropagation();
        }
    });
}


checkAllStatus = function ()
{
    var registriesCheck = $("td[id^=Status]")

    $.each(registriesCheck, function(index, props) {
         checkStatus($(props).attr('registryID'), $(props).attr('url'));
    });
}

checkStatus = function (registry_id, url)
{
    $("#Status"+registry_id).css("color", "#000000");
    $("#Status"+registry_id).html('<i class="fa fa-spinner fa-spin"></i>');
    $.ajax({
        url : 'check/registry',
        type : "POST",
        dataType: "json",
        async: true,
        data : {
        	url : url,
        },

        success: function(data){
            if (data.isAvailable)
            {
                $("#Status"+registry_id).html('<i class="fa fa-signal"></i> Available');
                $("#Status"+registry_id).css("color", "#5cb85c");
            }
            else {
                $("#Status"+registry_id).html('<i class="fa fa-signal"></i> Unavailable');
                $("#Status"+registry_id).css("color", "#d9534f");
            }
        },
        error:function(data){
            $("#Status"+registry_id).html('<i class="fa fa-warning"></i> Error while checking');
            $("#Status"+registry_id).css("color", "#d9534f");
        },
    });
}

viewRegistry = function(id){
    $( "#pleaseWaitDialog").show();
	$.ajax({
        url : "oai-pmh-detail-registry?id=" + id,
        type : "GET",
        success: function(data){
            $( "#pleaseWaitDialog").hide();
        	$("#registry_detail").html(data);
        	$(function() {
                $( "#dialog-detail-registry" ).dialog({
                    modal: true,
                    height: 530,
                    width: 700,
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
 * Show/hide
 * @param event
 */
showhide = function(event){
	console.log('BEGIN [showhide]');
	button = event.target
	parent = $(event.target).parent()
	$(parent.children()[2]).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse");
	}else{
		$(button).attr("class","expand");
	}

	console.log('END [showhide]');
}

/**
* Perform check before submit
*/
checkSubmit = function() {
    $("#build_errors").html("");
    $("#banner_build_errors").hide(200);
    $("#downloadXML").hide();
    $("#result").text('');
    var label = '';
    if ($("select#id_dataProvider").val() == '0') {
        label = 'Please pick a data provider.';
    } else if ($("select#id_verb").val() == '0') {
        label = 'Please pick a verb.';
    } else {
        if ($("select#id_verb").val() == '2') {
            if ($("select#id_metadataprefix").val() == '0') {
                label = 'Please pick a metadata prefix.';
            } else if ($("#id_identifiers").val().trim() == '') {
                label = 'Please provide an identifier.';
            }
        } else if ($("select#id_verb").val() == '3') {
            if ($("select#id_metadataprefix").val() == '0' && $("#id_resumptionToken").val() == '') {
                label = 'Please pick a metadata prefix.';
            }
        } else if ($("select#id_verb").val() == '5') {
            if ($("select#id_metadataprefix").val() == '0') {
                label = 'Please pick a metadata prefix.';
            }
        }
    }
    if (label == '') {
        submit();
    } else {
//        $( "#alert" ).html(label);
//        $( "#dialogError" ).dialog({
//            buttons : {
//                'Ok': function() {
//                    $(this).dialog("close");
//                }
//            }
//        });
        $("#banner_build_errors").show(200);
        $("#build_errors").html(label);
    }
}

submit = function() {
                           $("#submitBtn").attr("disabled","disabled");
                           $("#banner_submit_wait").show(200);
                           var identifier = '';
                           var set = '';
                           var from = '';
                           var until = '';
                           var token = '';
                           var metadata = '';

                           if ($("select#id_set").val() != '0') {
                                set += '&set='+$("select#id_set").val();
                           }

                           if ($("select#id_metadataprefix").val() != '0') {
                                metadata += '&metadataPrefix='+$("select#id_metadataprefix").val();
                           }

                           if ($("#id_identifiers").val() != '') {
                                identifier += '&identifier='+$("#id_identifiers").val();
                           }

                           if ($("#id_resumptionToken").val() != '') {
                                token += '&resumptionToken='+$("#id_resumptionToken").val();
                           }

                           if ($("#id_From").val() != '') {
                                from += '&from='+$("#id_From").val();
                           }

                           if ($("#id_until").val() != '') {
                                until += '&until='+$("#id_until").val();
                           }

                           var callURL = '';
                           if ($("select#id_dataProvider").val() != '0') {
                                    callURL = $("select#id_dataProvider").val().split('|')[1];
                           }
                           switch($("select#id_verb").val()) {
                               case '1': callURL+='?verb=Identify'; break;
                               case '2': callURL+='?verb=GetRecord'+identifier+metadata; break;
                               case '3': callURL+='?verb=ListRecords'+set+token+metadata+from+until; break;
                               case '4': callURL+='?verb=ListSets'+token; break;
                               case '5': callURL+='?verb=ListIdentifiers'+metadata+set+token+from+until; break;
                               case '6': callURL+='?verb=ListMetadataFormats'+identifier; break;
                           }

                           $.ajax({
                                    url : 'getdata/',
                                    type : "POST",
                                    dataType: "json",
                                    data : {
                                        url : callURL,
                                    },
                                    success: function(data){
                                        $("#banner_submit_wait").hide(200);
                                        $("#result").html(data.message);
                                        $("#downloadXML").show(100);
                                    },
                                    complete: function(data){
                                        $("#submitBtn").removeAttr("disabled");
                                        $("#banner_submit_wait").hide(200);
                                    },
                                    error:function(data){
                                        $("#banner_submit_wait").hide(200);
                                        $("#banner_build_errors").show(200);
                                        $("#build_errors").html(data.responseText);
                                    }
                                });
}

populateSelect = function() {
                             if ($("select#id_dataProvider").val() == '0') {
                                 $("select#id_set").html("<option>"+emptyEntry+'</option>');
                                 $("select#id_set").attr('disabled', true);
                                 $("select#id_metadataprefix").html('<option>'+emptyEntry+'</option>');
                                 $("select#id_metadataprefix").attr('disabled', true);
                             }
                             else {
                                var id = $("select#id_dataProvider").val().split('|')[0];
                                $.ajax({
                                    url : 'registry/' + id + '/all_sets/',
                                    type : "POST",
                                    dataType: "json",
                                    success: function(data){
                                        var options = '<option value="0">'+emptyEntry+'</option>';
                                         for (var i = 0; i < data.length; i++) {
                                            options += '<option value="' + data[i]['value'] + '">' + data[i]['key'] + '</option>';
                                         }
                                         $("select#id_set").attr('disabled', false);
                                         $("select#id_set").html(options);
                                         $("select#id_set option:first").attr('selected', 'selected');
                                    },
                                });

                                $.ajax({
                                    url : 'registry/' + id + '/all_metadataprefix/',
                                    type : "POST",
                                    dataType: "json",
                                    success: function(data){
                                        var options = '<option value="0">'+emptyEntry+'</option>';
                                         for (var i = 0; i < data.length; i++) {
                                            options += '<option value="' + data[i] + '">' + data[i] + '</option>';
                                         }
                                         $("select#id_metadataprefix").attr('disabled', false);
                                         $("select#id_metadataprefix").html(options);
                                         $("select#id_metadataprefix option:first").attr('selected', 'selected');
                                    },
                                });
                             }
}

/**
 * AJAX call, get XML data and redirects to download view
 */
downloadXmlBuildReq = function(){
    $.ajax({
        url : "download-xml-build-req",
        type : "POST",
        dataType: "json",
        success : function(data) {
            window.location = "download-xml-build-req?id="+ data.xml2downloadID
        },
        error : function(data) {
            $("#banner_build_errors").show(200);
            $("#build_errors").html(data.responseText);
        }
    });
}


clearMyEditError = function ()
{
    $("#banner_edit_my_errors").hide()
    $("#form_edit_errors").html("");
}

editMyRegistry = function()
{
 clearMyEditError();
 exist = load_edit_my_registry_form();
 $(function() {
    $( "#dialog-edit-my-registry" ).dialog({
      modal: true,
      width: 550,
      height: 'auto',
      buttons:
    	  [
    	  {
               text: "Cancel",
               click: function() {
                        $( this ).dialog( "close" );
                    }
           },
           {
               text: "Edit",
               click: function() {
                    clearMyEditError();
                    if(validateEditMyRegistry())
                    {
                       $("#banner_add_wait").show(200);
                       var formData = new FormData($( "#form_edit_my_registry" )[0]);
	            	   $.ajax({
	            	        url: "update/my-registry",
	            	        type: 'POST',
	            	        data: formData,
	            	        cache: false,
	            	        contentType: false,
	            	        processData: false,
	            	        async:true,
	            	   		success: function(data){
                                window.location = 'oai-pmh-my-infos'
	            	        },
	            	        error:function(data){
	            	        	$("#form_edit_errors").html(data.responseText);
                                $("#banner_edit_my_errors").show(200)
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


load_edit_my_registry_form = function(registryId){
	$.ajax({
        url : "update/my-registry",
        type : "GET",
        dataType: "json",
        data : {
        },
        success: function(data){
            $("#form_edit_errors").html("");
            $("#form_edit_current").html(data.template);
            Reinit();
        }
    });
}

validateEditMyRegistry = function()
{
    errors = ""

    if ($( "#id_name" ).val().trim() == ""){
        errors += "<li>Please enter a name.</li>"
    }

	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_edit_errors").html(errors);
		$("#banner_edit_my_errors").show(200)
		return (false);
	}else{
		return (true)
	}
    return true;
}


/**
 * AJAX call, harvest all data
 */
harvestAllData = function ()
{
    var registriesCheck = $("span[id^=harvest]:visible")

    $.each(registriesCheck, function(index, props) {
         harvestData($(props).attr('registryID'));
    });
}


/**
 * AJAX call, harvest data for a Registry
 * @param registry_id id of the registry
 */
harvestData = function(registry_id){
    $("#banner"+registry_id).show(200);
    $("#harvest"+registry_id).hide(200);
    $.ajax({
        url : 'harvest',
        type : "POST",
        dataType: "json",
        async: true,
        data : {
        	registry_id : registry_id,
        },
        success: function(data){
            checkHarvestData();
        },
        error:function(data){
	    }
    });
}

/**
 * AJAX call, check harvest data for all Registries
 */
checkHarvestData = function()
{
    $.ajax({
        url : 'check/harvest-data',
        type : "POST",
        dataType: "json",
        async: true,
        data : {
        },
        success: function(data){
            $.map(data, function (item) {
                if(item.isHarvesting)
                {
                    $("#harvest" + item.registry_id).hide(200);
                    $("#banner"+ item.registry_id).show(200);
                }
                else
                {
                    $("#banner"+ item.registry_id).hide(200);
                    $("#harvest" + item.registry_id).show(200);
                    if(item.lastUpdate != '')
                        $("#lastUpdate"+ item.registry_id).html(item.lastUpdate);
                }
             });
        },
        error:function(data){
	    }
    });
//    Refresh every 30 seconds
    setTimeout(checkHarvestData, 30000);
}





Init = function(){
    var buttonsetElts = $("td[id^=ButtonSet]")
    $.each(buttonsetElts, function(index, props) {
         $("#"+props.id).buttonset();
    });
    checkHarvestData();
}

Reinit = function(){
    var buttonsetElts = $("#form_edit_current td[id^=ButtonSet]")
    $.each(buttonsetElts, function(index, props) {
         $("#"+props.id).buttonset();
    });
    enterKeyPressSubscription();
}


init = function(){
    populateSelect();
    $("select").on('change', function() {
      $("#build_errors").html("");
      $("#banner_build_errors").hide(200);
    });
    $("input").on('change', function() {
      $("#build_errors").html("");
      $("#banner_build_errors").hide(200);
    });

    $("select#id_dataProvider").on('change', function() {
      populateSelect();
    });

    $('#id_until').datetimepicker({
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		forceParse: 0,
        showMeridian: 1
    });
    $('#id_From').datetimepicker({
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		forceParse: 0,
        showMeridian: 1
    });
}


clearAddMF = function ()
{
    clearAddMFError();
    $( "#form_add_MF" )[0].reset();
}

clearAddMFError = function ()
{
    $("#banner_add_MF_errors").hide()
    $("#form_add_MF_errors").html("");
}

validateMetadataFormat = function()
{
    errors = ""

    if ($( "#id_metadataPrefix" ).val().trim() == ""){
        errors += "<li>Please enter a Metadata Prefix.</li>"
    }

    if ($( "#id_schema" ).val().trim() == ""){
        errors += "<li>Please enter a schema.</li>"
    }

//    if ($( "#id_metadataNamespace" ).val().trim() == ""){
//        errors += "<li>Please enter a namespace.</li>"
//    }
//
//        if ($( "#id_xmlSchema" ).val().trim() == ""){
//        errors += "<li>Please provide an XML file.</li>"
//    }

	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_add_MF_errors").html(errors);
		$("#banner_add_MF_errors").show(200)
		return (false);
	}else{
		return (true)
	}
    return true;
}

displayAddMetadataFormat = function()
{
 $(function() {
    clearAddMF();
//    $('#duration').durationPicker();

    $( "#dialog-add-metadataformat" ).dialog({
      modal: true,
      width: 550,
      height: 'auto',
      buttons:
      [
      {
           text: "Cancel",
           click: function() {
                    $( this ).dialog( "close" );
                }
       },
       {
           text: "Add",
           click: function() {
                clearAddMFError();
                if(validateMetadataFormat())
                {
//                       $("#banner_add_wait").show(200);
                   var formData = new FormData($( "#form_add_MF" )[0]);
                   $.ajax({
                        url: "add/my-metadataFormat",
                        type: 'POST',
                        data: formData,
                        cache: false,
                        contentType: false,
                        processData: false,
                        async:true,
                        success: function(data){
                            window.location = 'oai-pmh-my-infos'
                        },
                        error:function(data){
//	            	            $("#banner_add_wait").hide(200);
                            $("#form_add_MF_errors").html(data.responseText);
                            $("#banner_add_MF_errors").show(200)
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

deleteMetadataFormat = function(metadataformat_id)
{
 $(function() {
    $( "#dialog-mf-confirm-delete" ).dialog({
      modal: true,
      buttons:{
            	Delete: function() {
            		delete_metadata_format(metadataformat_id);
            		},
				Cancel: function() {
	                $( this ).dialog( "close" );
		          },
		    }
    });
  });
}

/**
 * AJAX call, deletes one of my Metadata format
 * @param registry_id id of the registry
 */
delete_metadata_format = function(metadataformat_id){
    $("#banner_mf_delete_wait").show(200);
    $.ajax({
        url : 'delete/my-metadataFormat',
        type : "POST",
        dataType: "json",
        data : {
        	MetadataFormatId : metadataformat_id,
        },
        success: function(data){
            window.location = 'oai-pmh-my-infos'
        },
        error:function(data){
            $("#banner_mf_delete_wait").hide(200);
            $("#form_mf_delete_errors").html(data.responseText);
            $("#banner_mf_delete_errors").show(200);
	    }
    });
}


clearMFEditError = function ()
{
    $("#banner_edit_mf_errors").hide()
    $("#form_edit_mf_errors").html("");
}

validateMetadataFormatEdit = function()
{
    errors = ""

    if ($( "#form_edit_mf_current #id_metadataPrefix" ).val().trim() == ""){
        errors += "<li>Please enter a Metadata Prefix.</li>"
    }

    if ($( "#form_edit_mf_current #id_schema" ).val().trim() == ""){
        errors += "<li>Please enter a schema.</li>"
    }

    if ($( "#form_edit_mf_current #id_metadataNamespace" ).val().trim() == ""){
        errors += "<li>Please enter a namespace.</li>"
    }


	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_edit_mf_errors").html(errors);
		$("#banner_edit_mf_errors").show(200)
		return (false);
	}else{
		return (true)
	}
    return true;
}


/**
 * Show a dialog when a result is selected
 */
editMetadataFormat = function(metadataFormatId)
{
    clearMFEditError()
    exist = load_mf_edit_form(metadataFormatId);
    $(function() {
        $( "#dialog-mf-edit" ).dialog({
          modal: true,
          width: 400,
          height: 'auto',
          buttons:
              [
               {
                   text: "Cancel",
                   click: function() {
                            $( this ).dialog( "close" );
                        }
               },
               {
                   text: "Edit",
                   click: function() {
                        clearMFEditError();
                        if(validateMetadataFormatEdit())
                        {
                            var formData = new FormData($( "#form_edit_mf" )[0]);
                            $.ajax({
                                url: "update/my-metadataFormat",
                                type: 'POST',
                                data: formData,
                                cache: false,
                                contentType: false,
                                processData: false,
                                async:false,
                                success: function(data){
                                    window.location = 'oai-pmh-my-infos'
                                },
                                error:function(data){
                                    $("#form_edit_mf_errors").html(data.responseText);
                                    $("#banner_edit_mf_errors").show(200)
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


load_mf_edit_form = function(metadataFormatId){
	$.ajax({
        url : "update/my-metadataFormat",
        type : "GET",
        dataType: "json",
        data : {
            metadata_format_id : metadataFormatId,
        },
        success: function(data){
            $("#form_edit_mf_errors").html("");
            $("#form_edit_mf_current").html(data.template);
        }
    });
}