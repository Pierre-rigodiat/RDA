loadTemplateSelectionControllers = function()
{
    console.log('BEGIN [loadTemplateSelectionControllers]');
    $('.btn.set-template').on('click', setCurrentTemplate);
    $('.btn.set-curate-user-template').on('click', setCurrentUserTemplate);   
    console.log('END [loadTemplateSelectionControllers]');
}

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

doLoadForm = function()
{
    console.log('BEGIN [doLoadForm]');

    var formSelectedArray = document.getElementById('listOfForms');
    var formSelected = formSelectedArray.options[formSelectedArray.selectedIndex].value;

    Dajaxice.curate.loadFormForEntry(loadFormForEntryCallback,{'formSelected':formSelected});

    console.log('END [doLoadForm]');

    return false;
}

loadFormForEntryCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [loadFormForEntryCallback]');
    console.log('data passed back to callback function: ' + data);

    // business logic goes here

    console.log('END [loadFormForEntryCallback]');

    return false;
}

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

validateXML = function()
{
	var rootElement = document.getElementsByName("xsdForm")[0];
	var xmlString = '';
	
    xmlString = generateXMLString (rootElement, xmlString);
    
    Dajaxice.curate.validateXMLData(Dajax.process,{'xmlString':xmlString});
}

saveXMLDataCallback = function()
{
    console.log('BEGIN [saveXMLData]');

    window.location = "/curate/view-data"

    console.log('END [saveXMLData]');
}

generateXMLString = function(elementObj)
{
    console.log('BEGIN [generateXMLString]');

    var xmlString="";

    var children = elementObj.childNodes;
    for(var i = 0; i < children.length; i++) {
	console.log(children[i].tagName);
	if (children[i].nodeType == 1 && children[i].hasAttribute("xmlID")) {
	    if (children[i].getAttribute("xmlID") == "root") {
//		if (children[i].hasAttribute("hdf5ns")) {
//		    xmlString += "<" + children[i].firstChild.innerHTML.trim() + " xmlns:hdf5=\"http://hdfgroup.org/HDF5/XML/schema/HDF5-File\">"
//		    xmlString += generateXMLString(children[i]);
//		    xmlString += "</" + children[i].firstChild.innerHTML.trim() + ">"
//		} else {
		    xmlString += "<" + children[i].firstChild.innerHTML.trim() + ">"
		    xmlString += generateXMLString(children[i]);
		    xmlString += "</" + children[i].firstChild.innerHTML.trim() + ">"
//		}
	    }
	} else if (children[i].tagName == "UL") {
	    if (children[i].style.display != "none") {
		xmlString += generateXMLString(children[i]);
	    }
	} else if (children[i].tagName == "LI") {
		if (! $(children[i]).hasClass("removed") ) {
		    console.log(children[i].innerHTML);
		    var nobrNode1 = children[i].children[0];
		    var nobrNode2 = children[i].children[1];
		    if (nobrNode1.firstChild != null) {
			console.log(nobrNode1.firstChild.tagName);
			if (nobrNode1.firstChild.tagName == "DIV") {
//				tagId = $(nobrNode1.firstChild).attr("id");
//				if (typeof tagId !== typeof undefined && tagId !== false && tagId == "hdf5File") {
//					xmlString += hdf5String
//				}
	//		    alert("hdf5file matched");
	//		    xmlString += hdf5String;
			} else if (nobrNode1.firstChild.nodeValue.trim() != "Choose") {
			    xmlString += "<" + nobrNode1.firstChild.nodeValue.trim() + ">";
			    if (nobrNode1.firstChild.nodeValue.trim() == "Table") {
				xmlString += "table";
			    }
			    xmlString += generateXMLString(children[i]);
			    xmlString += "</" + nobrNode1.firstChild.nodeValue.trim() + ">";
			} else {
			    xmlString += generateXMLString(children[i]);
			}
		    } else if (nobrNode2.firstChild != null) {
			if (nobrNode2.firstChild.nodeValue.trim() != "Choose") {
			    xmlString += "<" + nobrNode2.firstChild.nodeValue.trim() + ">";
			    xmlString += generateXMLString(children[i]);
			    xmlString += "</" + nobrNode2.firstChild.nodeValue.trim() + ">";
			} else {
			    xmlString += generateXMLString(children[i]);
			}
		    } else {
			xmlString += generateXMLString(children[i]);
		    }
		}
	}
	else if (children[i].tagName == "DIV" && $(children[i]).hasClass("module") ){
		xmlString += $($(children[i]).parent()).find(".moduleResult").html();		
	} 
//	else if (children[i].tagName == "DIV"){
//		valModule = $(children[i]).attr("value");
//		if (typeof valModule !== typeof undefined && valModule !== false) {
//			xmlString += valModule
//		}
//	} 	
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
    
    console.log('END [generateXMLString]');

    return xmlString
}

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

//selectElement = function(periodicTableElement,divElement, selectedElementId)
//{
//    console.log('BEGIN [selectElement(' + periodicTableElement + ',' + divElement + ')]');
//
//    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>" + periodicTableElement + "</b>";
//
//    $(function() {
//	$("#dialog-select-element" ).dialog({ width: 700 });
//        $("#dialog-select-element" ).dialog({
//            modal: true,
//            buttons: {
//		Select: function() {
//		    		doSelectElement(divElement, selectedElementId);
//                    $( this ).dialog( "close" );
//                },
//		Cancel: function() {
//                    $( this ).dialog( "close" );
//                }
//	    }
//        });
//    });
//	
//    console.log('END [selectElement]');
//}
//
//chooseElement = function(element)
//{
//console.log('BEGIN [chooseElement(' + element + ')]');
//
//$('#chosenElement').html("Chosen Element: <b id=\"selectedElement\">" + element + "</b>");
//
//console.log('END [chooseElement(' + element + ')]');
//}
//
//doSelectElement = function(divElement, selectedElementId)
//{
//console.log('BEGIN [selectElement(' + divElement + ')]');
//
////var selectedElement = document.getElementById('selectedElement').innerHTML;
////divElement.onclick = function onclick(event) { selectElement(selectedElement,this); }
////divElement.parentNode.childNodes[2].innerHTML = "Current Selection: " + selectedElement;
//var selectedElement = document.getElementById('selectedElement').innerHTML;
//divElement.onclick = function onclick(event) { selectElement(selectedElement,this); }
//document.getElementById('elementSelected'+selectedElementId).innerHTML = "Current Selection: " + selectedElement;
//
//// reset for next selection
//document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>None</b>";
//
//console.log('END [selectElement(' + divElement + ')]');
//}

selectElement = function(divElement)
{   
	console.log('BEGIN [selectElement()]');
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
	console.log('END [selectElement()]');
}

chooseElement = function(element)
{
    console.log('BEGIN [chooseElement(' + element + ')]');

    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b id=\"selectedElement\">" + element + "</b>";

    console.log('END [chooseElement(' + element + ')]');
}

doSelectElement = function(divElement)
{
    console.log('BEGIN [selectElement(' + divElement + ')]');

    var selectedElement = document.getElementById('selectedElement').innerHTML;
    divElement.onclick = function onclick(event) { selectElement(selectedElement,this); }	
	$($(divElement).parent()).children(".moduleDisplay").html("Current Selection: "+selectedElement);
	//$($(divElement).parent()).children(".moduleResult").html("<element>" + selectedElement + "</element>");
	$($(divElement).parent()).children(".moduleResult").html(selectedElement);
	
    // reset for next selection
    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>None</b>";

    console.log('END [selectElement(' + divElement + ')]');
}

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

doSelectHDF5File = function(divElement)
{
	moduleTag = $(divElement).parent();
    Dajaxice.curate.getHDF5String(getHDF5StringCallback);
}

getHDF5StringCallback = function(data)
{
	spreadsheetXML = data.spreadsheetXML;

	if (spreadsheetXML != ""){
		moduleTag.children(".moduleResult").html(spreadsheetXML);
		moduleTag.children(".moduleDisplay").html("Spreadsheet successfully loaded.");
	}	
	
}

changeChoice = function(selectObj)
{
    console.log('BEGIN [changeChoice(' + selectObj.id + ' : ' + selectObj.selectedIndex + ')]');

    // get the index of the selected option 
    var idx = selectObj.selectedIndex;  

    for (i=0; i < selectObj.options.length;i++) {
    	if (i == idx){
    		$("#" + selectObj.id + "-" + i).removeAttr("style");
		} else {
			$("#" + selectObj.id + "-" + i).attr("style","display:none");
		}    	
    }

    console.log('END [changeChoice(' + selectObj.id + ' : ' + selectObj.selectedIndex + ')]');
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

verifyTemplateIsSelectedCurateEnterData = function(){
    console.log('BEGIN [verifyTemplateIsSelected]');

    Dajaxice.curate.verifyTemplateIsSelected(verifyTemplateIsSelectedCurateEnterDataCallback); 

    console.log('END [verifyTemplateIsSelected]');
}

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
//    $('.btn.select-element').on('click', selectElement);

    Dajaxice.curate.generateXSDTreeForEnteringData(Dajax.process); //,{'templateFilename':'xxxx'});

    Dajaxice.curate.updateFormList(Dajax.process);

    console.log('END [loadCurrentTemplateFormForCuration]');
}

loadExploreCurrentTemplateForm = function()
{
    console.log('BEGIN [loadExploreCurrentTemplateForm]');

    $('.btn.clear-fields').on('click', clearFields);
    $('.btn.load-form').on('click', loadForm);
    $('.btn.save-form').on('click', saveForm);

    Dajaxice.explore.generateXSDTreeForEnteringData(Dajax.process); //,{'templateFilename':'xxxx'});

    console.log('END [loadExploreCurrentTemplateForm]');
}

displayTemplateForm = function()
{
    console.log('BEGIN [displayTemplateForm]');

    
	
    console.log('END [displayTemplateForm]');
}

verifyTemplateIsSelectedViewData = function(){
    console.log('BEGIN [verifyTemplateIsSelected]');

    Dajaxice.curate.verifyTemplateIsSelected(verifyTemplateIsSelectedViewDataCallback); 

    console.log('END [verifyTemplateIsSelected]');
}

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


loadCurrentTemplateView = function()
{
    console.log('BEGIN [loadCurrentTemplateView]');

    $('.btn.download-xml').on('click', downloadXML);
    $('.btn.save-to-repo').on('click', saveToRepository);

    //    Dajaxice.curate.generateXSDTreeForEnteringData(Dajax.process); //,{'templateFilename':'xxxx'});

    console.log('END [loadCurrentTemplateView]');
}


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


downloadXML = function()
{
    console.log('BEGIN [downloadXML]');

    Dajaxice.curate.downloadXML(Dajax.process);

    console.log('END [downloadXML]');
}


downloadXSD = function()
{
    console.log('BEGIN [downloadXSD]');

    console.log('[downloadXSD] Downloading XSD...');
    
    window.location = '/curate/enter-data/download-XSD';
    $( "#dialog-download-options" ).dialog("close");
    
    console.log('[downloadXSD] Schema downloaded');

    console.log('END [downloadXSD]');
}

downloadForm = function()
{
    console.log('BEGIN [downloadForm]');

//    dataToDownload = document.getElementById('xsdForm').innerHTML;
//    document.location = 'data:Application/octet-stream,' + encodeURIComponent(dataToDownload);
    
    Dajaxice.curate.saveHTMLForm(downloadFormCallback,{'saveAs':"form2download", 'content':document.getElementById('xsdForm').innerHTML});

    console.log('END [downloadForm]');
}

downloadFormCallback = function()
{
    console.log('BEGIN [downloadFormCallback]');

    window.location = '/curate/enter-data/download-form';
    $( "#dialog-download-options" ).dialog("close");
    
    console.log('END [downloadFormCallback]');
}

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

doSaveToRepository = function()
{
    console.log('BEGIN [doSaveToRepository]');

    Dajaxice.curate.saveXMLDataToDB(Dajax.process,{'saveAs':document.getElementById('saveAsInput').value});

    console.log('END [doSaveToRepository]');
}

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



changeHTMLForm = function(operation,selectObj, tagID)
{
    console.log('BEGIN [changeHTMLForm(' + operation + ',' + selectObj + ']');
    console.log(tagID);
    if (operation == 'add') {
//		var nodeToAdd = selectObj.parentNode.parentNode;
//		var parentNode = nodeToAdd.parentNode;
		$("input").each(function(){
		    $(this).attr("value", $(this).val());
		});
		$('select option').each(function(){ this.defaultSelected = this.selected; });
		var xsdForm = $("#xsdForm").html()
		Dajaxice.curate.duplicate(Dajax.process,{"tagID":tagID, "xsdForm":xsdForm})
    } else if (operation == 'remove') {
    	$("input").each(function(){
		    $(this).attr("value", $(this).val());
		});
		$('select option').each(function(){ this.defaultSelected = this.selected; });
		var xsdForm = $("#xsdForm").html()
		Dajaxice.curate.remove(Dajax.process,{"tagID":tagID, "xsdForm":xsdForm})
    }
    
    console.log('END [changeHTMLForm(' + operation + ',' + selectObj + ']');

    return false;
}


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

setCurrentTemplateCallback2 = function(templateName,notifElement)
{
    Dajax.process(templateName,notifElement);
    console.log('[setCurrentTemplateCallback] '+templateName);
    notifElement.html('<span style="color:green;font-weight:bold">Current template</span>');
}

generateTrees = function(notifElement)
{
	var trElement = notifElement.parent(),
		trElementClass = trElement.attr('class');
	
	$.ajax({
        url: 'parser/controllers/php/generateReferenceTrees.php',
        type: 'GET',
        success: function(data) {
        	try
        	{
        		var jsonObject = $.parseJSON(data);
        		
        		if(jsonObject.code>=0)
	        	{
					console.log('[generateReferenceTrees] Trees generated');
					
					loadPage($(location).attr('href'));
	        	}
	        	else
	        	{
	        		console.error('[generateReferenceTrees] Error '+jsonObject.code+'  ('+jsonObject.result+') occured while toggle module');
	        		
	        		trElement.attr('class', (trElementClass?trElementClass+' error':'error'));
            		notifElement.html('<span style="font-weight:bold;color:red">Ajax call error</span>');
	        	}
        	}
        	catch(ex)
        	{
        		console.error('[generateReferenceTrees] JSON parsing error');
        		
        		trElement.attr('class', (trElementClass?trElementClass+' error':'error'));
            	notifElement.html('<span style="font-weight:bold;color:red">Ajax call error</span>');
        	}
        },
        error: function() {
            console.error("[generateReferenceTrees] Problem with the AJAX call");
            
            trElement.attr('class', (trElementClass?trElementClass+' error':'error'));
            notifElement.html('<span style="font-weight:bold;color:red">Ajax call error</span>');
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}
