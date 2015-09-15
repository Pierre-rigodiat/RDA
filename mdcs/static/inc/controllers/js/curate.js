/**
 * 
 * File Name: curate.js
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
 * AJAX call, checks that a template is selected
 * @param selectedLink redirection link
 */
verifyTemplateIsSelected = function(selectedLink)
{
    console.log('BEGIN [verifyTemplateIsSelected]');
    
    $.ajax({
        url : "/curate/verify_template_is_selected",
        type : "GET",
        dataType: "json",
        success: function(data){
            verifyTemplateIsSelectedCallback(data, selectedLink);
        }
    });

    console.log('END [verifyTemplateIsSelected]');
}


/**
 * AJAX callback, redirects to selected link if authorized
 * @param data data from server
 * @param selectedLink redirection link
 */
verifyTemplateIsSelectedCallback = function(data, selectedLink)
{
    console.log('BEGIN [verifyTemplateIsSelectedCallback]');

    if (data.templateSelected == 'no') {
        $(function() {
            $( "#dialog-error-message" ).dialog({
                modal: true,
                buttons: {
                    Ok: function() {
                    $( this ).dialog( "close" );
                    }
                }
            });
        });
    } else {
        location.href = selectedLink;
    }

    console.log('END [verifyTemplateIsSelectedCallback]');
}


/**
 * Display message to block access to enter data from first step.
 */
enterDataError = function()
{
    $(function() {
        $( "#dialog-enter-error-message" ).dialog({
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
 * Display message to block access to view data from first step.
 */
viewDataError = function()
{
    $(function() {
        $( "#dialog-view-error-message" ).dialog({
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
 * Load controllers for template selection
 */
loadTemplateSelectionControllers = function()
{
    console.log('BEGIN [loadTemplateSelectionControllers]');
    $('.btn.set-template').on('click', setCurrentTemplate);
    $('.btn.set-curate-user-template').on('click', setCurrentUserTemplate);
    init_curate();
    console.log('END [loadTemplateSelectionControllers]');    
}


/**
 * AJAX call, initializes curation
 */
init_curate = function(){
    $.ajax({
        url : "/curate/init_curate",
        type : "GET",
        dataType: "json",
    });
}


/**
 * Clear the fields of the current curated data
 */
clearFields = function()
{
    console.log('BEGIN [clearFields]');

    $(function() {
        $( "#dialog-cleared-message" ).dialog({
            modal: true,
            buttons: {
            	Clear: function() {
            		clear_fields();
                    $( this ).dialog( "close" );
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [clearFields]');
}


/**
 * AJAX call, clears fields 
 */
clear_fields = function(){
    $.ajax({
        url : "/curate/clear_fields",
        type : "GET",
        dataType: "json",
        success: function(data){
            $("#xsdForm").html(data.xsdForm);
        }
    });
}


/**
 * Save the current form. Show the window.
 */
saveForm = function()
{
    console.log('BEGIN [saveForm]');

    $(function() {
        $( "#dialog-save-form-message" ).dialog({
            modal: true,
            buttons: {
				Save: function() {				 
					$( this ).dialog( "close" );
					var rootElement = document.getElementsByName("xsdForm")[0];
					var xmlString = '';						
				    xmlString = generateXMLString (rootElement);
					save_form(xmlString);
                },
			Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
	
    console.log('END [saveForm]');
}


/**
 * AJAX call, saves the current form 
 * @param xmlString xml string to save
 */
save_form = function(xmlString){
    $.ajax({
        url : "/curate/save_form",
        type : "POST",
        dataType: "json",
        data : {
        	xmlString : xmlString,
        },
        success: function(data){
        	$( "#dialog-saved-message" ).dialog({
            modal: true,
            buttons: {
    		Ok: function() {
                        $( this ).dialog( "close" );
                    }
    	    	}
            });
        }
    });
}


/**
 * Displays the current data to be curated
 */
viewData = function()
{
    console.log('BEGIN [viewData]');

    var rootElement = document.getElementsByName("xsdForm")[0];

    // Need to Set input values explicitiy before sending innerHTML for save
    var elems = document.getElementsByName("xsdForm")[0].getElementsByTagName("input");
    for(var i = 0; i < elems.length; i++) {
	// sent attribute to property value
	elems[i].setAttribute("value", elems[i].value);
    }

    formContent = document.getElementById('xsdForm').innerHTML
    view_data(formContent);

    console.log('END [viewData]');
}


/**
 * AJAX call, redirects to View Data after sending the current form
 * @param formContent
 */
view_data = function(formContent){
    $.ajax({
        url : "/curate/view_data",
        type : "POST",
        dataType: "json",
        data : {
            form_content : formContent,
        },
        success: function(data){
            window.location = "/curate/view-data"
        }
    });
}


/**
 * Validate the current data to curate.
 */
validateXML = function()
{
	var rootElement = document.getElementsByName("xsdForm")[0];
	var xmlString = '';
	
    xmlString = generateXMLString (rootElement);
    
    $("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });

    xsdForm = $('#xsdForm').html();
    validate_xml_data(xmlString, xsdForm);
}


/**
 * AJAX call, send the XML String to the server for validation
 * @param xmlString XML String generated from the HTML form
 * @param xsdForm HTML form
 */
validate_xml_data = function(xmlString, xsdForm){
    $.ajax({
        url : "/curate/validate_xml_data",
        type : "POST",
        dataType: "json",
        data : {
            xmlString : xmlString,
            xsdForm: xsdForm
        },
        success: function(data){
            if ('errors' in data){
                 $("#saveErrorMessage").html(data.errors);
                saveXMLDataToDBError();
            }else{
                viewData();
            }
        }
    });
}


/**
 * Generate an XML String from values entered in the form.
 * @param elementObj
 * @returns {String}
 */
generateXMLString = function(elementObj)
{
    var xmlString="";

    var children = $(elementObj).children();
    for(var i = 0; i < children.length; i++) {
	    if (children[i].tagName == "UL") {
	    	// don't generate branches not chosen
	    	if (! $(children[i]).hasClass("notchosen") ) {
	    		xmlString += generateXMLString(children[i]);
	    	}
		} else if (children[i].tagName == "LI") {
			// don't generate removed branches/leaves
			if (! $(children[i]).hasClass("removed") ) {
				if($(children[i]).hasClass("choice") ) { // the node is a choice
					xmlString += generateXMLString(children[i]);
				}else if ($(children[i]).hasClass("sequence") ) { // the node is a sequence
					xmlString += generateXMLString(children[i]);
				}else if ($(children[i]).hasClass("element") ){ // the node is an element
					var textNode = $(children[i]).contents().filter(function(){
				        return this.nodeType === 3;
				    }).text().trim();
					
					// get attributes
					var attributes = ""
					$(children[i]).children("ul").children("li.attribute:not(.removed)").each(function(){
						var text = $(this).contents().filter(function(){
					        return this.nodeType === 3;
					    }).text().trim();
					
						attrChildren = $(this).children();					
 
						var value= ""
						for(var j = 0; j < attrChildren.length; j++) {
							if (attrChildren[j].tagName == "SELECT") {
							    // get the index of the selected option 
							    var idx = attrChildren[j].selectedIndex;
							    if (idx >= 0){
								    // get the value of the selected option 		    
								    value = attrChildren[j].options[idx].value; 
							    }
							} else if (attrChildren[j].tagName == "INPUT") {
								console.log(attrChildren[j]);
								value = attrChildren[j].value;
							}
						}						
						attributes += " " + text + "='" + value + "'";
					});
					// build opening tag with potential attributes
					xmlString += "<" + textNode + attributes + ">";
					// build the content of the element
				    xmlString += generateXMLString(children[i]);
				    // build the closing tag
				    xmlString += "</" + textNode + ">";
				}			    	
			}
		} else if (children[i].tagName == "DIV" && $(children[i]).hasClass("module") ){
			xmlString += $($(children[i]).parent()).find(".moduleResult").text();		
		} else if (children[i].tagName == "SELECT") {
		    // get the index of the selected option 
		    var idx = children[i].selectedIndex; 
		    
		    if (idx >= 0){
			    // get the value of the selected option 		    
			    var which = children[i].options[idx].value;
			    
			    if (children[i].getAttribute("id") != null && children[i].getAttribute("id").indexOf("choice") > -1){
				    // choice
			    	xmlString += generateXMLString(children[i]);
			    }else { 
			    	// enumeration
			    	xmlString += which;
			    }
		    }
		} else if (children[i].tagName == "INPUT") { // the node is an input
		    xmlString += children[i].value;
		}  else {
		    xmlString += generateXMLString(children[i]);
		}
    }

    return xmlString    
}


/**
 * Display the periodic table to select a chemical element
 * @param divElement
 */
selectElement = function(divElement)
{   
	console.log('BEGIN [selectElement('+divElement+')]');
    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>None</b>";

    $(function() {
	$("#dialog-select-element" ).dialog({ width: 700 });
        $("#dialog-select-element" ).dialog({
            modal: true,
            buttons: {
		Select: function() {
		    		doSelectElement(divElement);
                    $( this ).dialog( "close" );
                },
		Cancel: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	console.log('END [selectElement('+divElement+')]');
}


/**
 * Display the selected element
 * @param element
 */
chooseElement = function(element)
{
    console.log('BEGIN [chooseElement(' + element + ')]');

    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b id=\"selectedElement\">" + element + "</b>";

    console.log('END [chooseElement(' + element + ')]');
}


/**
 * Save the selected element into the form
 * @param divElement
 */
doSelectElement = function(divElement)
{
    console.log('BEGIN [doSelectElement(' + divElement + ')]');

    var selectedElement = document.getElementById('selectedElement').innerHTML;
    console.log('[selected Element(' + selectedElement + ')]');
    divElement.onclick = function onclick(event) { selectElement(this); }	
	$($(divElement).parent()).children(".moduleDisplay").html("Current Selection: "+selectedElement);
	//$($(divElement).parent()).children(".moduleResult").html("<element>" + selectedElement + "</element>");
	$($(divElement).parent()).children(".moduleResult").html(selectedElement);
	
    // reset for next selection
    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>None</b>";

    console.log('END [doSelectElement(' + divElement + ')]');
}


/**
 * Display the periodic table to select multiple chemical elements
 * @param divElement
 */
selectMultipleElements = function(divElement)
{
  console.log('BEGIN [selectElement(' + divElement + ')]');
  
  
  if ($($(divElement).parent()).children(".moduleDisplay").html() != ""){	  
	  var newTable = "<table>";
	  newTable += "<tr><th>Element</th><th>Quantity</th><th>Purity</th><th>Error</th><th>Actions</th></tr>";
	  console.log($($(divElement).parent()).children(".moduleDisplay").children("table").children("tbody").children())
	  $($(divElement).parent()).children(".moduleDisplay").children("table").children("tbody").children().each(function(i,tr){
			// not the headers
			if (i != 0){  
				console.log(i,tr)				
				newTable += "<tr>";
				newTable += "<td style='text-align:center'>"  + $($(tr).children()[0]).html() + "</td>";
				newTable += "<td><input type='text' value='"  + $($(tr).children()[1]).html() + "'/></td>"; 
				newTable += "<td><input type='text' value='"  + $($(tr).children()[2]).html() + "'/></td>";
				newTable += "<td><input type='text' value='"  + $($(tr).children()[3]).html() + "'/></td>";
				newTable += "<td><span class='btn' onclick='removeMultipleElement(this)'>Remove</span></td>"
				newTable += "</tr>";
			}
	  });
	  
	  newTable += "</table>"  
	  $("#tableChosenElements").html(newTable);
  }
  
  $(function() {
      $("#dialog-select-element-multiple" ).dialog({
          modal: true,
          width: 700,
          height: 550,
          buttons: {
        	  Save: function() {
		    		doSelectMultipleElements(divElement);
                  $( this ).dialog( "close" );
              },
              Cancel: function() {
                  $( this ).dialog( "close" );
              }
	    }
      });
  });
	
  console.log('END [selectElement]');
}


/**
 * Display the selected elements
 * @param element
 */
chooseMultipleElements = function(element)
{
  console.log('BEGIN [chooseElement(' + element + ')]');
  
  // if 2 rows: headers + 1 row
  if ($("#tableChosenElements").children("tbody").children().length == 2){
  	// if the second row contains 1 cel: no selected elements
  	if ($($("#tableChosenElements").children("tbody").children()[1]).children().length == 1){
  		$("#tableChosenElements").children("tbody").children()[1].remove();
  	}
  }
  $("#tableChosenElements").children("tbody").append("<tr><td>"+ element +"</td><td><input type='text'/></td><td><input type='text'/></td><td><input type='text'/></td><td><span class='btn' onclick='removeMultipleElement(this)'>Remove</span></td></tr>");
  

  console.log('END [chooseElement(' + element + ')]');
}


/**
 * Save the selected elements into the form
 * @param divElement
 */
doSelectMultipleElements = function(divElement)
{
console.log('BEGIN [selectElement(' + divElement + ')]');


var xmlResult = "";
var displayedResults = "";
//if the second row contains 1 cel: no selected elements
if (!($("#tableChosenElements").children("tbody").children().length == 2 && $($("#tableChosenElements").children("tbody").children()[1]).children().length == 1)){
	displayedResults = "<table>"
	displayedResults += "<tr><th>Element</th><th>Quantity</th><th>Purity</th><th>Error</th></tr>"
	
	$("#tableChosenElements").children("tbody").children().each(function(i,tr){
		// not the headers
		if (i != 0){  			
			xmlResult += "<constituent>";
			xmlResult += "<element>"  + $($(tr).children()[0]).html() + "</element>";
			xmlResult += "<quantity>"  + $($(tr).children()[1]).children().val() + "</quantity>"; 
			xmlResult += "<purity>"  + $($(tr).children()[2]).children().val() + "</purity>";
			xmlResult += "<error>"  + $($(tr).children()[3]).children().val() + "</error>";
			xmlResult += "</constituent>";
			
			displayedResults += "<tr>";
			displayedResults += "<td style='text-align:center'>"  + $($(tr).children()[0]).html() + "</td>";
			displayedResults += "<td style='text-align:center'>"  + $($(tr).children()[1]).children().val() + "</td>"; 
			displayedResults += "<td style='text-align:center'>"  + $($(tr).children()[2]).children().val() + "</td>";
			displayedResults += "<td style='text-align:center'>"  + $($(tr).children()[3]).children().val() + "</td>";
			displayedResults += "</tr>";
		}
	})
	displayedResults += "</table>"
}

$($(divElement).parent()).children(".moduleDisplay").html(displayedResults);
$($(divElement).parent()).children(".moduleResult").html(xmlResult);

// reset for next selection
document.getElementById('chosenMultipleElements').innerHTML = "<table id='tableChosenElements'>" +
															"<tr><th>Element</th><th>Quantity</th><th>Purity</th><th>Error</th><th>Actions</th></tr>" +
															"<tr><td colspan='5' style='text-align:center; color:red;'>No selected elements.</td></tr>" +
													"</table>" 
console.log('END [selectElement(' + divElement + ')]');
}


/**
 * Remove an element from the selection
 */
removeMultipleElement = function(removeButton){
	console.log('BEGIN [removeMultipleElement)]');
	
	$($($(removeButton).parent()).parent()).remove();
	
	if ($("#tableChosenElements").children("tbody").children().length == 1){
		document.getElementById('chosenMultipleElements').innerHTML = "<table id='tableChosenElements'>" +
		"<tr><th>Element</th><th>Quantity</th><th>Purity</th><th>Error</th><th>Actions</th></tr>" +
		"<tr><td colspan='5' style='text-align:center; color:red;'>No selected elements.</td></tr>" +
		"</table>" 
	}
	
	console.log('END [removeMultipleElement]');
}


/**
 * Update the display regarding the choice of the user.
 * @param selectObj
 */
changeChoice = function(selectObj)
{
    console.log('BEGIN [changeChoice(' + selectObj.id + ' : ' + selectObj.selectedIndex + ')]');

    // get the index of the selected option 
    var idx = selectObj.selectedIndex;

    // change the displayed choice
    for (i=0; i < selectObj.options.length;i++) {
    	if (i == idx){
    		$("#" + selectObj.id + "-" + i).removeAttr("class");
		} else {
			$("#" + selectObj.id + "-" + i).attr("class","notchosen");
		}
    }
    // the choice is not yet generated
    if ($("#" + selectObj.id + "-" + idx).children().length == 0){
        // save values in the form
        $("input").each(function(){
	        $(this).attr("value", $(this).val());
	    });
	    $('select option').each(function(){ this.defaultSelected = this.selected; });
	    // generate selected choice
        generate(selectObj.id.substr(6) + "-" + idx, "choice");
    }

    console.log('END [changeChoice(' + selectObj.id + ' : ' + selectObj.selectedIndex + ')]');
}


/**
 * Show a dialog when a template is selected
 */
displayTemplateSelectedDialog = function()
{
 $(function() {
    $( "#dialog-message" ).dialog({
      modal: true,
      buttons:
    	  [
           {
               text: "Start",
               click: function() {
            	   
            	   if (validateStartCurate()){
	            	   var formData = new FormData($( "#form_start" )[0]);
	            	   $.ajax({
	            	        url: "/curate/start_curate",
	            	        type: 'POST',
	            	        data: formData,
	            	        cache: false,
	            	        contentType: false,
	            	        processData: false,
	            	        async:false,
	            	   		success: function(data){
	            	   			window.location = '/curate/enter-data'
	            	        },
	            	        error:function(data){
	            	        	$("#form_start_errors").html(data.responseText);
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

/**
 * AJAX call, launch the curation from the selected parameters
 */
start_curate = function(){
    $.ajax({
        url : "/curate/start_curate",
        type : "POST",
        dataType: "json",
        success: function(data){
        }
    });
}


/**
 * Check if the template is selected, to prevent manual navigation.
 */
verifyTemplateIsSelectedCurateEnterData = function(){
    console.log('BEGIN [verifyTemplateIsSelected]');

    verify_template_is_selected(verifyTemplateIsSelectedCurateEnterDataCallback);

    console.log('END [verifyTemplateIsSelected]');
}


/**
 * AJAX call, checks that a template has been selected
 * @param callback
 */
verify_template_is_selected = function(callback){
    $.ajax({
        url : "/curate/verify_template_is_selected",
        type : "GET",
        dataType: "json",
        success: function(data){
            callback(data.templateSelected);
        }
    });
}


/**
 * Callback redirects to main page if no templates selected.
 * @param data
 */
verifyTemplateIsSelectedCurateEnterDataCallback = function(templateSelected)
{
    console.log('BEGIN [verifyTemplateIsSelectedCallback]');

    if (templateSelected == 'no') {
        location.href = "/curate";
    }else{
    	loadCurrentTemplateFormForCuration();
    }

    console.log('END [verifyTemplateIsSelectedCallback]');
}


/**
 * Load the form to curate data
 */
loadCurrentTemplateFormForCuration = function()
{
    console.log('BEGIN [loadCurrentTemplateFormForCuration]');

    $('.btn.clear-fields').on('click', clearFields);
    $('.btn.save-form').on('click', saveForm);
    $('.btn.download').on('click', downloadOptions);

    generate_xsd_form();

    console.log('END [loadCurrentTemplateFormForCuration]');
}


/**
 * AJAX call, generates HTML form from XSD
 */
generate_xsd_form = function(){
    $.ajax({
        url : "/curate/generate_xsd_form",
        type : "GET",
        dataType: "json",
        success : function(data) {
            $('#modules').html(data.modules);
            $('#periodicTable').html(data.periodicTable);
            $('#periodicTableMultiple').html(data.periodicTableMultiple);
            $('#xsdForm').html(data.xsdForm);
            setTimeout(disable_elements ,0);
            
            initModules();
        },
    });
}


/**
 * Check that the tempalte is selected or redirect to main page
 */
verifyTemplateIsSelectedViewData = function(){
    console.log('BEGIN [verifyTemplateIsSelected]');

    verify_template_is_selected(verifyTemplateIsSelectedViewDataCallback);

    console.log('END [verifyTemplateIsSelected]');
}


/**
 * Check that the tempalte is selected or redirect to main page
 */
verifyTemplateIsSelectedViewDataCallback = function(data)
{
    console.log('BEGIN [verifyTemplateIsSelectedCallback]');

    if (data.templateSelected == 'no') {
        location.href = "/curate";
    }else{
    	loadCurrentTemplateView();
    	load_xml();
    }

    console.log('END [verifyTemplateIsSelectedCallback]');
}


/**
 * AJAX call, loads XML data into the page for review
 */
load_xml = function(){
    $.ajax({
        url : "/curate/load_xml",
        type : "GET",
        dataType: "json",
        success : function(data) {
            $('#XMLHolder').html(data.XMLHolder);
        }
    });
}


/**
 * Load template view controllers
 */
loadCurrentTemplateView = function()
{
    console.log('BEGIN [loadCurrentTemplateView]');

    $('.btn.download-xml').on('click', downloadXML);
    $('.btn.save-to-repo').on('click', saveToRepository);

    console.log('END [loadCurrentTemplateView]');
}


/**
 * Shows a dialog to choose dialog options
 */
downloadOptions = function()
{
 $(function() {
    $( "#dialog-download-options" ).dialog({
      modal: true,
      buttons: {
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });
}


/**
 * Download the XML document
 */
downloadXML = function()
{
    console.log('BEGIN [downloadXML]');

    download_xml();

    console.log('END [downloadXML]');
}


/**
 * AJAX call, get XML data and redirects to download view
 */
download_xml = function(){
    $.ajax({
        url : "/curate/download_xml",
        type : "GET",
        dataType: "json",
        success : function(data) {
            window.location = "/curate/view-data/download-XML?id="+ data.xml2downloadID
        }
    });
}


/**
 * Download the XSD template
 */
downloadXSD = function()
{
    console.log('BEGIN [downloadXSD]');

    console.log('[downloadXSD] Downloading XSD...');
    
    window.location = '/curate/enter-data/download-XSD';
    $( "#dialog-download-options" ).dialog("close");
    
    console.log('[downloadXSD] Schema downloaded');

    console.log('END [downloadXSD]');
}


/**
 * Download the current XML document
 */
downloadCurrentXML = function()
{
    console.log('BEGIN [downloadCurrentXML]');
    
	var rootElement = document.getElementsByName("xsdForm")[0];
	var xmlString = '';
    
    xmlString = generateXMLString (rootElement);   
    
    download_current_xml(xmlString);
    
    console.log('END [downloadCurrentXML]');
}


/**
 * AJAX call, download XML document in its current form
 */
download_current_xml = function(xmlString){
    $.ajax({
        url : "/curate/enter-data/download_current_xml",
        type : "POST",
        dataType: "json",
        data:{
        	xmlString: xmlString
        },
        success : function(data) {
        	window.location = "/curate/view-data/download-XML?id="+ data.xml2downloadID
        	$("#dialog-download-options").dialog("close");
        }
    });
}


/**
 * Save XML data to repository. Shows dialog.
 */
saveToRepository = function()
{
    console.log('BEGIN [saveToRepository]');

    $(function() {
        $( "#dialog-save-data-message" ).dialog({
            modal: true,
            buttons: {
            	Save: function() {
					$( this ).dialog( "close" );
					doSaveToRepository();
                },
				Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
	
    console.log('END [saveToRepository]');
}


/**
 * Save XML data to repository. 
 */
doSaveToRepository = function()
{
    console.log('BEGIN [doSaveToRepository]');

    save_xml_data_to_db();

    console.log('END [doSaveToRepository]');
}


/**
 * AJAX call, saves data to database
 * @param saveAs title of the document
 */
save_xml_data_to_db = function(saveAs){
    $.ajax({
        url : "/curate/save_xml_data_to_db",
        type : "POST",
        dataType: "json",
        data:{
        },
        success : function(data) {
            if ('errors' in data){
                $("#saveErrorMessage").html(data.errors);
                $(function() {
                    $( "#dialog-save-error-message" ).dialog({
                        modal: true,
                        buttons: {
                        	Ok: function() {
                                $( this ).dialog( "close" );
                            }
                        }
                    });
                });                
            }else{
                savedXMLDataToDB();
            }
        }
    });
}


/**
 * Saved XML data to DB message.
 */
savedXMLDataToDB = function()
{
    console.log('BEGIN [savedXMLDataToDB]');

    $(function() {
        $( "#dialog-saved-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                    window.location = "/curate"
                }
	    }
        });
    });
    
    console.log('END [savedXMLDataToDB]');
}


/**
 * Save XML data to DB error message. 
 */
saveXMLDataToDBError = function()
{
    console.log('BEGIN [saveXMLDataToDBError]');
    
    $(function() {
        $( "#dialog-save-error-message" ).dialog({
            modal: true,
            buttons: {
            	Ok: function(){
            		$(this).dialog("close");
            	}
            }
        });
    });
    
    console.log('END [saveXMLDataToDBError]');
}


/**
 * Duplicate or remove an element
 * @param operation
 * @param tagID
 * @returns {Boolean}
 */
changeHTMLForm = function(operation, tagID)
{
    console.log('BEGIN [changeHTMLForm(' + operation + ')]');
    
    $("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });

    if (operation == 'add') {
        // the element has to be created
        if ($("#element"+tagID).children("ul").length == 0 && // complex element not generated
        $("#element"+tagID).children("input").length == 0 && // input element not generated
        $("#element"+tagID).children("select").length == 0 && // enumeration not generated 
        $("#element"+tagID).children("div.module").length == 0){ // module not generated
            generate(tagID, "element");
        }
        else{
            // the element is already generated
            $("#element"+tagID).children(".expand").attr("class","collapse");
            duplicate(tagID);
        }
    } else if (operation == 'remove') {
    	$("#element"+tagID).children(".collapse").attr("class","expand");
		remove(tagID);
    }

    console.log('END [changeHTMLForm(' + operation + ')]');

    return false;
}


/**
 * AJAX call, generate an element from the form
 * @param tagID HTML id of the element to generate
 */
generate = function(tagID, tag){
    var xsdForm = $("#xsdForm").html();
    $.ajax({
        url : "/curate/generate",
        type : "POST",
        dataType: "json",
        data : {
            tagID : tagID,
            tag: tag,
            xsdForm: xsdForm
        },
        success: function(data){
            $("#xsdForm").html(data.xsdForm);
            $("#element" + tagID).prop("disabled",false);
            $("#element" + tagID).children('select').prop("disabled",false);
            $("#element" + tagID).removeClass("removed");
            $("#element" + tagID).children("ul").show(500);

            initModules();
        }
    });
}

/**
 * AJAX call, duplicate an element from the form
 * @param tagID HTML id of the element to duplicate
 */
duplicate = function(tagID){
    $.ajax({
        url : "/curate/can_duplicate",
        type : "POST",
        dataType: "json",
        data : {
            tagID : tagID,
        },
        success: function(data){
        	if ('occurs' in data){
        		if (data.occurs == "zero"){
		            $('#add' + data.id).attr('style', data.styleAdd);
		            $('#remove' + data.id).attr('style','');
		            $("#" + data.tagID).prop("disabled",false);
		            $("#" + data.tagID).children('select').prop("disabled",false);
		            $("#" + data.tagID).removeClass("removed");
		            $("#" + data.tagID).children("ul").attr('style','');
		            if($("#element"+tagID).attr("class").split(" ").indexOf("choice") > -1 && $("#element"+tagID).children("ul").children().length == 0){ // choice element not generated
		            	changeChoice($("#element"+tagID).children("select")[0]);
		            }
	            }
	            else{
	            	var xsdForm = $("#xsdForm").html();
	            	
	            	$.ajax({
				        url : "/curate/duplicate",
				        type : "POST",
				        dataType: "json",
				        data : {
				            tagID : tagID,
				            xsdForm: xsdForm
				        },
				        success: function(data){
				        	$("#xsdForm").html(data.xsdForm);
				        }
        			});
	            }
        	}
        }
    });
}

/**
 * disable removed element
 * @param tagID HTML id of the element to disable
 */
disable_element = function(tagID){
	$("#" + tagID).children(".collapse").attr("class","expand");
	$('#add' + tagID.substring(7)).attr('style','');
    $('#remove' + tagID.substring(7)).attr('style','display:none');
    $("#" + tagID).prop("disabled",true);
    $("#" + tagID).children('select').prop("disabled",true);
    $("#" + tagID).children("ul").hide();
}

/**
 * disable all removed elements
 * @param tagID HTML id of the element to disable
 */
disable_elements = function(){
	$("#xsdForm").find(".removed").each(function(){
		disable_element($(this).attr('id'));
	});
}

/**
 * AJAX call, remove an element from the form
 * @param tagID HTML id of the element to remove
 */
remove = function(tagID){
$.ajax({
        url : "/curate/can_remove",
        type : "POST",
        dataType: "json",
        data : {
            tagID : tagID,
        },
        success: function(data){
        	if ('occurs' in data){
        		if (data.occurs == "zero"){
                    $("#" + data.tagID).addClass("removed");
                    $('#add' + data.tagID.substring(7)).attr('style','');
                    $('#remove' + data.tagID.substring(7)).attr('style','display:none');
                    $("#" + data.tagID).prop("disabled",true);
                    $("#" + data.tagID).children('select').prop("disabled",true);
                    $("#" + data.tagID).children("ul").hide(500);
        		}else{
        			var xsdForm = $("#xsdForm").html();     			
        			$.ajax({
				        url : "/curate/remove",
				        type : "POST",
				        dataType: "json",
				        data : {
				            tagID : tagID,
				            xsdForm: xsdForm
				        },
				        success: function(data){
				        	$("#xsdForm").html(data.xsdForm);
				        }
        			});
        		}
        	}
        }
    });
}


/**
 * Set the current template 
 * @returns {Boolean}
 */
setCurrentTemplate = function()
{
	var templateName = $(this).parent().parent().children(':first').text();
	var templateID = $(this).parent().parent().children(':first').attr('templateID');
	var templateFilename = $(this).parent().parent().children(':nth-child(2)').text();
	var tdElement = $(this).parent();
		
	tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
	$('.btn.set-template').off('click');
	
	console.log('[setCurrentTemplate] Setting '+templateName+' with filename '+templateFilename+' as current template...');

    set_current_template(templateFilename,templateID);

    return false;
}


/**
 * AJAX call, sets the current template
 * @param templateFilename name of the selected template
 * @param templateID id of the selected template
 */
set_current_template = function(templateFilename,templateID){
    $.ajax({
        url : "/curate/set_current_template",
        type : "POST",
        dataType: "json",
        data : {
            templateFilename : templateFilename,
            templateID: templateID
        },
        success: function(){
            setCurrentTemplateCallback();
        }
    });
}


/**
 * Set current user defined template
 * @returns {Boolean}
 */
setCurrentUserTemplate = function()
{
	var templateName = $(this).parent().parent().children(':first').text();
	var templateID = $(this).parent().parent().children(':first').attr('templateID');
	var tdElement = $(this).parent();
		
	tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
	$('.btn.set-template').off('click');

    set_current_user_template(templateID);

    return false;
}


/**
 * AJAX call, sets the current user defined template
 * @param templateID
 */
set_current_user_template = function(templateID){
    $.ajax({
        url : "/curate/set_current_user_template",
        type : "POST",
        dataType: "json",
        data : {
            templateID: templateID
        },
        success: function(){
            setCurrentTemplateCallback();
        }
    });
}

load_start_form = function(){
	$.ajax({
        url : "/curate/start_curate",
        type : "GET",
        dataType: "json",
        data : {
        	
        },
        success: function(data){
            $("#form_start_content").html(data.template);
        }
    });
}

validateStartCurate = function(){
	errors = ""
	
	// check if an option has been selected
	selected_option = $( "#form_start" ).find("input:radio[name='curate_form']:checked").val()
	if (selected_option == undefined){
		errors = "No option selected. Please check one radio button."
		$("#form_start_errors").html(errors);
		return (false);
	}else{
		if (selected_option == "new"){
			if ($( "#id_document_name" ).val().trim() == ""){
				errors = "You selected the option 'Create a new document'. Please provide a name for the document."
			}
		}else if (selected_option == "open"){
			if ($( "#id_forms" ).val() == ""){
				errors = "You selected the option 'Open a Form'. Please select an existing form from the list."
			}
		}else if (selected_option == "upload"){
			if ($( "#id_file" ).val() == ""){
				errors = "You selected the option 'Upload a File'. Please select an XML file."
			}
		}
	}
		
	if (errors != ""){
		$("#form_start_errors").html(errors);
		return (false);
	}else{
		return (true)
	}	
}


/**
 * Update page when template selected.
 * @param data
 */
setCurrentTemplateCallback = function()
{
    console.log('BEGIN [setCurrentTemplateCallback]');

    $('#template_selection').load(document.URL +  ' #template_selection', function() {
    	loadTemplateSelectionControllers();
    	displayTemplateSelectedDialog();
    });
    
    load_start_form();
    
    console.log('END [setCurrentTemplateCallback]');
}

