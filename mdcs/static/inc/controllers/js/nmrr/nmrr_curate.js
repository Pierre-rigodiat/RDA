/**
 * Get validation errors before submitting the form
 */
validate_form = function(){
    console.log('BEGIN [validate_form]');
    
    errors = []
    
    // get errors    
    $(".error_nmrr").each(function(){
    	// not in removed parts of the form
    	if (! $(this).closest("li").hasClass("removed")){
    		errors.push($(this));
    	}
    });
    
    
    if (errors.length == 0){
    	// save values in the form
        $("input:text").each(function(){
    	    $(this).attr("value", $(this).val());
    	});
    	$('select option').each(function(){ this.defaultSelected = this.selected; });
    	$("input:checkbox:not(:checked)").each(function(){
    	    
    	    $(this).removeAttr("checked");
    	});
    	$("input:checkbox:checked").each(function(){
        
    	    $(this).attr("checked", true);
    	});
    	validateXML();
    }else{
    	var errors_nmrr = "<ul>"    		
		$(errors).each(function(){
			errors_nmrr += "<li>" + $(this).text() + "</li>";
		});
    	errors_nmrr += "</ul>"
    	$("#validation_errors").html(errors_nmrr);
    	$(function() {
    	    $( "#form_validation" ).dialog({
    	      modal: true,
    	      buttons: {
    	        OK: function() {
    	          $( this ).dialog( "close" );
    	          $("#validation_errors").html("");
    	        },
    	      }
    	    });
    	  });	
    }
    console.log('END [validate_form]');
}



editForm = function(){
	if (document.referrer.indexOf('&useForm=true')){
		window.location = document.referrer;
	}else{
		window.location = document.referrer + '&useForm=true';
	}
}

