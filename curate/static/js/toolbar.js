sendSaveRequest = function() {
    console.log('Saving form...')

    $.ajax({
        'url': '/curate/save_form',
        'type': 'POST',
        'dataType': 'json',
        success: function(data) {
            $( "#dialog-saved-message" ).dialog({
                modal: true,
                buttons: {
                    Ok: function() {
                        $( this ).dialog( "close" );
                    }
                }
            });
        },
        error: function(data) {

        }
    });
};

saveForm = function(event)
{
    event.preventDefault();

    $(function() {
        $( "#dialog-save-form-message" ).dialog({
            modal: true,
            buttons: {
				Save: function() {
				    sendSaveRequest()
					$( this ).dialog( "close" );
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}

$(document).on('click', '.btn.save-form', saveForm);