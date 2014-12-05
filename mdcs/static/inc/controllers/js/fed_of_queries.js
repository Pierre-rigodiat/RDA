/**
 * 
 * File Name: fed_of_queries.js
 * Author: Sharief Youssef
 * 		   sharief.youssef@nist.gov
 *
 *        Guillaume SOUSA AMARAL
 *        guillaume.sousa@nist.gov
 * 
 * Sponsor: National Institute of Standards and Technology (NIST)
 * 
 */

loadFedOfQueriesHandler = function()
{
	console.log('BEGIN [loadFedOfQueriesHandler]');
	$('.add.instance').on('click',addInstance);
	$('.edit.instance').on('click',editInstance);
    $('.delete.instance').on('click', deleteInstance);
	console.log('END [loadFedOfQueriesHandler]');
}

addInstance = function()
{
	console.log('BEGIN [addInstance]');
	$("#instance_error").html("");
	$('input:text').each(
		    function(){
		        $(this).val('');
		    });
	$('input:password').each(
		    function(){
		        $(this).val('');
		    });
	$(function() {
        $( "#dialog-add-instance" ).dialog({
            modal: true,
            width: 520,
            buttons: {
            	Test: function(){
            		name = $("#instance_name").val();
            		protocol = $("#instance_protocol").val();
            		address = $("#instance_address").val();
            		port = $("#instance_port").val();
            		user = $("#instance_user").val();
            		password = $("#instance_password").val();
            		
            		$("#instance_error").html("");
            		
            		errors = checkFields(protocol, address, port, user, password);
            		
            		if (errors != ""){
            			$("#instance_error").html(errors);
            		}else{
            			Dajaxice.admin.pingRemoteAPI(Dajax.process,{"name":name, "protocol": protocol, "address":address, "port":port, "user": user, "password": password});
            		}
            	},
            	Add: function() {	
            		name = $("#instance_name").val();
            		protocol = $("#instance_protocol").val();
            		address = $("#instance_address").val();
            		port = $("#instance_port").val();
            		user = $("#instance_user").val();
            		password = $("#instance_password").val();
            		
            		errors = checkFields(protocol, address, port, user, password);
            		
            		if (errors != ""){
            			$("#instance_error").html(errors);
            		}else{
            			Dajaxice.admin.addInstance(Dajax.process,{"name":name, "protocol": protocol, "address":address, "port":port, "user": user, "password": password});
            		}
                },
                Cancel: function() {	
                	$("#instance_error").html("");
            		$( this ).dialog( "close" );
                }
            }
        });
    });
	console.log('END [addInstance]');
}

function ValidateAddress(address)   
{  
	if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(address))  
	{  
		return (true)  ;
	}  
	return (false)  ;
} 

function ValidatePort(port)   
{  
	if (/^[0-9]{1,5}$/.test(port))  
	{  
		return (true)  ;
	}  
	return (false)  ;
} 

function checkFields(protocol, address, port, user, password){
	errors = ""
	
	if (name == "")
	{
		errors += "The name can't be empty.<br/>";
	}
	if(ValidateAddress(address) == false){
		errors += "The address is not valid.<br/>";
	}
	if(ValidatePort(port) == false){
		errors += "The port number is not valid.<br/>";
	}
	if (user == "")
	{
		errors += "The user can't be empty.<br/>";
	}
	if (password == "")
	{
		errors += "The password can't be empty.<br/>";
	}
	
	return errors;
}

editInstance = function()
{    
    var instanceid = $(this).attr("instanceid");
    $("#edit_instance_error").html("");
    Dajaxice.admin.retrieveInstance(Dajax.process,{"instanceid":instanceid});
}

editInstanceCallback = function(name, protocol, address, port, user, password, instanceid){
    $("#edit-instance-name").val(name);
    $("#edit-instance-protocol").val(protocol);
    $("#edit-instance-address").val(address);
    $("#edit-instance-port").val(port);
    $("#edit-instance-user").val(user);
    $("#edit-instance-password").val(password);
    $(function() {
        $( "#dialog-edit-instance" ).dialog({
            modal: true,
            height: 450,
            width: 275,
            buttons: {
                Edit: function() {
                    name = $("#edit-instance-name").val()
                    protocol = $("#edit-instance-protocol").val()
                    address = $("#edit-instance-address").val()
                    port = $("#edit-instance-port").val()     
                    user = $("#edit-instance-user").val()
                    password = $("#edit-instance-password").val()
                     
                    errors = checkFields(protocol, address, port, user, password);
                     
                    if (errors != ""){
                        $("#edit_instance_error").html(errors)
                    }else{
                        Dajaxice.admin.editInstance(Dajax.process,{"instanceid":instanceid,"name":name, "protocol": protocol, "address":address, "port":port, "user": user, "password": password});
                    }
                },
                Cancel: function() {                        
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}
deleteInstance = function()
{
	var instanceid = $(this).attr("instanceid");
	$(function() {
        $( "#dialog-deleteinstance-message" ).dialog({
            modal: true,
            width: 520,
            buttons: {
            	Delete: function() {	
            		Dajaxice.admin.deleteInstance(Dajax.process, {"instanceid": instanceid});
            	},
            	Cancel: function() {	
            		$( this ).dialog( "close" );
            	}
            }      
        });
	});
}

