saveForm = function(event) {
    event.preventDefault();

    console.log('Saving form...')
    var $xsdForm = $('#xsdForm');
    var inputList = {};
    var threadCount = 0;

    $.each($xsdForm.find('input'), function(index, input) {
        var $input = $(input);
        var inputId = $input.attr('id');

        threadCount += 1;

        $.ajax({
            'url': '/curate/save_form',
            'type': 'POST',
            'dataType': 'json',
            'data': {
                'id': inputId,
                'value': $input.val()
            },
            success: function(data) {
                threadCount -= 1;

                if ( threadCount == 0 ) {
                    console.log('Form saved');
                }
            },
            error: function(data) {
                threadCount -= 1;
                console.error('An error occured when saving element ' + inputId);

                if ( threadCount == 0 ) {
                    console.log('Form saved');
                }
            }
        });
    });
};

$(document).on('click', '.btn.save-form', saveForm);