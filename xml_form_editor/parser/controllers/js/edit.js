/**
 * JS to edit element in the configuration view
 * Script version: 1.0
 * Author: P.Dessauw
 * 
 */
$(document).ready(function(){
	$( "#dialog" ).dialog({
        autoOpen: false,
        show: "blind",
        hide: "explode",
        height: 300,
        width: 350,
        modal: true,
        buttons: {
            "Create an account": function() {
                $( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        close: function() {
            //allFields.val( "" ).removeClass( "ui-state-error" );
        }
    });
	
	// We need to use .live() method here because of the newly created elements
	// Linking the event on all the + buttons
	$('.edit').on('click', editElement);
});

/**
 * Function to call the PHP script and replace the current element 
 * @param event Handle the JSON string put in parameter
 * 
 */
editElement = function()
{
	$( "#dialog" ).dialog( "open" );
    return false;
}
