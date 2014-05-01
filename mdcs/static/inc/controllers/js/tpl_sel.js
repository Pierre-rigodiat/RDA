var hdf5String = "";

loadTemplateSelectionControllers = function()
{
    console.log('BEGIN [loadTemplateSelectionControllers]');
    $('.btn.set-template').on('click', setCurrentTemplate);
    $('.btn.set-explore-template').on('click', setExploreCurrentTemplate);
    console.log('END [loadTemplateSelectionControllers]');
}

clearFields = function()
{
    console.log('BEGIN [clearFields]');

    $('#dataEntryForm')[0].reset();

    $(function() {
        $( "#dialog-cleared-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
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

//    alert (document.getElementsByName("xsdForm")[0].innerHTML);

    var rootElement = document.getElementsByName("xsdForm")[0];
    var xmlString = '';

    xmlString = generateXMLString (rootElement,xmlString);

    // Need to Set input values explicitiy before sending innerHTML for save
    var elems = document.getElementsByName("xsdForm")[0].getElementsByTagName("input");
    for(var i = 0; i < elems.length; i++) {
	// sent attribute to property value
	elems[i].setAttribute("value", elems[i].value);
    }

    Dajaxice.curate.saveXMLData(saveXMLDataCallback,{'xmlContent':xmlString,'formContent':document.getElementById('xsdForm').innerHTML});

//    alert (formatXml(xmlString));

    console.log('END [viewData]');
}

saveXMLDataCallback = function()
{
    console.log('BEGIN [saveXMLData]');

    window.location = "/curate/view-data"

    console.log('END [saveXMLData]');
}

generateXMLString = function(elementObj)
{
//    console.log('BEGIN [generateXMLString]');

    var xmlString="";

    var children = elementObj.childNodes;
    for(var i = 0; i < children.length; i++) {
	console.log(children[i].tagName);
	if (children[i].nodeType == 1 && children[i].hasAttribute("xmlID")) {
	    if (children[i].getAttribute("xmlID") == "root") {
		if (children[i].hasAttribute("hdf5ns")) {
		    xmlString += "<" + children[i].firstChild.innerHTML.trim() + " xmlns:hdf5=\"http://hdfgroup.org/HDF5/XML/schema/HDF5-File\">"
		    xmlString += generateXMLString(children[i]);
		    xmlString += "</" + children[i].firstChild.innerHTML.trim() + ">"
		} else {
		    xmlString += "<" + children[i].firstChild.innerHTML.trim() + ">"
		    xmlString += generateXMLString(children[i]);
		    xmlString += "</" + children[i].firstChild.innerHTML.trim() + ">"
		}
	    }
	} else if (children[i].tagName == "UL") {
	    if (children[i].style.display != "none") {
		xmlString += generateXMLString(children[i]);
	    }
	} else if (children[i].tagName == "LI") {
	    console.log(children[i].innerHTML);
	    var nobrNode1 = children[i].children[0];
	    var nobrNode2 = children[i].children[1];
	    if (nobrNode1.firstChild != null) {
		console.log(nobrNode1.firstChild.tagName);
		if (nobrNode1.firstChild.tagName == "DIV") {
		    console.log("hdf5file matched");
		    xmlString += hdf5String;
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
	} else if (children[i].tagName == "SELECT") {
	    // get the index of the selected option 
//	    var idx = children[i].selectedIndex; 
	    // get the value of the selected option 
//	    var which = children[i].options[idx].value; 
//	    xmlString += "<" + which + ">";
//	    xmlString += generateXMLString(children[i]);
//	    xmlString += "</" + which + ">";
	} else if (children[i].tagName == "INPUT") {
	    xmlString += children[i].value;
	} else if (children[i].nodeType == 1 && children[i].getAttribute("id") == "elementSelected") {
	    var ptArray = children[i].innerHTML.split(" ");
	    xmlString += ptArray[ptArray.length - 1];
	} else {
	    xmlString += generateXMLString(children[i]);
	}
    }
    
//    console.log('END [generateXMLString]');

    return xmlString
}

function formatXml(xml) {
    var formatted = '';
    var reg = /(>)(<)(\/*)/g;
    xml = xml.replace(reg, '$1\r\n$2$3');
    var pad = 0;
    jQuery.each(xml.split('\r\n'), function(index, node) {
        var indent = 0;
        if (node.match( /.+<\/\w[^>]*>$/ )) {
            indent = 0;
        } else if (node.match( /^<\/\w/ )) {
            if (pad != 0) {
                pad -= 1;
            }
        } else if (node.match( /^<\w[^>]*[^\/]>.*$/ )) {
            indent = 1;
        } else {
            indent = 0;
        }
 
        var padding = '';
        for (var i = 0; i < pad; i++) {
            padding += '  ';
        }
 
        formatted += padding + node + '\r\n';
        pad += indent;
    });
 
    return formatted;
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

selectElement = function(periodicTableElement,divElement)
{
    console.log('BEGIN [selectElement(' + periodicTableElement + ',' + divElement + ')]');

    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>" + periodicTableElement + "</b>";

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
	
    console.log('END [selectElement]');
}

selectHDF5File = function(hdf5File,divElement)
{
    console.log('BEGIN [selectHDF5File(' + hdf5File + ',' + divElement + ')]');

    document.getElementById('hdf5File').innerHTML = hdf5File;

    $(function() {
        $("#dialog-select-hdf5file" ).dialog({
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

doSelectHDF5File = function(divElement)
{
    console.log('BEGIN [doSelectHDF5File(' + divElement + ')]');

    Dajaxice.curate.getHDF5String(getHDF5StringCallback);

//    var fileObj = document.getElementById('yourinputname').files[0];
//    document.getElementById('hdf5File').innerHTML = fileObj.name;

//    if (fileObj) {
//      var r = new FileReader();
//      r.onload = function(e) { 
//	  var contents = e.target.result;
//	  Dajaxice.curate.getHDF5String(getHDF5StringCallback,{'hdf5FileContents':contents});
//      }
//      r.readAsText(fileObj);
//    } else { 
//      alert("Failed to load file");
//    }

    console.log('END [doSelectHDF5File(' + divElement + ')]');
}

getHDF5StringCallback = function(data)
{
    console.log('BEGIN [getHDF5StringCallback(' + data + ')]');

    hdf5String = data.hdf5String;
    var rootElement = document.getElementsByName("xsdForm")[0];
    rootElement.childNodes[0].setAttribute("hdf5ns", "http://hdfgroup.org/HDF5/XML/schema/HDF5-File");
    console.log(rootElement.parentNode.innerHTML);

    console.log('END [getHDF5StringCallback(' + data + ')]');
}

chooseElement = function(element)
{
    console.log('BEGIN [chooseElement(' + element + ')]');

    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b id=\"selectedElement\">" + element + "</b>";

    console.log('END [chooseElement(' + element + ')]');
}

doSelectElement = function(divElement)
{
    console.log('BEGIN [chooseElement(' + divElement + ')]');

    var selectedElement = document.getElementById('selectedElement').innerHTML;
    divElement.onclick = function onclick(event) { selectElement(selectedElement,this); }
    divElement.parentNode.childNodes[2].innerHTML = "Current Selection: " + selectedElement;

    // reset for next selection
    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>None</b>";

    console.log('END [chooseElement(' + divElement + ')]');
}

changeChoice = function(selectObj)
{
    console.log('BEGIN [changeChoice(' + selectObj + ')]');

    // get the index of the selected option 
    var idx = selectObj.selectedIndex; 
    // get the value of the selected option 
    var which = selectObj.options[idx].value; 

    for (i=0; i < selectObj.options.length;i++) {
	console.log(selectObj.options[i].value);
	if (selectObj.options[i].value == selectObj.options[idx].value) {
	    document.getElementById(selectObj.options[i].value).style.display = "";
	} else {
	    document.getElementById(selectObj.options[i].value).style.display = "none";
	}
    }

    console.log('END [changeChoice(' + selectObj + ')]');
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
    $('.btn.select-element').on('click', selectElement);

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

    Dajaxice.curate.saveXMLDataToDB(downloadXMLCallback,{'saveAs':"xml2download"});

    console.log('END [downloadXML]');
}

downloadXMLCallback = function() 
{    
    console.log('BEGIN [downloadXMLCallabck]');

    window.location = '/curate/view-data/download-XML';
    
    console.log('END [downloadXMLCallback]');
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

    Dajaxice.curate.saveXMLDataToDB(saveXMLDataToDBCallback,{'saveAs':document.getElementById('saveAsInput').value});

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
	
    console.log('END [doSaveToRepository]');
}

saveXMLDataToDBCallback = function()
{
    console.log('BEGIN [doSaveXMLDataToDBCallback]');


    console.log('END [doSaveXMLDataToDBCallback]');
}


changeXMLSchema = function(operation,xpath,name)
{
    console.log('BEGIN [changeXMLSchema]');
    Dajaxice.curate.changeXMLSchema(changeXMLSchemaCallback,{'operation':operation,'xpath':xpath,'name':name});

    console.log('END [changeXMlSchema]');

    return false;
}

changeHTMLForm = function(operation,selectObj)
{
    console.log('BEGIN [changeHTMLForm(' + operation + ',' + selectObj + ']');

    if (operation == 'add') {
	var nodeToAdd = selectObj.parentNode.parentNode;
	var parentNode = nodeToAdd.parentNode;

	console.log("operation: add");
	console.log(selectObj.parentNode);
	console.log("occurs: " + parentNode.getAttribute("occurs"));

	if (parentNode.getAttribute("occurs") == "0") {
	    inputElements = nodeToAdd.getElementsByTagName('input');
	    for (var i=0;i<inputElements.length;i++) {
		inputElements[i].disabled = false;
	    }
	    parentNode.setAttribute("occurs", (parseInt(parentNode.getAttribute("occurs")) + 1).toString());
	    spanElements = nodeToAdd.getElementsByClassName('icon remove');
	    for (var i=0;i<spanElements.length;i++) {
		spanElements[i].style.display = "";
	    }
	    spanElements = nodeToAdd.getElementsByClassName('icon add');
	    for (var i=0;i<spanElements.length;i++) {
		spanElements[i].style.display = "none";
	    }
	} else if (parentNode.getAttribute("occurs") == "1") {
	    selectObj.parentNode.getElementsByClassName("icon remove")[0].style.display = "";

	    newNode = nodeToAdd.cloneNode(true);
	    parentNode.appendChild(newNode);
	    parentNode.setAttribute("occurs", (parseInt(parentNode.getAttribute("occurs")) + 1).toString());
	} else if (parentNode.getAttribute("occurs") == parentNode.getAttribute("minOccurs")) {
	    selectObj.parentNode.getElementsByClassName("icon remove")[0].style.display = "";

	    newNode = nodeToAdd.cloneNode(true);
	    parentNode.appendChild(newNode);
	    parentNode.setAttribute("occurs", (parseInt(parentNode.getAttribute("occurs")) + 1).toString());
	    for (var j=0;j<parentNode.childNodes.length;j++) {
		console.log("var j: " + j);
		console.log("length: " + parentNode.childNodes.length);
//		console.log(parentNode.innerHTML);
		console.log(parentNode.childNodes[j].innerHTML);
		spanElements = parentNode.childNodes[j].getElementsByClassName('icon remove');
		for (var i=0;i<0;i++) {
		    console.log("var : " + i);
		    console.log(spanElements[i].parentNode.innerHTML);
		    spanElements[i].style.display = "";
		}
	    }
	} else {
	    newNode = nodeToAdd.cloneNode(true);
	    parentNode.appendChild(newNode);
	    parentNode.setAttribute("occurs", (parseInt(parentNode.getAttribute("occurs")) + 1).toString());
	}
    } else if (operation == 'remove') {
	var nodeToRemove = selectObj.parentNode.parentNode;
	var parentNode = nodeToRemove.parentNode;
	
	console.log("operation: remove");
	console.log("nodeToRemove: " + nodeToRemove.innerHTML);
	console.log("parentNode: " + parentNode.innerHTML);
//	console.log(parentNode.childNodes.length);
	console.log("occurs: " + parentNode.getAttribute("occurs"));

	if (parentNode.getAttribute("occurs") == "0") {
	    nodeToRemove.disabled = true;
	} else if (parentNode.getAttribute("occurs") == "1") {
	    inputElements = nodeToRemove.getElementsByTagName('input');
	    for (var i=0;i<inputElements.length;i++) {
		inputElements[i].disabled = true;
	    }
	    parentNode.setAttribute("occurs", (parseInt(parentNode.getAttribute("occurs")) - 1).toString());
	    spanElements = nodeToRemove.getElementsByClassName('icon remove');
	    for (var i=0;i<spanElements.length;i++) {
		spanElements[i].style.display = "none";
	    }
	    spanElements = nodeToRemove.getElementsByClassName('icon add');
	    for (var i=0;i<spanElements.length;i++) {
		spanElements[i].style.display = "";
	    }
	} else if (parentNode.getAttribute("occurs") == "2") {
	    parentNode.getElementsByClassName("icon remove")[0].style.display = "none";
	    parentNode.getElementsByClassName("icon remove")[1].style.display = "none";

	    parentNode.removeChild(nodeToRemove);
	    parentNode.setAttribute("occurs", (parseInt(parentNode.getAttribute("occurs")) - 1).toString());
	} else {
	    parentNode.removeChild(nodeToRemove);
	    parentNode.setAttribute("occurs", (parseInt(parentNode.getAttribute("occurs")) - 1).toString());
	}
    }
    
    console.log('END [changeHTMLForm(' + operation + ',' + selectObj + ']');

    return false;
}

changeXMLSchemaCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [changeXMLSchemaCallback]');
    console.log('data passed back to callback function: ' + data);

    // business logic goes here

    console.log('END [changeXMlSchemaCallback]');

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

//        Dajaxice.curate.setCurrentTemplate(setCurrentTemplateCallback(templateName,tdElement),{'templateName':templateName});
//        Dajaxice.curate.setCurrentTemplate(Dajax.process,{'templateFilename':templateFilename});
        Dajaxice.curate.setCurrentTemplate(setCurrentTemplateCallback,{'templateFilename':templateFilename,'templateID':templateID});
//        tdElement.html('<span style="color:green;font-weight:bold">Current template</span>');
        

//        Dajaxice.curate.setCurrentTemplate(setCurrentTemplateCallback(),{'templateName':templateName,'notifElement':tdElement.serializeObject()});
//        Dajaxice.curate.setCurrentTemplate(Dajax.process);
	
//	$.ajax({
//        url: '/static/inc/controllers/php/schemaLoader.php',
//        type: 'GET',
//        success: function(data) {
//      		/* Generate additional trees for the form */
//        	generateTrees(tdElement);
//        	console.log('[setCurrentTemplate] '+templateName+' loaded');
//        },
//        error: function() {
//            console.error("[setCurrentTemplate] A problem occured during template loading");
//        },
//        // Form data
//        data: 'n='+templateName,
//        //Options to tell JQuery not to process data or worry about content-type
//        cache: false,
//        contentType: false,
//        processData: false
//    });

    return false;
}


setExploreCurrentTemplate = function()
{
    var templateName = $(this).parent().parent().children(':first').text();
    var templateFilename = $(this).parent().parent().children(':nth-child(2)').text();
    var tdElement = $(this).parent();
		
    tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
    $('.btn.set-template').off('click');
    
    console.log('[setExploreCurrentTemplate] Setting '+templateName+' with filename '+templateFilename+' as current template...');

    Dajaxice.explore.setCurrentTemplate(setCurrentTemplateCallback,{'templateFilename':templateFilename});

    return false;
}


setCurrentTemplateCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [setCurrentTemplateCallback]');
    console.log('data passed back to callback function: ' + data);
//    location.reload();

//    var messageLocation = $("#main").children(":first");
//    messageLocation.hide().html("Template Successfully Selected").fadeIn(500);
//    messageLocation.delay(2000).fadeOut(500);

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
