/**
 * 
 * File Name: contact.js
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
 * Load controllers for contact
 */
loadContactControllers = function()
{
    console.log('BEGIN [loadContactControllers]');
    $('.btn.submit').on('click', submitMessage);
    console.log('END [loadContactControllers]');
}


/**
 * Submit message.
 */
submitMessage = function()
{
	console.log('BEGIN [submitMessage]');
    
	name = $("#id_sender_name").val();
	email = $("#id_sender_email").val();
	message = $("#id_sender_message").val();	
	
	errors = "";
	if (name == "" || email == "" || message == ""){
		errors += "Some fields are empty.<br/>";
	}else{
		if(!email.match(/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/)){
			errors += "The email address is not valid.<br/>"
		}
	}
	if (errors != ""){
		$("#contact-errors").html(errors);
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
	else{
		Dajaxice.admin.contact(submitMessageCallback,{"name":name, "email":email, "message":message});
	}

    console.log('END [submitMessage]');	
}

/**
 * Submit message Callback.
 */
submitMessageCallback = function() {
	$(function() {
	    $( "#dialog-sent-message" ).dialog({
	      modal: true,
	      buttons: {
	        Ok: function() {
	          $( this ).dialog( "close" );
	          window.location = "/";
	        }
	      }
	    });
	  });
}


/**
 * Load controllers for contact messages
 */
loadContactMessagesHandler = function(){
    console.log('BEGIN [loadContactMessagesHandler]');
    $('.remove.message').on('click', removeMessage);
    console.log('END [loadContactMessagesHandler]');
}

/**
 * Delete a message from the list
 */
removeMessage = function(){
	var messageid = $(this).attr("messageid");
	$(function() {
	    $( "#dialog-confirm-delete" ).dialog({
	      modal: true,
	      buttons: {
	        Yes: function() {
	          $( this ).dialog( "close" );
	          Dajaxice.admin.removeMessage(removeMessageCallback,{"messageid": messageid});
	        },
	        No:function() {
	         $( this ).dialog( "close" );
		    }
	      }
	    });
	  });	
}

/**
 * Delete message Callback
 */
removeMessageCallback = function(){
	$('#model_selection').load(document.URL +  ' #model_selection', function() {
        loadContactMessagesHandler();
    });
}
