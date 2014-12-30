/**
 * 
 * File Name: website.js
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
 * Load controllers for terms of use
 */
loadTermsOfUseControllers = function()
{
    console.log('BEGIN [loadTermsOfUseControllers]');
    $('.btn.terms').on('click', saveTermsOfUse);
    console.log('END [loadTermsOfUseControllers]');
}

/**
 * Save the terms of use
 */
saveTermsOfUse = function(){
	content = $("#terms_of_use_content").val();
	Dajaxice.admin.saveTermsOfUse(saveTermsOfUseCallback, {"content":content});
}

/**
 * Callback displays a success message and redirects to main page
 */
saveTermsOfUseCallback = function(){		
    $(function() {
        $( "#dialog-saved-terms" ).dialog({
            modal: true,
            buttons: {
            	OK: function() {
                    $( this ).dialog( "close" );
                    window.location = "/admin/website"
                }
            }
        });
    });
}


/**
 * Load controllers for privacy policy
 */
loadPrivacyPolicyControllers = function()
{
    console.log('BEGIN [loadPrivacyPolicyControllers]');
    $('.btn.policy').on('click', savePrivacyPolicy);
    console.log('END [loadPrivacyPolicyControllers]');
}

/**
 * Save the terms of use
 */
savePrivacyPolicy = function(){
	content = $("#policy_content").val();
	Dajaxice.admin.savePrivacyPolicy(savePrivacyPolicyCallback, {"content":content});
}

/**
 * Callback displays a success message and redirects to main page
 */
savePrivacyPolicyCallback = function(){		
    $(function() {
        $( "#dialog-saved-policy" ).dialog({
            modal: true,
            buttons: {
            	OK: function() {
                    $( this ).dialog( "close" );
                    window.location = "/admin/website"
                }
            }
        });
    });
}