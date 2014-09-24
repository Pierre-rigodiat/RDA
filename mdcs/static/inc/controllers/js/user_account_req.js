loadUserAccountRequest = function()
{
    console.log('BEGIN [loadUserAccountRequest]');
    
    console.log('END [loadUserAccountRequest]');
}

checkPassword = function(password){
	//if length is 8 characters or more, increase strength value
	if (password.length < 8){
		return false;
	}
//	//lower and uppercase characters
//	if (!password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)){
//		return false;
//	}
	
	//numbers and characters
	if (!password.match(/([a-zA-Z])/) || !password.match(/([0-9])/)){
		return false;
	} 
}

request_account = function()
{
	username = $("#username").val();
	pass1 = $("#password1").val();
	pass2 = $("#password2").val();
	firstname = $("#firstname").val();
	lastname = $("#lastname").val();
	email = $("#emailaddress").val();	
	
	errors = "";
	if (username == "" || pass1 == "" || pass2 == "" || firstname == "" || lastname == "" || email == ""){
		errors += "Some fields are empty.<br/>";
	}else{
		if (pass1 != pass2){
			errors += "Passwords should be identic.";
		}else{
			if(checkPassword(pass1) == false){
				errors += "Password should respect the following requirements:<br/>"
				errors += "- Minimum length: 8 characters.<br/>"
				errors += "- At least 1 alphanumeric character.<br/>"
				errors += "- At least 1 non alphanumeric character.<br/>"				
			}
		}
		if(!email.match(/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/)){
			errors += "The email address is not valid.<br/>"
		}
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


loadEditProfileHandler = function()
{
    console.log('BEGIN [loadEditProfileHandler]');
    $('.btn.save-profile').on('click', saveProfile);
    console.log('END [loadEditProfileHandler]');
}

saveProfile = function()
{
    console.log('BEGIN [saveProfile]');
    
	firstname = $("#first_name").val();
	lastname = $("#last_name").val();
	username = $("#username").val();
	email = $("#email").val();	
	userid = $(this).attr("userid");
	
	errors = "";
	if (username == "" || firstname == "" || lastname == "" || email == ""){
		errors += "Some fields are empty.<br/>";
	}else{
		if(!email.match(/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/)){
			errors += "The email address is not valid.<br/>"
		}
	}
	if (errors != ""){
		$("#edit-errors").html(errors);
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
		Dajaxice.curate.saveUserProfile(Dajax.process,{"userid":userid, "username":username, "firstname":firstname, "lastname": lastname, "email": email});
	}

    console.log('END [saveProfile]');
}

loadChangePasswordHandler = function()
{
    console.log('BEGIN [loadChangePasswordHandler]');
    $('.btn.change-pass').on('click', changePassword);
    console.log('END [loadChangePasswordHandler]');
}

changePassword = function()
{
    console.log('BEGIN [changePassword]');

    old_pass = $("#old_pass").val();
	pass1 = $("#pass1").val();
	pass2 = $("#pass2").val();
	userid = $(this).attr("userid");
	
	errors = "";
	if (old_pass == "" || pass1 == "" || pass2 == ""){
		errors += "Some fields are empty.<br/>";
	}else{
		if (pass1 != pass2){
			errors += "New passwords should be identic.<br/>";
		}else{
			if(checkPassword(pass1) == false){
				errors += "Password should respect the following requirements:<br/>"
				errors += "- Minimum length: 8 characters.<br/>"
				errors += "- At least 1 alphanumeric character.<br/>"
				errors += "- At least 1 non alphanumeric character.<br/>"				
			}
		}
	}
	if (errors != ""){
		$("#list-errors").html(errors);
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
		Dajaxice.curate.changePassword(Dajax.process,{"userid":userid, "old_password":old_pass, "password":pass1});
	}
    
    
//    $(function() {
//        $( "#dialog-saved-message" ).dialog({
//            modal: true,
//            buttons: {
//                    Ok: function() {
//                    $( this ).dialog( "close" );
//                }
//    }
//        });
//    });

    console.log('END [changePassword]');
}

