loadUserAccountRequest = function()
{
    console.log('BEGIN [loadUserAccountRequest]');
    
    console.log('END [loadUserAccountRequest]');
}

request_account = function()
{
	username = $("#username").val();
	pass1 = $("#password1").val();
	pass2 = $("#password2").val();
	firstname = $("#firstname").val();
	lastname = $("#lastname").val();
	email = $("#emailaddress").val();	
	
	errors = ""
	if (username == "" || pass1 == "" || pass2 == "" || firstname == "" || lastname == "" || email == ""){
		errors += "Some fields are empty.<br/>"
	}
	if (pass1 != pass2){
		errors += "Passwords should be identic."
	}
	if (errors != ""){
		$("#listErrors").html(errors);
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
		Dajaxice.curate.requestAccount(Dajax.process,{"username":username, "password":pass1, "firstname":firstname, "lastname": lastname, "email": email});
	}
}