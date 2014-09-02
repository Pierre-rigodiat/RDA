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
            		
            		errors = checkFields(protocol, address, port, user, password);
            		
            		if (errors != ""){
            			$("#instance_error").html(errors);
            		}else{
            			
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
            			Dajaxice.curate.addInstance(Dajax.process,{"name":name, "protocol": protocol, "address":address, "port":port, "user": user, "password": password});
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
    Dajaxice.curate.retrieveInstance(Dajax.process,{"instanceid":instanceid});
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
            		Dajaxice.curate.deleteInstance(Dajax.process, {"instanceid": instanceid});
            	},
            	Cancel: function() {	
            		$( this ).dialog( "close" );
            	}
            }      
        });
	});
}

