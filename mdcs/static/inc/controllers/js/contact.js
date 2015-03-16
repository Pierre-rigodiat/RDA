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
