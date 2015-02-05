/**
 * 
 * File Name: composer.js
 * Author: Sharief Youssef
 * 		   sharief.youssef@nist.gov
 *
 *        Guillaume SOUSA AMARAL
 *        guillaume.sousa@nist.gov
 * 
 * Sponsor: National Institute of Standards and Technology (NIST)
 * 
 */

/**
 * Load controllers of the template selection page.
 */
loadTemplateSelectionControllers = function()
{
    console.log('BEGIN [loadTemplateSelectionControllers]');    
    $('.btn.set-compose-template').on('click', setComposeCurrentTemplate);
    $('.btn.set-compose-user-template').on('click', setComposeCurrentUserTemplate);
    console.log('END [loadTemplateSelectionControllers]');
}

/**
 * Check that a template is selected.
 */
verifyTemplateIsSelectedBuild = function(){
    console.log('BEGIN [verifyTemplateIsSelected]');

    Dajaxice.compose.verifyTemplateIsSelected(verifyTemplateIsSelectedBuildCallback); 

    console.log('END [verifyTemplateIsSelected]');
}

/**
 * The template is not selected, redirect to main page.
 * @param data 'yes' or 'no'
 */
verifyTemplateIsSelectedBuildCallback = function(data)
{
    console.log('BEGIN [verifyTemplateIsSelectedCallback]');

    if (data.templateSelected == 'no') {
        location.href = "/compose";
    }else{
    	loadComposeBuildTemplate();
    	verifyNewTemplate();
    }

    console.log('END [verifyTemplateIsSelectedCallback]');
}

/**
 * Check if the selected template is a new template
 */
verifyNewTemplate = function(){
	Dajaxice.compose.isNewTemplate(newTemplateCallback);
}

/**
 * If new template, need to give it a name
 * @param data 'yes' or 'no'
 */
newTemplateCallback = function(data){
	if (data.newTemplate == 'yes'){
		$("#newTemplateTypeNameError").html("");
		$(function() {
		    $( "#dialog-new-template" ).dialog({
		      modal: true,
		      width:400,
		      height:270,
		      buttons: {
		        Start: function() {
		          if ($("#newTemplateTypeName").val() == ""){
		        	  $("#newTemplateTypeNameError").html("The name can't be empty.");
		          }else{
		        	  $("#XMLHolder").find(".type").html($("#newTemplateTypeName").val());
		        	  Dajaxice.compose.changeRootTypeName(Dajax.process, {"typeName":$("#newTemplateTypeName").val()});
		        	  $( this ).dialog( "close" );
		          }
		        }
		      }
		    });
		  });
	} 
}

/**
 * Set a template to be current
 */
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

/**
 * Set a user template to be current
 */
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

/**
 * 
 * @param data
 */
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
	$('.btn.save.template').on('click', saveTemplate);
	$('.btn.save.types').on('click', saveType);
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


saveType = function(){
	console.log('BEGIN [saveType]');
	
	$("#new-type-error").html("");
	
	$(function() {
		$("#dialog-save-type").dialog({
		  modal: true,
		  width: 400,
		  height: 250,
		  buttons: {
			Save: function() {
					typeName = $("#newTypeName").val();
					if (typeName.length > 0){	
						Dajaxice.compose.saveType(saveTemplateCallback, {"typeName":typeName});						
						$( this ).dialog( "close" );
					}else{
						$( "#new-type-error" ).html("The name can't be empty.")
					}
			   	},			      
		    Cancel: function() {
		    		$( this ).dialog( "close" );
		        }
		      }
		    });
	  });
	
	console.log('END [saveType]');
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
	parentPath = $(target).parent().parent().parent().parent().siblings('.path').text();
	
	// if root element
	if(parentPath.indexOf('schema') > -1){
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
	}else{ // not root element
		$("<ul id='menu' style='position:absolute;z-index:9999;'>" + 
	      "<li><span onclick='displayRenameElementDialog()'>Rename</span></li>" +
	      "<li><span onclick='displayOccurrencesElementDialog()'>Manage Occurrences</span></li>" +
	      "<li><span onclick='displayDeleteElementDialog()'>Delete</span></li>" +
	      "</ul>")
			.menu()
			.appendTo("body")
			.position({
		        my: "left top",
		        at: "left bottom",
		        of: event.target
		      }).show();
	}	
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
      open: function(){
    	  $('#table_types').accordion({
    			collapsible: true,
		  });
      },
      buttons: {
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });
}

displayChangeTypeDialog = function()
{
	 $(function() {
	    $( "#dialog-change-xsd-type" ).dialog({
	      modal: true,
	      width: 275,
	      height: 185,
	      buttons: {
	    	Change: function() {
	    		  newType = $("#newXSDtype").val();
	    		  xpath = getXPath();
	    		  oldType = $(target).text().split(":")[1];
	    		  $(target).html($(target).html().replace(oldType,newType));
	    		  $(target).parent().siblings(".path").html($(target).parent().siblings(".path").html().replace(oldType,newType));
	    		  Dajaxice.compose.changeXSDType(Dajax.process,{"xpath":xpath, "newType": newType});
		          $( this ).dialog( "close" );
		    },
	        Cancel: function() {
	          $( this ).dialog( "close" );
	        }
	      }
	    });
	  });
	}

function isInt(value) {
  return !isNaN(value) && parseInt(Number(value)) == value && !isNaN(parseInt(value, 10));
}


displayOccurrencesElementDialog = function()
{
	 $( "#manage-occurrences-error" ).html("");
	 $(function() {
		xpath = getXPath();
		Dajaxice.compose.getOccurrences(getOccurrencesCallback,{"xpath":xpath})
	    $( "#dialog-occurrences-element" ).dialog({
	      modal: true,
	      width: 600,
	      height: 350,
	      buttons: {
			Save: function() {
				minOccurs = $("#minOccurrences").val();
				maxOccurs = $("#maxOccurrences").val();

				errors = ""

				if (! isInt(minOccurs)){
					errors += "minOccurs should be an integer.<br/>";
				}else {
					if (minOccurs < 0){
						errors += "minOccurs should be superior or equal to 0.<br/>";
					}
					if (! isInt(maxOccurs)){
						if (maxOccurs != "unbounded"){
							errors += "maxOccurs should be an integer or 'unbounded'.<br/>";
						}
					}else {
						if (maxOccurs < 1){
							errors += "maxOccurs should be superior or equal to 1.<br/>";
						}else if (maxOccurs < minOccurs){
							errors += "maxOccurs should be superior or equal to minOccurs.<br/>";
						}
					}
				}
				
				if (errors == ""){
					Dajaxice.compose.setOccurrences(Dajax.process,{"xpath":xpath, "minOccurs":minOccurs,"maxOccurs":maxOccurs});
					occursStr = "( " + minOccurs + " , ";
					if (maxOccurs == "unbounded"){
						occursStr += "*";
					}else{
						occursStr += maxOccurs;
					}
					occursStr += " )";
					$(target).parent().siblings(".occurs").html(occursStr)
					$( this ).dialog( "close" );
				}else{
					$( "#manage-occurrences-error" ).html(errors);
				}
			},
			Cancel: function() {
			  $( this ).dialog( "close" );
			}
	      }
	    });
	  });
}


getOccurrencesCallback = function(data){
	$("#minOccurrences").val(data[0].val['minOccurs']);
	$("#maxOccurrences").val(data[0].val['maxOccurs']);
}

displayDeleteElementDialog = function()
{
	 $(function() {
		xpath = getXPath();
	    $( "#dialog-delete-element" ).dialog({
	      modal: true,
	      width: 400,
	      height: 170,
	      buttons: {
			Delete: function() {
				manageXPath();
				$(target).parent().parent().parent().remove();				
				Dajaxice.compose.deleteElement(Dajax.process,{"xpath":xpath});
				$( this ).dialog( "close" );
			},
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
												"<span class='occurs'>( 1 , 1)</span>" +
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


manageXPath = function(){	
	namespace = $(target).text().split(":")[0];
	i = 1;
	$(target).closest("ul").children().each(function(){
	  if(!($(this).find(".path").html() == $(target).closest("li").find(".path").html() )){
		  $(this).find(".path").html(namespace + ":element["+i+"]");
		  i += 1;
	  }	  
	})
}