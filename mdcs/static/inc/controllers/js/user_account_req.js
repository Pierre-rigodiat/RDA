/**
 * 
 * File Name: user_account_req.js
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
 * Check that the password is correct
 * @param password
 * @returns {Boolean}
 */
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

/**
 * Check that the current request is valid
 */
validateRequest = function(){
	pass1 = $("#id_password1").val();
	pass2 = $("#id_password2").val();
	
	errors = "";
	
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
	
	if (errors != ""){
		$("#request_error").html(errors);
		return (false);
	}
	else{
		$("#request_error").html("");
		return (true);
	}
}

/**
 * Load controllers for edit profile page
 */
loadEditProfileHandler = function()
{
    console.log('BEGIN [loadEditProfileHandler]');
    $('.btn.save-profile').on('click', saveProfile);
    console.log('END [loadEditProfileHandler]');
}

/**
 * Save the user profile
 */
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
		Dajaxice.admin.saveUserProfile(Dajax.process,{"userid":userid, "username":username, "firstname":firstname, "lastname": lastname, "email": email});
	}

    console.log('END [saveProfile]');
}

/**
 * Load controllers for change password page
 */
loadChangePasswordHandler = function()
{
    console.log('BEGIN [loadChangePasswordHandler]');
    $('.btn.change-pass').on('click', changePassword);
    console.log('END [loadChangePasswordHandler]');
}

/**
 * Change the user password
 */
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
		Dajaxice.admin.changePassword(Dajax.process,{"userid":userid, "old_password":old_pass, "password":pass1});
	}
    
    console.log('END [changePassword]');
}

/**
 * Display a dialog with errors when bad user account request 
 */
showErrorRequestDialog = function(){
	$("#listErrors").html("This user already exists. Please choose another username.");
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

/**
 * Display a dialog with success message when user request sent
 */
showSentRequestDialog = function (){
	$(function() {
        $( "#dialog-request-sent" ).dialog({
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
 * Display a dialog with errors for user profile edition
 * @param errors
 */
showEditErrorDialog = function(errors){
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

/**
 * Display a message when user profile saved
 */
showSavedProfileDialog = function(){
	$(function() {
        $( "#dialog-saved-message" ).dialog({
            modal: true,
            buttons: {
                    Ok: function() {                        
                    $( this ).dialog( "close" );
                    window.location = "/my-profile";
                }
            }
        });
    });
}

/**
 * Display a dialog with errors for user password change
 * @param errors
 */
showChangePasswordErrorDialog = function(errors){
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

/**
 * Display a message when user password changed
 */
showPasswordChangedDialog = function(){
    $(function() {
        $( "#dialog-saved-message" ).dialog({
            modal: true,
            buttons: {
                    Ok: function() {                        
                    $( this ).dialog( "close" );
                    window.location = "/my-profile";
                }
            }
        });
    });
}