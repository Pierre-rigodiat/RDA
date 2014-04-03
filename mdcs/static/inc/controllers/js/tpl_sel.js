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
        $( "#dialog-loaded-message" ).dialog({
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
        $( "#dialog-saved-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [saveForm]');
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

loadCurrentTemplateForm = function()
{
    console.log('BEGIN [loadCurrentTemplateForm]');

    $('.btn.clear-fields').on('click', clearFields);
    $('.btn.load-form').on('click', loadForm);
    $('.btn.save-form').on('click', saveForm);

    Dajaxice.curate.generateXSDTreeForEnteringData(Dajax.process); //,{'templateFilename':'xxxx'});

    console.log('END [loadCurrentTemplateForm]');
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


downloadXML = function()
{
    console.log('BEGIN [downloadXML]');

    console.log('[downloadXML] Downloading XML...');
    
    window.location = '/curate/view-data/download-XML';
    
    console.log('[downloadXML] XML downloaded');

/*
    $(function() {
        $( "#dialog-downloaded-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
*/
    console.log('END [downloadXML]');
}

saveToRepository = function()
{
    console.log('BEGIN [saveToRepository]');

    console.log('[saveToRepository] Saving XML...');

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

    console.log('[saveToRepository] XML saved');
    //console.error("[saveXml] A problem occured during the save");
	
    console.log('END [saveToRepository]');
}

changeXMLSchema = function(operation,xpath,name)
{
    console.log('BEGIN [changeXMLSchema]');
    Dajaxice.curate.changeXMLSchema(changeXMLSchemaCallback,{'operation':operation,'xpath':xpath,'name':name});

    console.log('END [changeXMlSchema]');

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
	var templateFilename = $(this).parent().parent().children(':nth-child(2)').text();
	var tdElement = $(this).parent();
		
	tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
	$('.btn.set-template').off('click');
	
	console.log('[setCurrentTemplate] Setting '+templateName+' with filename '+templateFilename+' as current template...');

//        Dajaxice.curate.setCurrentTemplate(setCurrentTemplateCallback(templateName,tdElement),{'templateName':templateName});
//        Dajaxice.curate.setCurrentTemplate(Dajax.process,{'templateFilename':templateFilename});
        Dajaxice.curate.setCurrentTemplate(setCurrentTemplateCallback,{'templateFilename':templateFilename});
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
