/**
 * 
 * File Name: data_exploration.js
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
 * Load controllers for the template selection
 */
loadTemplateSelectionControllers = function()
{
    console.log('BEGIN [loadTemplateSelectionControllers]');
    $('.btn.set-explore-template').on('click', setExploreCurrentTemplate);
    $('.btn.set-explore-user-template').on('click', setExploreCurrentUserTemplate);
    Dajaxice.explore.redirectExploreTabs(Dajax.process);
    console.log('END [loadTemplateSelectionControllers]');
}

/**
 * set the current template
 * @returns {Boolean}
 */
setExploreCurrentTemplate = function()
{
    var templateName = $(this).parent().parent().children(':first').text();
    var templateID = $(this).parent().parent().children(':first').attr('templateID');
    var templateFilename = $(this).parent().parent().children(':nth-child(2)').text();
    var tdElement = $(this).parent();
		
    tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
    $('.btn.set-template').off('click');
    
    console.log('[setExploreCurrentTemplate] Setting '+templateName+' with filename '+templateFilename+' as current template...');

    Dajaxice.explore.setCurrentTemplate(setCurrentTemplateCallback,{'templateFilename':templateFilename, 'templateID':templateID});

    return false;
}

/**
 * set the current user template
 * @returns {Boolean}
 */
setExploreCurrentUserTemplate = function()
{
    var templateName = $(this).parent().parent().children(':first').text();
    var templateID = $(this).parent().parent().children(':first').attr('templateID');
    var tdElement = $(this).parent();
		
    tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
    $('.btn.set-template').off('click');

    Dajaxice.explore.setCurrentUserTemplate(setCurrentTemplateCallback,{'templateID':templateID});

    return false;
}

/**
 * Set template Callback. Updates the template display.
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

/**
 * Shows a dialog when the template is selected
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
 * When an element is selected in the query builder, input fields are added to the form regarding the type of the element.
 * @param fromElementID
 * @param criteriaID
 */
function updateUserInputs(fromElementID, criteriaID){
	$("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var html = $("#queryForm").html();
	Dajaxice.explore.updateUserInputs(Dajax.process,{'htmlForm':html, 'fromElementID':fromElementID, 'criteriaID':criteriaID});
}

/**
 * Submit a query
 */
function query(){
	$("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var queryForm = $("#queryForm").html()
	var queryBuilder = $("#queryBuilder").html()
	
	var elems = $("#fed_of_queries_instances")[0].getElementsByTagName("input");
    for(var i = 0; i < elems.length; i++) {
    	if(elems[i].checked == true)
    	{
    		elems[i].setAttribute("checked","checked");
    	}else
    	{
    		elems[i].removeAttribute('checked');
    	}
    }
	var fedOfQueries = $("#fed_of_queries_instances").html()
	
	Dajaxice.explore.executeQuery(Dajax.process,{'queryForm':queryForm, 'queryBuilder':queryBuilder, "fedOfQueries": fedOfQueries});
}

/**
 * Redirect to results page
 */
resultsCallback = function()
{
	console.log('BEGIN [resultsCallback]');

    window.location = "/explore/results"
    	
    console.log('END [resultsCallback]');
}

/**
 * Get results asynchronously (disabled)
 * @param nbInstances
 */
getAsyncResults = function(nbInstances)
{
	/*for (i=0; i < Number(nbInstances); ++i){
		Dajaxice.explore.getResultsByInstance(Dajax.process,{"numInstance": i});		
	}*/
	Dajaxice.explore.getResultsByInstance(Dajax.process,{"numInstance": nbInstances});
}

/**
 * Get SPARQL results asynchronously (disabled)
 * @param nbInstances
 */
getAsyncSparqlResults = function(nbInstances)
{
	/*for (i=0; i < Number(nbInstances); ++i){
		Dajaxice.explore.getSparqlResultsByInstance(Dajax.process,{"numInstance": i});
	}*/
	Dajaxice.explore.getSparqlResultsByInstance(Dajax.process,{"numInstance": nbInstances});
}

/**
 * Add an empty field to the query builder
 */
function addField(){
	$("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var html = $("#queryForm").html()
	Dajaxice.explore.addField(Dajax.process,{'htmlForm':html});
}

/**
 * Remove a field from the query builder
 * @param tagID
 */
function removeField(tagID){
	$("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var queryForm = $("#queryForm").html()
	Dajaxice.explore.removeField(Dajax.process,{'queryForm':queryForm, 'criteriaID':tagID});
}

/**
 * Save the current query
 */
function saveQuery(){
	$("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var queryForm = $("#queryForm").html()
	var queriesTable = $("#queriesTable").html()	
	Dajaxice.explore.saveQuery(Dajax.process,{'queryForm':queryForm, 'queriesTable':queriesTable});
}

/**
 * Insert a saved query in the query builder
 * @param savedQueryID
 */
function addSavedQueryToForm(savedQueryID){
	$("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var queryForm = $("#queryForm").html()
	Dajaxice.explore.addSavedQueryToForm(Dajax.process,{'queryForm':queryForm, 'savedQueryID':savedQueryID})
} 

/**
 * Delete a save query
 * @param savedQueryID
 */
function deleteQuery(savedQueryID){
	$(function() {
        $( "#dialog-DeleteQuery" ).dialog({
            modal: true,
            buttons: {		
            	Delete: function(){
		        	Dajaxice.explore.deleteQuery(Dajax.process,{'savedQueryID':savedQueryID})
		        	$( this ).dialog( "close" );
        		},
        		Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}

/**
 * Clear the current criterias
 */
function clearCriterias(){
	$("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var queryForm = $("#queryForm").html()
	Dajaxice.explore.clearCriterias(Dajax.process, {'queryForm':queryForm})
}

/**
 * Delete all saved queries 
 */
clearQueries = function()
{
	$(function() {
        $( "#dialog-DeleteAllQueries" ).dialog({
            modal: true,
            buttons: {		
        		Delete: function(){
		        	$("input").each(function(){
		        	    $(this).attr("value", $(this).val());
		        	});
		        	$('select option').each(function(){ this.defaultSelected = this.selected; });
		        	Dajaxice.explore.clearQueries(Dajax.process)
		        	$( this ).dialog( "close" );
        		},
        		Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}

/**
 * Save the custom form
 */
exploreData = function()
{
    console.log('BEGIN [exploreData]');


    // Need to Set input values explicitiy before sending innerHTML for save
    var elems = document.getElementsByName("xsdForm")[0].getElementsByTagName("input");
    for(var i = 0; i < elems.length; i++) {
    	// sent attribute to property value
    	elems[i].setAttribute("value", elems[i].checked);
    	if(elems[i].checked == true)
    	{
    		elems[i].setAttribute("checked","checked");
    	}
    }
    $('select option').each(function(){ this.defaultSelected = this.selected; }); 
    Dajaxice.explore.saveCustomData(saveCustomXMLDataCallback,{'formContent':document.getElementById('xsdForm').innerHTML});

    console.log('END [exploreData]');
}

/**
 * Redirect to Perform Search
 */
saveCustomXMLDataCallback = function()
{
    console.log('BEGIN [saveCustomXMLData]');

    window.location = "/explore/perform-search"
    	
    console.log('END [saveCustomXMLData]');
}

/**
 * Change a choice in the XSD form
 * @param selectObj
 */
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

/**
 * Check that a template is selected
 */
verifyTemplateIsSelectedCustomize = function(){
    console.log('BEGIN [verifyTemplateIsSelected]');

    Dajaxice.explore.verifyTemplateIsSelected(verifyTemplateIsSelectedCustomizeCallback); 

    console.log('END [verifyTemplateIsSelected]');
}

/**
 * Callback of check template selected. Display an error message if not selected.
 * @param data
 */
verifyTemplateIsSelectedCustomizeCallback = function(data)
{
    console.log('BEGIN [verifyTemplateIsSelectedCallback]');

    if (data.templateSelected == 'no') {
        location.href = "/explore";
    }else{
    	loadExploreCurrentTemplateForm();
    }

    console.log('END [verifyTemplateIsSelectedCallback]');
}

/**
 * Generate a form to select fields to use in the query builder
 */
loadExploreCurrentTemplateForm = function()
{
    console.log('BEGIN [loadExploreCurrentTemplateForm]');

    $('.btn.clear-fields').on('click', clearFields);

    Dajaxice.explore.generateXSDTreeForQueryingData(Dajax.process); 

    console.log('END [loadExploreCurrentTemplateForm]');
}

/**
 * Clear all check boxes of the form
 */
clearFields = function()
{
    console.log('BEGIN [clearFields]');

    // reset all select to their 0 index
    $('#dataQueryForm').find("select").each(function(){
	  this.selectedIndex = 0;
	  for (i=0; i < this.options.length;i++) {
	    if (i == 0){
	    		$("#" + this.id + "-" + i).removeAttr("style");
			} else {
	        $("#" + this.id + "-" + i).attr("style","display:none");
			}
	    	
	    }
	});
    // clear all checkboxes
    $("#dataQueryForm").find("input").each(function() {
    	$( this ).removeAttr('checked');
    });
    // display a message
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

/**
 * Download all results
 */
downloadResults = function()
{
	console.log('BEGIN [downloadResults]');
		
	Dajaxice.explore.downloadResults(Dajax.process);
	
	console.log('END [downloadResults]');
}

/**
 * Display errors
 */
displayErrors = function()
{
	$(function() {
        $( "#dialog-errors-message" ).dialog({
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
 * Comes back to the query, keeping the current criterias
 */
backToQuery = function()
{
	console.log('BEGIN [backToQuery]');
	
	Dajaxice.explore.backToQuery(backToQueryCallback);
	
	console.log('END [backToQuery]');
}

/**
 * Redirect to Perform Search
 */
backToQueryCallback = function()
{
    console.log('BEGIN [backToQueryCallback]');

    window.location = "/explore/perform-search"    	
   
    console.log('END [backToQueryCallback]');
}

/**
 * Manage the display of the tabs
 */
switchTabRefresh = function()
{
	console.log('BEGIN [switchTabRefresh]');
	
	var tab = $("#explore-tabs").find("input:radio:checked").attr("id");	
	
	if (tab == null){
		$("#tab-1").prop("checked",true);
		tab = "tab-1"
	}
	switchTab(tab);
	
	console.log('END [switchTabRefresh]');
}

/**
 * Manage the display of the tabs
 */
switchTab = function(tab)
{
	console.log('BEGIN [switchTab]');
	
	//var tab = $("#explore-tabs").find("input:radio:checked").attr("id")
	
	$("#subnav-wrapper .tabbed").attr("style","display:none;");
	$("#subnav-"+tab).removeAttr("style");
	
	if (tab == "tab-1"){
		$("#queryBuilder").removeAttr("style");
		$("#customForm").removeAttr("style");
		$("#QbEDesc").removeAttr("style");
		$("#SPARQLqueryBuilder").attr("style","display:none;");		
		$("#SPARQLDesc").attr("style","display:none;");	
	}else{
		$("#queryBuilder").attr("style","display:none;");
		$("#customForm").attr("style","display:none;");
		$("#QbEDesc").attr("style","display:none;");
		$("#SPARQLqueryBuilder").removeAttr("style");
		$("#SPARQLDesc").removeAttr("style");	
	}
	Dajaxice.explore.switchExploreTab(Dajax.process,{"tab":tab});
	
	console.log('END [switchTab]');
}

/**
 * Manage the display of the tabs
 */
redirectExplore = function(tab)
{
	console.log('BEGIN [redirectExplore]');
	
	//window.location = "/explore";
	Dajaxice.explore.redirectExplore(Dajax.process);
	
	console.log('END [redirectExplore]');
}

/**
 * Manage the display of the tabs
 */
redirectSPARQLTab = function()
{
	console.log('BEGIN [redirectSPARQLTab]');
	
	$("#explore-tabs").find("input:radio").removeAttr('checked');
	$("#tab-2").prop("checked",true);
	switchTabRefresh();
	
	console.log('END [redirectSPARQLTab]');
}

/**
 * Show the custom tree to choose a field for the query builder
 * @param criteriaID
 */
showCustomTree = function(criteriaID)
{
	console.log('BEGIN [showCustomTree]');
	
	Dajaxice.explore.setCurrentCriteria(Dajax.process,{"currentCriteriaID":criteriaID});
	
	$(function() {
        $( "#dialog-customTree" ).dialog({
            modal: true,
            width: 500,
            height: 620,
            buttons: {
		Close: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
	console.log('END [showCustomTree]');
}

/**
 * Select an element to insert in the query builder
 * @param elementID
 */
selectElement = function(elementID)
{
	console.log('BEGIN [selectElement]');
		
	var elementName = $("#" + elementID).text().trim();
	Dajaxice.explore.selectElement(Dajax.process, {"elementID":elementID, "elementName":elementName});
	
	console.log('END [selectElement]');
}

/**
 * Submit a SPARQL query
 */
function sparqlquery(){
	var queryStr = $("#SPARQLqueryBuilder .SPARQLTextArea").val();	
	var sparqlFormatIndex = $("#SPARQLFormat").prop("selectedIndex");
	var elems = $("#fed_of_queries_instances")[0].getElementsByTagName("input");
    for(var i = 0; i < elems.length; i++) {
    	if(elems[i].checked == true)
    	{
    		elems[i].setAttribute("checked","checked");
    	}else
    	{
    		elems[i].removeAttribute('checked');
    	}
    }
	var fedOfQueries = $("#fed_of_queries_instances").html()
	Dajaxice.explore.executeSPARQLQuery(Dajax.process,{"queryStr":queryStr,"sparqlFormatIndex":sparqlFormatIndex, "fedOfQueries": fedOfQueries});
}

/**
 * Redirect to SPARQL results
 */
sparqlResultsCallback = function()
{
	console.log('BEGIN [sparqlResultsCallback]');

    window.location = "/explore/sparqlresults"
    	
    console.log('END [sparqlResultsCallback]');
}

/**
 * Download SPARQL results
 */
downloadSparqlResults = function()
{
	console.log('BEGIN [downloadSparqlResults]');
	
	Dajaxice.explore.downloadSparqlResults(Dajax.process);
	
	console.log('END [downloadSparqlResults]');
}

/**
 * Get the path to an element to use in a SPARQL query
 */
getElementPath = function()
{
	console.log('BEGIN [getElementPath]');
	
	$(function() {
        $( "#dialog-sparqlcustomTree" ).dialog({
            modal: true,
            width: 510,
            height: 660,
            buttons: {
		Close: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
	
	console.log('END [getElementPath]');
}

/**
 * Select an element from the custom tree, for subelement query
 * @param leavesID
 */
selectParent = function(leavesID)
{
	console.log('BEGIN [selectParent]');
	
	try{
		$("#dialog-customTree").dialog("close"); 
		subElementQuery(leavesID);
	}catch(err)
	{
		
	}
	console.log('END [selectParent]');
}

/**
 * Open the dialog to create a query on subelements of the same document
 * @param leavesID
 */
subElementQuery = function(leavesID)
{
	console.log('BEGIN [subElementQuery]');
	$(function() {
        $( "#dialog-subElementQuery" ).dialog({
            modal: true,
            width: 670,
            height: 420,
            buttons: {
		Close: function() {
                    $( this ).dialog( "close" );
                },
        Insert: function(){
        			var checkboxes = $("#subElementQueryBuilder").find("input:checkbox");
        			for(var i = 0; i < checkboxes.length; i++) {
        				checkboxes[i].setAttribute("value", checkboxes[i].checked);
        		    	if(checkboxes[i].checked == true)
        		    	{
        		    		checkboxes[i].setAttribute("checked","checked");
        		    	}
        		    }
        			$("input").each(function(){
        			    $(this).attr("value", $(this).val());
        			});
        			$('select option').each(function(){ this.defaultSelected = this.selected; });
        			var form = $("#subElementQueryBuilder").html();
        			Dajaxice.explore.insertSubElementQuery(Dajax.process,{"leavesID":leavesID, "form":form});
        		}
            }
        });
    });
	
	Dajaxice.explore.prepareSubElementQuery(Dajax.process,{"leavesID":leavesID});
	console.log('END [subElementQuery]');
}

/**
 * Show an error message when no repository are selected
 */
showErrorInstancesDialog = function()
{
	$(function() {
        $( "#dialog-Instances" ).dialog({
            modal: true,
            buttons: {
            	OK: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}
