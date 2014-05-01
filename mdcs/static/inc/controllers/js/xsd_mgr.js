/**
 * 
 */
loadXsdManagerHandler = function()
{
    console.log('BEGIN [loadXsdManagerHandler]');
    $('.add').on('click', setCurrentModel);
    $('.delete.schema').on('click', deleteSchema);
    $('.copy.schema').on('click', copySchema);
    $('.upload.schema').on('click', uploadSchema);
    $('.delete.ontology').on('click', deleteOntology);
    $('.copy.ontology').on('click', copyOntology);
    $('.upload.ontology').on('click', uploadOntology);
    console.log('END [loadXsdManagerHandler]');
}

/**
 * 
 */
displayModelSelectedDialog = function()
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
 * 
 */
setCurrentModel = function()
{
    console.log('BEGIN [setCurrentModel]');
    var modelName = $(this).parent().siblings(':first').text();
    var modelFilename = $(this).parent().siblings(':nth-child(2)').text();
    var tdElement = $(this).parent();
	
    $('.add').off('click');
		
    tdElement.html('<img src="/static/resources/img/ajax-loader.gif" alt="Loading..."/>');
		
    console.log('[setCurrentModel] Loading '+modelName+' with filename '+modelFilename+' as current model...');

    Dajaxice.curate.setCurrentModel(setCurrentModelCallback,{'modelFilename':modelFilename});
	
//    $.ajax({
//        url: 'inc/controllers/php/schemaLoader.php',
//        type: 'GET',
//        success: function(data) {
//        	// Refresh the page
//        	loadPage($(location).attr('href')+'?manageSchemas');
//        	console.log('[setCurrentModel] '+modelName+' loaded');
//        },
//        error: function() {
//            console.error("[setCurrentModel] A problem occured during schema loading");
//        },
//        // Form data
//        data: 'n='+modelName,
//        //Options to tell JQuery not to process data or worry about content-type
//        cache: false,
//        contentType: false,
//        processData: false
//    });

    console.log('END [setCurrentModel]');
}

setCurrentModelCallback = function(data)
{
    Dajax.process(data);
    console.log('BEGIN [setCurrentModelCallback]');
//    location.reload();

//    var messageLocation = $("#main").children(":first");
//    messageLocation.hide().html("Template Successfully Selected").fadeIn(500);
//    messageLocation.delay(2000).fadeOut(500);

    $('#model_selection').load(document.URL +  ' #model_selection', function() {
	loadXsdManagerHandler();
	//displayModelSelectedDialog();
    });
    console.log('END [setCurrentModelCallback]');
}

/**
 * 
 */
deleteSchema = function()
{
    console.log('BEGIN [deleteSchema]');
    var schemaName = $(this).parent().siblings(':first').text();
    var schemaFilename = $(this).parent().siblings(':nth-child(2)').text();
    var schemaID = $(this).attr("schemaid");

    document.getElementById("schema-to-delete").innerHTML = schemaName;

    $(function() {
        $( "#dialog-deleteconfirm-message" ).dialog({
            modal: true,
            buttons: {
		Yes: function() {
                    deleteSchemaConfirmed(schemaID);
                    $( this ).dialog( "close" );
                },
		No: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [deleteSchema]');
}

/**
 * 
 */
deleteSchemaConfirmed = function(schemaID)
{
    console.log('BEGIN [deleteSchemaConfirmed('+schemaID+')]');

    Dajaxice.curate.deleteXMLSchema(deleteSchemaCallback,{'xmlSchemaID':schemaID});

    console.log('END [deleteSchemaConfirmed('+schemaID+')]');
}

/**
 * 
 */
deleteSchemaCallback = function(data)
{
    console.log('BEGIN [deleteSchemaCallback]');

    Dajax.process(data);

    $('#model_selection').load(document.URL +  ' #model_selection', function() {
	loadXsdManagerHandler();
    });

    console.log('END [deleteSchemaCallback]');
}

/**
 * 
 */
copySchema = function()
{
    console.log('BEGIN [copySchema]');

    $(function() {
        $( "#dialog-copied-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [copySchema]');
}

/**
 * 
 */
uploadSchema = function()
{
    console.log('BEGIN [uploadSchema]');

    document.getElementById('schema_name').value = ""
    document.getElementById('files').value = ""
    document.getElementById('list').innerHTML = ""
    document.getElementById('schemaNameErrorMessage').innerHTML = ""

    $(function() {
        $( "#dialog-upload-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                },
		Cancel: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [uploadSchema]');
}

/**
 * 
 */
deleteOntology = function()
{
    console.log('BEGIN [deleteOntology]');
    var ontologyName = $(this).parent().siblings(':first').text();
    var ontologyFilename = $(this).parent().siblings(':nth-child(2)').text();
    var ontologyID = $(this).attr("ontologyid");

    document.getElementById("ontology-to-delete").innerHTML = ontologyName;

    $(function() {
        $( "#dialog-deleteconfirm-message" ).dialog({
            modal: true,
            buttons: {
		Yes: function() {
                    deleteOntologyConfirmed(ontologyID);
                    $( this ).dialog( "close" );
                },
		No: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [deleteOntology]');
}

/**
 * 
 */
deleteOntologyConfirmed = function(ontologyID)
{
    console.log('BEGIN [deleteOntologyConfirmed('+ontologyID+')]');

    Dajaxice.curate.deleteXMLOntology(deleteOntologyCallback,{'xmlOntologyID':ontologyID});

    console.log('END [deleteOntologyConfirmed('+ontologyID+')]');
}

/**
 * 
 */
deleteOntologyCallback = function(data)
{
    console.log('BEGIN [deleteOntologyCallback]');

    Dajax.process(data);

    $('#model_selection').load(document.URL +  ' #model_selection', function() {
	loadXsdManagerHandler();
    });

    console.log('END [deleteOntologyCallback]');
}

/**
 * 
 */
copyOntology = function()
{
    console.log('BEGIN [copyOntology]');

    $(function() {
        $( "#dialog-copied-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [copyOntology]');
}

/**
 * 
 */
uploadOntology = function()
{
    console.log('BEGIN [uploadOntology]');

    document.getElementById('ontology_name').value = ""
    document.getElementById('files').value = ""
    document.getElementById('list').innerHTML = ""
    document.getElementById('ontologyNameErrorMessage').innerHTML = ""

    $(function() {
        $( "#dialog-upload-message" ).dialog({
            modal: true,
            buttons: {
		Ok: function() {
                    $( this ).dialog( "close" );
                },
		Cancel: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	
    console.log('END [uploadOntology]');
}

