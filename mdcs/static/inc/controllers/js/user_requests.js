/**
 * 
 * File Name: user_requests.js
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
 * Load controllers to manage user requests
 */
loadUserRequestsHandler = function()
{
	console.log('BEGIN [loadUserRequestsHandler]');
	$('.accept.request').on('click',acceptRequest);
	$('.remove.request').on('click',denyRequest);
	console.log('END [loadUserRequestsHandler]');
}

/**
 * Accept a user request
 */
acceptRequest = function()
{
	var requestid = $(this).attr("requestid");
	Dajaxice.admin.acceptRequest(Dajax.process,{"requestid": requestid});
}

/**
 * Deny a user request
 */
denyRequest = function()
{
	var requestid = $(this).attr("requestid");
    $(function() {
        $( "#dialog-denied-request" ).dialog({
          modal: true,
          buttons: {
            Deny: function() {
              Dajaxice.admin.denyRequest(Dajax.process,{"requestid": requestid});
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
 * Display errors for user requests
 */
showErrorRequestDialog = function(){
	$(function() {
        $( "#dialog-error-request" ).dialog({
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
 * Display success message when user created
 */
showAcceptedRequestDialog = function(){
	$(function() {
        $( "#dialog-accepted-request" ).dialog({
          modal: true,
          buttons: {
            Ok: function() {
              $( this ).dialog( "close" );
            }
          }
        });
      });
      $('#model_selection').load(document.URL +  ' #model_selection', function() {
          loadUserRequestsHandler();
      });
}

