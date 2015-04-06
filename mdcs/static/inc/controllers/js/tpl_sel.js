/**
 * 
 * File Name: tpl_sel.js
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
 * Load controllers for template selection
 */
loadTemplateSelectionControllers = function()
{
    console.log('BEGIN [loadTemplateSelectionControllers]');
    $('.btn.set-template').on('click', setCurrentTemplate);
    $('.btn.set-curate-user-template').on('click', setCurrentUserTemplate);
    Dajaxice.curate.initCuration(Dajax.process);
    console.log('END [loadTemplateSelectionControllers]');    
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
            		Dajaxice.curate.clearFields(Dajax.process);
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
 * Load an existing form. Show the window.
 */
loadForm = function()
{
    console.log('BEGIN [loadForm]');

    $(function() {
        $( "#dialog-load-form-message" ).dialog({
            modal: true,
            buttons: {
		Load: function() {
                    $( this ).dialog( "close" );
                    doLoadForm();
                },
		Cancel: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [loadForm]');
}

/**
 * Load an existing form.
 * @returns {Boolean}
 */
doLoadForm = function()
{
    console.log('BEGIN [doLoadForm]');

    var formSelectedArray = document.getElementById('listOfForms');
    var formSelected = formSelectedArray.options[formSelectedArray.selectedIndex].value;

    Dajaxice.curate.loadFormForEntry(loadFormForEntryCallback,{'formSelected':formSelected});

    console.log('END [doLoadForm]');

    return false;
}

/**
 * Load form callback.
 * @param data
 * @returns {Boolean}
 */
loadFormForEntryCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [loadFormForEntryCallback]');
    console.log('data passed back to callback function: ' + data);


    console.log('END [loadFormForEntryCallback]');

    return false;
}

/**
 * Display message when form loaded.
 */
formLoaded = function()
{
    console.log('BEGIN [loadForm]');

    $(function() {
        $( "#dialog-form-loaded-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [loadForm]');
}

/**
 * Save the current form. Show the window.
 */
saveForm = function()
{
    console.log('BEGIN [saveForm]');

    $(function() {
        $( "#dialog-save-as-message" ).dialog({
            modal: true,
            buttons: {
		Save: function() {
		    if (document.getElementById('saveAsInput').value.length>0) {
			$( this ).dialog( "close" );
			doSave();
		    } else {
			document.getElementById('saveAsErrorMessage').innerHTML = "<font color=\"red\">Please enter a name</font>";
		    }
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
 * Save an existing form. 
 */
doSave = function()
{
    console.log('BEGIN [doSave]');

    // Need to Set input values explicitiy before sending innerHTML for save
    var elems = document.getElementsByName("xsdForm")[0].getElementsByTagName("input");
    for(var i = 0; i < elems.length; i++) {
	// sent attribute to property value
	elems[i].setAttribute("value", elems[i].value);
    }

    var elems = document.getElementsByName("xsdForm")[0].getElementsByTagName("select");
    for(var i = 0; i < elems.length; i++) {
	// get the index of the selected option 
	var idx = elems[i].selectedIndex; 
	// set the value of the selected option to selected
	elems[i].selectedIndex = idx;
    }

    Dajaxice.curate.saveHTMLForm(saveHTMLFormCallback,{'saveAs':document.getElementById('saveAsInput').value, 'content':document.getElementById('xsdForm').innerHTML});

    $(function() {
        $( "#dialog-saved-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
		    document.getElementById('saveAsInput').value = "";
		    document.getElementById('saveAsErrorMessage').innerHTML = "";
                }
	    }
        });
    });
	
    console.log('END [doSave]');
}

/**
 * Display the current data to curate
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

    Dajaxice.curate.saveXMLData(saveXMLDataCallback,{'formContent':document.getElementById('xsdForm').innerHTML});

    console.log('END [viewData]');
}

/**
 * Validate the current data to curate.
 */
validateXML = function()
{
	var rootElement = document.getElementsByName("xsdForm")[0];
	var xmlString = '';
	
    xmlString = generateXMLString (rootElement, xmlString);
    console.log(xmlString);
    
    $("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
    Dajaxice.curate.validateXMLData(Dajax.process,{'xmlString':xmlString, 'xsdForm': $('#xsdForm').html()});
}

/**
 * Redirect to View Data.
 */
saveXMLDataCallback = function()
{
    console.log('BEGIN [saveXMLData]');

    window.location = "/curate/view-data"

    console.log('END [saveXMLData]');
}

/**
 * Generate an XML String from values entered in the form.
 * @param elementObj
 * @returns {String}
 */
generateXMLString = function(elementObj)
{
    var xmlString="";

    var children = elementObj.childNodes;
    for(var i = 0; i < children.length; i++) {
	    if (children[i].tagName == "UL") {
	    	if (! $(children[i]).hasClass("notchosen") ) {
	    		xmlString += generateXMLString(children[i]);
	    	}
		} else if (children[i].tagName == "LI") {
			if (! $(children[i]).hasClass("removed") ) {
			
				var textNode = $(children[i]).contents().filter(function(){
			        return this.nodeType === 3;
			    }).text();
				
				if (textNode.trim() != "Choose") {
				    xmlString += "<" + textNode + ">";
				    xmlString += generateXMLString(children[i]);
				    xmlString += "</" + textNode + ">";
				}else {
					xmlString += generateXMLString(children[i]);
				}
			    	
			}
		}
		else if (children[i].tagName == "DIV" && $(children[i]).hasClass("module") ){
			console.log($($(children[i]).parent()).find(".moduleResult").html());	
			xmlString += $($(children[i]).parent()).find(".moduleResult").html();		
		} 	
		else if (children[i].tagName == "SELECT") {
		    // get the index of the selected option 
		    var idx = children[i].selectedIndex; 
		    // get the value of the selected option 
		    var which = children[i].options[idx].value; 
		    	    
		    if (children[i].getAttribute("id") != null && children[i].getAttribute("id").indexOf("choice") > -1){
		    	xmlString += generateXMLString(children[i]);
		    }else {
		    	xmlString += which;
		    }	    
		} else if (children[i].tagName == "INPUT") {
		    xmlString += children[i].value;
		} else if (children[i].nodeType == 1 && children[i].getAttribute("id") != null && children[i].getAttribute("id").indexOf("elementSelected") > -1) {
		    var ptArray = children[i].innerHTML.split(" ");
		    xmlString += ptArray[ptArray.length - 1];
		} else {
		    xmlString += generateXMLString(children[i]);
		}
    }

    return xmlString
}

/**
 * 
 * @param data
 * @returns {Boolean}
 */
saveHTMLFormCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [saveHTMLFormCallback]');
    console.log('data passed back to callback function: ' + data);

    // business logic goes here
    Dajaxice.curate.updateFormList(Dajax.process);

    console.log('END [saveHTMLFormCallback]');

    return false;
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
 * Select an Excel Spreadseet. Show the dialog box.
 * @param hdf5File
 * @param divElement
 */
selectHDF5File = function(hdf5File,divElement)
{	
    $(function() {
        //$("#dialog-select-hdf5file" ).dialog({
    	$('<div id="dialog-select-hdf5file" title="Upload Spreadsheet File" style="display:none;">'+
    	'<iframe src="/curate/select-hdf5file">'+
    	'</iframe>'+	
    	'</div>' ).dialog({
            modal: true,
            buttons: {
            	Done: function() {
            		doSelectHDF5File(divElement);
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

var moduleTag;
/**
 * Select an Excel Spreadseet. 
 * @param divElement
 */
doSelectHDF5File = function(divElement)
{
	moduleTag = $(divElement).parent();
    Dajaxice.curate.getHDF5String(getHDF5StringCallback);
}

/**
 * Insert the Spreadsheet information in the form.
 * @param data
 */
getHDF5StringCallback = function(data)
{
	spreadsheetXML = data.spreadsheetXML;

	if (spreadsheetXML != ""){
		moduleTag.children(".moduleResult").html(spreadsheetXML);
		moduleTag.children(".moduleDisplay").html("Spreadsheet successfully loaded.");
	}	
	
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

    for (i=0; i < selectObj.options.length;i++) {
    	if (i == idx){
    		$("#" + selectObj.id + "-" + i).removeAttr("class");
		} else {
			$("#" + selectObj.id + "-" + i).attr("class","notchosen");
		}    	
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
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });
}

/**
 * Check if the template is selected, to prevent manual navigation.
 */
verifyTemplateIsSelectedCurateEnterData = function(){
    console.log('BEGIN [verifyTemplateIsSelected]');

    Dajaxice.curate.verifyTemplateIsSelected(verifyTemplateIsSelectedCurateEnterDataCallback); 

    console.log('END [verifyTemplateIsSelected]');
}

/**
 * Callback redirects to main page if no templates selected.
 * @param data
 */
verifyTemplateIsSelectedCurateEnterDataCallback = function(data)
{
    console.log('BEGIN [verifyTemplateIsSelectedCallback]');

    if (data.templateSelected == 'no') {
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
    $('.btn.load-form').on('click', loadForm);
    $('.btn.save-form').on('click', saveForm);
    $('.btn.download').on('click', downloadOptions);
    $('.btn.download-xsd').on('click', downloadXSD);
    $('.btn.download-form').on('click', downloadForm);
    $('.btn.download-xml').on('click', downloadXML);

    Dajaxice.curate.generateXSDTreeForEnteringData(Dajax.process); 

    Dajaxice.curate.updateFormList(Dajax.process);

    console.log('END [loadCurrentTemplateFormForCuration]');
}

/**
 * Load the form to customize fields for query
 */
loadExploreCurrentTemplateForm = function()
{
    console.log('BEGIN [loadExploreCurrentTemplateForm]');

    $('.btn.clear-fields').on('click', clearFields);
    $('.btn.load-form').on('click', loadForm);
    $('.btn.save-form').on('click', saveForm);

    Dajaxice.explore.generateXSDTreeForEnteringData(Dajax.process); //,{'templateFilename':'xxxx'});

    console.log('END [loadExploreCurrentTemplateForm]');
}

/**
 * 
 */
displayTemplateForm = function()
{
    console.log('BEGIN [displayTemplateForm]');

    
	
    console.log('END [displayTemplateForm]');
}

/**
 * Check that the tempalte is selected or redirect to main page
 */
verifyTemplateIsSelectedViewData = function(){
    console.log('BEGIN [verifyTemplateIsSelected]');

    Dajaxice.curate.verifyTemplateIsSelected(verifyTemplateIsSelectedViewDataCallback); 

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
    	Dajaxice.curate.loadXML(Dajax.process);
    }

    console.log('END [verifyTemplateIsSelectedCallback]');
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

    Dajaxice.curate.downloadXML(Dajax.process);

    console.log('END [downloadXML]');
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
 * Download the HTML form
 */
downloadForm = function()
{
    console.log('BEGIN [downloadForm]');
    
    Dajaxice.curate.downloadHTMLForm(Dajax.process,{'saveAs':"form2download", 'content':document.getElementById('xsdForm').innerHTML});

    console.log('END [downloadForm]');
}

/**
 * Save XML data to repository. Shows dialog.
 */
saveToRepository = function()
{
    console.log('BEGIN [saveToRepository]');

    $(function() {
        $( "#dialog-save-as-message" ).dialog({
            modal: true,
            buttons: {
		Save: function() {
		    if (document.getElementById('saveAsInput').value.length>0) {
			$( this ).dialog( "close" );
			doSaveToRepository();
		    } else {
			document.getElementById('saveAsErrorMessage').innerHTML = "<font color=\"red\">Please enter a name</font>";
		    }
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

    Dajaxice.curate.saveXMLDataToDB(Dajax.process,{'saveAs':document.getElementById('saveAsInput').value});

    console.log('END [doSaveToRepository]');
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
                    document.getElementById('saveAsInput').value = "";
                    document.getElementById('saveAsErrorMessage').innerHTML = "";
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
    console.log(tagID);
    
    $("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var xsdForm = $("#xsdForm").html()
	
    if (operation == 'add') {
    	$("#element"+tagID).children(".expand").attr("class","collapse");
		Dajaxice.curate.duplicate(Dajax.process,{"tagID":tagID, "xsdForm":xsdForm});		
    } else if (operation == 'remove') {    	
    	$("#element"+tagID).children(".collapse").attr("class","expand");
		Dajaxice.curate.remove(Dajax.process,{"tagID":tagID, "xsdForm":xsdForm});		
    }
    console.log('END [changeHTMLForm(' + operation + ')]');

    return false;
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

    Dajaxice.curate.setCurrentTemplate(setCurrentTemplateCallback,{'templateFilename':templateFilename,'templateID':templateID});

    return false;
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

    Dajaxice.curate.setCurrentUserTemplate(setCurrentTemplateCallback,{'templateID':templateID});

    return false;
}

/**
 * Update page when template selected.
 * @param data
 */
setCurrentTemplateCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [setCurrentTemplateCallback]');

    $('#template_selection').load(document.URL +  ' #template_selection', function() {
	loadTemplateSelectionControllers();
	displayTemplateSelectedDialog();
    });
    console.log('END [setCurrentTemplateCallback]');
}

