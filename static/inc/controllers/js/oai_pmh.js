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
      height: 370,
      buttons:
    	  [
           {
               text: "Add",
               click: function() {
                    clearAddError();
                    if(validateRegistry())
                    {
                       $("#banner_add_wait").show(200);
                       var formData = new FormData($( "#form_add" )[0]);
	            	   $.ajax({
	            	        url: "/oai_pmh/client/add/registry",
	            	        type: 'POST',
	            	        data: formData,
	            	        cache: false,
	            	        contentType: false,
	            	        processData: false,
	            	        async:true,
	            	   		success: function(data){
                                window.location = '/admin/oai-pmh'
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

    if ($( "#form_edit_current #id_harvestrate" ).val().trim() == ""){
        errors += "<li>Please enter an  harvest rate.</li>"
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
          height: 370,
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
                                url: "/oai_pmh/client/update/registry",
                                type: 'POST',
                                data: formData,
                                cache: false,
                                contentType: false,
                                processData: false,
                                async:false,
                                success: function(data){
                                    window.location = '/admin/oai-pmh'
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
        url : "/oai_pmh/client/update/registry",
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
        url : '/oai_pmh/client/delete/registry',
        type : "POST",
        dataType: "json",
        data : {
        	RegistryId : registry_id,
        },
        success: function(data){
            window.location = '/admin/oai-pmh'
        },
        error:function(data){
            $("#banner_delete_wait").hide(200);
            $("#form_delete_errors").html(data.responseText);
            $("#banner_delete_errors").show(200);
	    }
    });
}


Init = function(){
    var buttonsetElts = $("td[id^=ButtonSet]")
    $.each(buttonsetElts, function(index, props) {
         $("#"+props.id).buttonset();
    });
//    enterKeyPressSubscription();
}

Reinit = function(){
    var buttonsetElts = $("#form_edit_current td[id^=ButtonSet]")
    $.each(buttonsetElts, function(index, props) {
         $("#"+props.id).buttonset();
    });
//    enterKeyPressSubscription();
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
        url : '/oai_pmh/client/check/registry',
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
	$.ajax({
        url : "/admin/oai-pmh-detail-registry?id=" + id,
        type : "GET",
        success: function(data){
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