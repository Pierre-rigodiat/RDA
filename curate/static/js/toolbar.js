saveForm = function(event) {
    event.preventDefault();

    console.log('Saving form...')

    $.ajax({
        'url': '/curate/save_form',
        'type': 'POST',
        'dataType': 'json',
        /*'data': {
            'id': inputId,
            'value': $input.val()
        },*/
        success: function(data) {

        },
        error: function(data) {

        }
    });
};

$(document).on('click', '.btn.save-form', saveForm);