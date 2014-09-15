loadUserRequestsHandler = function()
{
	console.log('BEGIN [loadUserRequestsHandler]');
	$('.accept.request').on('click',acceptRequest);
	$('.remove.request').on('click',denyRequest);
	console.log('END [loadUserRequestsHandler]');
}


acceptRequest = function()
{
	var requestid = $(this).attr("requestid");
	Dajaxice.curate.acceptRequest(Dajax.process,{"requestid": requestid});
}

denyRequest = function()
{
	var requestid = $(this).attr("requestid");
    $(function() {
        $( "#dialog-denied-request" ).dialog({
          modal: true,
          buttons: {
            Deny: function() {
              Dajaxice.curate.denyRequest(Dajax.process,{"requestid": requestid});
              $( this ).dialog( "close" );
            },
            Cancel: function() {            
                $( this ).dialog( "close" );
            }
          }
        });
      });
}