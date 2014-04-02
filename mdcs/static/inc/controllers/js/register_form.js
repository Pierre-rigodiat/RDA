/**
 * 
 */
loadRegisterFormController = function()
{
	var delay = 300;
	
	$(document).on('keyup', delayFunction(saveInSession, delay));
	$(document).on('change', 'select.xsdman.restriction', delayFunction(saveInSession, delay));
	
	removeRegisterFormController();
	
	/**
	 * Dialog basic configuration 
	 */
	$("#dialog").dialog({
        autoOpen: false,
        show: "blind",
        hide: "blind",
        height: 150,
        width: 300,
        modal: true,
        resizable: false,
        buttons: {
            "Load form": function() {
            	var formId = $('#form-id').val();
            	
            	loadForm(formId);
            		  		
            	$( this ).dialog("close");
            },
            Cancel: function() {
                $(this).dialog("close");
            }
        }
    });
	
	$('.btn.clear-fields').on('click', clearFields);
	$('.btn.load-form').on('click', loadFormDialog);
	$('.btn.save-form').on('click', saveInDB);
	
	$('.btn.edit').on('click', editField);
}

removeRegisterFormController = function()
{
	$('.blank').off('click');
	$('.load').off('click');
	$('.save').off('click');
	
	if($('#dialog').is(':ui-dialog')) $('#dialog').dialog("destroy");
}

delayFunction = function(func, delay)
{
	var timer = null;
	
    return function(){
        var context = this, 
        	args = arguments;
        
        clearTimeout(timer);
        timer = window.setTimeout(
        	function(){
            	func.apply(context, args);
        	},
        	delay
        );
    };
}

clearFields = function()
{
	console.log("[clearFields] Clearing fields");
	var inputs = $('input.text');
	
	inputs.each(function()
	{
		var inputId = $(this).parent().attr('id');
		
		if(!isNaN(parseInt(inputId)))
		{
			$(this).attr('value', '');
		}	
	});
	
	$.ajax({
        url: 'inc/controllers/php/manageData.php',
        type: 'GET',
        success: function(data) {
        	
        },
        error: function() {
            console.error("[clearFields] Problem with the AJAX call");
        },
        // Form data
        data: 'a=c',
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });

	console.log("[clearFields] Fields cleared");
}

loadFormDialog = function()
{
	$('#dialog').dialog('open');
}

loadForm = function(formId)
{
	var successMessage = '<div class="temp success"><span class="icon valid"></span>Form successfully loaded!</div>',
		errorMessage = '<div class="temp error"><span class="icon invalid"></span>An error occured during the save</div>',
		messageLocation = $("#main").children(":first");
	
	console.log('[loadForm] Loading form '+formId+'...');
	
	$.ajax({
        url: 'inc/controllers/php/manageData.php',
        type: 'GET',
        success: function(data) {
        	var jsonData = $.parseJSON(data);
        	
        	$(document).find('#page_content').html(htmlspecialchars_decode(jsonData.result));
        	
        	removeRegisterFormController();
        	loadRegisterFormController();
        	
        	messageLocation.hide().html(successMessage).fadeIn(500);
        	messageLocation.delay(2000).fadeOut(500);
        	
        	console.log("[loadForm] Form saved");
        },
        error: function() {
        	messageLocation.hide().html(errorMessage).fadeIn(500);
        	messageLocation.delay(2000).fadeOut(500);
        	
            console.error("[loadForm] Problem with the AJAX call");
        },
        // Form data
        data: 'a=l&id='+formId,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

saveInSession = function()
{
	console.log("[saveInSession] Saving fields...");
	
	var inputs = $('input.text'),
		selects = $('select.xsdman.restriction'),
		qString = '';
	
	inputs.each(function()
	{
		var inputId = $(this).parent().attr('id'),
			inputValue = $(this).attr('value');
		
		if(inputValue != '' && !isNaN(parseInt(inputId)))
		{
			console.log('[saveInSession] Id '+parseInt(inputId)+' = '+inputValue);
			qString += parseInt(inputId)+'='+inputValue+'&';
		}	
	});
	
	selects.each(function()
	{
		var selectId = $(this).parent().attr('id'),
			selectValue = $(this).attr('value');
			
		if(!isNaN(parseInt(selectId)))
		{
			console.log('[saveInSession] Id '+parseInt(selectId)+' = '+selectValue);
			qString += parseInt(selectId)+'='+selectValue+'&';
		}
	});
	
	qString = qString.substring(0, qString.length-1);
	
	$.ajax({
        url: 'inc/controllers/php/manageData.php',
        type: 'GET',
        success: function(data) {
        	console.log("[saveInSession] Form saved");
        },
        error: function() {
            console.error("[saveInSession] Problem with the AJAX call");
        },
        // Form data
        data: 'a=s&'+qString,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

saveInDB = function()
{
	var successMessage = '<div class="temp success"><span class="icon valid"></span>Form successfully saved!</div>',
		errorMessage = '<div class="temp error"><span class="icon invalid"></span>An error occured during the save</div>',
		messageLocation = $("#main").children(":first");
	
	console.log("[saveInDB] Saving into db...");
	
	saveInSession();
	
	$.ajax({
        url: 'inc/controllers/php/manageData.php',
        type: 'GET',
        success: function(data) {
        	messageLocation.hide().html(successMessage).fadeIn(500);
        	messageLocation.delay(2000).fadeOut(500);
        	
        	console.log("[saveInDB] Form saved");
        	
        },
        error: function() {
        	messageLocation.hide().html(errorMessage).fadeIn(500);
        	messageLocation.delay(2000).fadeOut(500);   
        	
            console.error("[saveInDB] Problem with the AJAX call");
        },
        // Form data
        data: 'a=d',
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

editField = function(event)
{
	event.preventDefault();
	
	var inputField = $(this).parent().children('input');
	
	if(inputField.attr('disabled'))
	{
		console.log('[editField] Edit mode ON');
	
		$(this).children(':first').attr('class', 'icon-ok')
		inputField.removeAttr('disabled');
	}
	else
	{
		console.log('[editField] Edit mode OFF');
		
		$(this).children(':first').attr('class', 'icon-edit')
		inputField.attr('disabled', 'disabled');
		
		$.ajax({
	        url: 'inc/controllers/php/change.php',
	        type: 'GET',
	        success: function(data) {
	        	console.log("[editField] Form saved");
	        },
	        error: function() {
	            console.error("[editField] Problem with the AJAX call");
	        },
	        // Form data
	        data: 'id='+inputField.attr('value'),
	        //Options to tell JQuery not to process data or worry about content-type
	        cache: false,
	        contentType: false,
	        processData: false
	    });
	}	
}
