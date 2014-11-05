loadTemplateSelectionControllers = function()
{
    console.log('BEGIN [loadTemplateSelectionControllers]');
    $('.btn.set-compose-template').on('click', setComposeCurrentTemplate);
    $('.btn.set-compose-user-template').on('click', setComposeCurrentUserTemplate);
    console.log('END [loadTemplateSelectionControllers]');
}


setComposeCurrentTemplate = function()
{
    var templateName = $(this).parent().parent().children(':first').text();
    var templateFilename = $(this).parent().parent().children(':nth-child(2)').text();
    var tdElement = $(this).parent();
    var templateID = $(this).parent().parent().children(':first').attr('templateid');
		
    tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
    $('.btn.set-template').off('click');
    
    console.log('[setCurrentComposeTemplate] Setting '+templateName+' with filename '+templateFilename+' as current template...');

    Dajaxice.compose.setCurrentTemplate(setCurrentTemplateCallback,{'templateFilename':templateFilename,'templateID':templateID});

    return false;
}

setComposeCurrentUserTemplate = function()
{
    var templateName = $(this).parent().parent().children(':first').text();
    var tdElement = $(this).parent();
    var templateID = $(this).parent().parent().children(':first').attr('templateid');
		
    tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
    $('.btn.set-template').off('click');

    Dajaxice.compose.setCurrentUserTemplate(setCurrentTemplateCallback,{'templateID':templateID});

    return false;
}

setCurrentTemplateCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [setCurrentTemplateCallback]');
    console.log('data passed back to callback function: ' + data);

    $('#template_selection').load(document.URL +  ' #template_selection', function() {
		loadTemplateSelectionControllers();
		displayTemplateSelectedDialog();
    });
    console.log('END [setCurrentTemplateCallback]');
}

displayTemplateSelectedDialog = function()
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

loadComposeBuildTemplate = function(){
	console.log('BEGIN [loadComposeBuildTemplate]');
		
	$('.btn.download').on('click', downloadTemplate);
	$('.btn.save').on('click', saveTemplate);
	$(document).on('click', function(event) {
	  if (!$(event.target).closest('#XMLHolder').length) {
	    $("#menu").remove();
	  }
	});
	
	Dajaxice.compose.loadXML(Dajax.process);
	console.log('END [loadComposeBuildTemplate]');
}

downloadTemplate = function(){
	console.log('BEGIN [downloadTemplate]');
	
	Dajaxice.compose.downloadTemplate(Dajax.process);
	
	console.log('END [downloadTemplate]');
}

saveTemplate = function(){
	console.log('BEGIN [saveTemplate]');
	
	$("#new-template-error").html("");
	
	$(function() {
		$("#dialog-save-template").dialog({
		  modal: true,
		  width: 400,
		  height: 250,
		  buttons: {
			Save: function() {
					templateName = $("#newTemplateName").val();
					if (templateName.length > 0){						
						Dajaxice.compose.saveTemplate(saveTemplateCallback, {"templateName":templateName});						
						$( this ).dialog( "close" );
					}else{
						$( "#new-template-error" ).html("The name can't be empty.")
					}					 
			   	},			      
		    Cancel: function() {
		    		$( this ).dialog( "close" );
		        }
		      }
		    });
	  });
	
	console.log('END [saveTemplate]');
}


saveTemplateCallback = function(){
	console.log('BEGIN [saveTemplateCallback]');
	
	$(function() {
        $( "#dialog-saved-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
	
	console.log('END [saveTemplateCallback]');
}

showhide = function(event){
	console.log('BEGIN [showhide]');
	button = event.target
	parent = $(event.target).parent()
	$(parent.children()[3]).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse");
	}else{
		$(button).attr("class","expand");
	}
		
	console.log('END [showhide]');
}

var target;

var showMenuSequence=function(event){
	$("#menu").remove();
	
	target = event.target;
	$("<ul id='menu' style='position:absolute;z-index:9999;'>" + 
      "<li><span onclick='displayInsertElementSequenceDialog()'>Add Element</span></li>" +
      "<li><span onclick='displayChangeTypeDialog()'>Change Type</span></li>" +
      "</ul>")
		.menu()
		.appendTo("body")
		.position({
	        my: "left top",
	        at: "left bottom",
	        of: event.target
	      }).show();
};		

var showMenuElement=function(event){
	$("#menu").remove();
	
	target = event.target;
	$("<ul id='menu' style='position:absolute;z-index:9999;'>" + 
      "<li><span onclick='displayRenameElementDialog()'>Rename</span></li>" +
      "</ul>")
		.menu()
		.appendTo("body")
		.position({
	        my: "left top",
	        at: "left bottom",
	        of: event.target
	      }).show();
};	

displayInsertElementSequenceDialog = function()
{
 $(function() {
	$("#table_types").find(".btn.insert").each(function(){
		$(this).attr('onclick','insertElementSequence(event)');
	});
    $( "#dialog-insert-element-sequence" ).dialog({
      modal: true,
      width: 600,
      height: 400,
      buttons: {
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });
}

displayRenameElementDialog = function()
{
	$( "#rename-element-error" ).html("");
	$("#newElementName").val($(target).parent().siblings('.name').html());
	$(function() {
		$( "#dialog-rename-element" ).dialog({
		  modal: true,
		  width: 400,
		  height: 250,
		  buttons: {
			Rename: function() {
					newName = $("#newElementName").val();
					if (newName.length > 0){
						xpath = getXPath();
						Dajaxice.compose.renameElement(Dajax.process, {"xpath":xpath, "newName":newName});
						$(target).parent().siblings('.name').html(newName);
						$( this ).dialog( "close" );
					}else{
						$( "#rename-element-error" ).html("The name can't be empty.")
					}					 
			   	},			      
		    Cancel: function() {
		    		$( this ).dialog( "close" );
		        }
		      }
		    });
	  });
}

insertElementSequence = function(event){	
	// change the sequence style
	parent = $(target).parent()
	if ($(parent).attr('class') == "element"){
		$(parent).before("<span class='collapse' style='cursor:pointer;' onclick='showhide(event);'></span>");
		$(parent).after("<ul></ul>");
		$(parent).attr('class','category');
	}
	
	insertButton = event.target;
	typeName = $(insertButton).parent().siblings(':first').text();
	typeID = $(insertButton).parent().siblings(':first').attr('templateid');
	namespace = $(target).text().split(":")[0];
	
	nbElement = $(parent).parent().find("ul").children().length;
	
	console.log(nbElement)
	if (nbElement == 0){
		path = namespace + ":element";
//	}else if (nbElement == 1){
//		path = namespace + ":element[2]";
//		$($(parent).parent().find("ul").children()[0]).find(".element-wrapper").find(".path").text(namespace + ":element[0]");
	}else{
		path = namespace + ":element[" + String(nbElement + 1) + "]";
	}	
	
	xpath = getXPath();
	
	// add the new element
	$(parent).parent().find("ul").append("<li>" +
											"<div class='element-wrapper'>" +
												"<span class=path>"+
												 path +
												"</span>" +
												"<span class='newElement'>" +
													"<span onclick='showMenuElement(event)' style='cursor:pointer;'>" +
													namespace + ":element : "+ 
													"</span>" +													
												"</span>" +
												"<span class='name'>"+ typeName +"</span>" +
												"<span class='type'>"+ typeName +"</span>" +
											"</div>"+
										"</li>")
	
	$( "#dialog-insert-element-sequence" ).dialog("close");
	
	Dajaxice.compose.insertElementSequence(Dajax.process, {"typeID": typeID, "xpath":xpath, "typeName": typeName});
}

getXPath = function(){
	current = $(target).parent().siblings('.path');
	xpath = $(current).text();	
	current = $(current).parent().parent().parent().siblings('.path');
	while(current != null){
		current_path = $(current).text() ;
		if (current_path.contains("schema")){
			current = null;
		}else{			
			xpath = current_path + "/" + xpath;	
			current = $(current).parent().parent().parent().siblings('.path');
		}		
	}
	
	return xpath;
}
