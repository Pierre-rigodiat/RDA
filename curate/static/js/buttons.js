showButton = function($data, buttonClass) {
    $data.find('.' + buttonClass + ':first').removeClass('hidden');
};

hideButton = function($data, buttonClass) {
    $data.find('.' + buttonClass + ':first').addClass('hidden');
};


addElement = function(event) {
    event.preventDefault();

    var $parents = $(this).parents('[id]');

    // The element has to have a parent
    if ( $parents.size() == 0 ) {
        console.error('No element to duplicate');
        return;
    }

    var $element = $($parents[0]),
        elementId = $element.attr('id');

    console.log("Adding " + elementId + "...")

    $.ajax({
        url : "/curate/generate-bis",
        type : "POST",
        dataType: "html",
        data : {
            id: elementId
        },
        success: function(data){
            var $data = $(data);

            // Displaying the data on the screen
            showButton($data, 'remove');
            $element.after($data);

            // If the element was one of occurence 0
            if ( $element.hasClass('removed') ) {
                $element.remove();
            } else {
                showButton($element, 'remove');
            }

            console.log("Element " + elementId + " successfully created");
        },
        error: function() {
            console.error("An error occured while generating a new element.");
        }
    });
};

removeElement = function(event) {
    event.preventDefault();

    var $parents = $(this).parents('[id]');

    // The element has to have a parent
    if ( $parents.size() == 0 ) {
        console.error('No element to duplicate');
        return;
    }

    var $element = $($parents[0]),
        elementId = $element.attr('id');

    console.log("Removing " + elementId + "...");

    $.ajax({
        url : "/curate/remove-bis",
        type : "POST",
        dataType: "html",
        data : {
            id: elementId
        },
        success: function(data){
            if ( data !== '' ) {  // Some of the data needs to be rewritten
                var $data = $(data);

                $.each($data, function(index, value) {
                    var selector = "[id=" + $(value).attr('id') + "]",
                        searchResults = $(document).find(selector);

                    if ( searchResults.size() > 0 ) {
                        $.each(searchResults, function(index, value) {
                            $(value).remove();
                        });
                    }
                });

                $element.after(data);
            }

            $element.remove();

            console.log("Element " + elementId + " successfully removed");
        },
        error: function() {
            console.error("An error occured while generating a new element.");
        }
    });
};

saveElement = function(event) {
    event.preventDefault();

    var $input = $(this);
    var inputId = $input.attr('id');

    console.log('Saving element ' + inputId + '...');

    $.ajax({
        'url': '/curate/save_element',
        'type': 'POST',
        'dataType': 'json',
        'data': {
            'id': inputId,
            'value': $input.val()
        },
        success: function(data) {
            console.log('Element ' + inputId + ' saved');

            if(data.type === 'choice') {
                console.log('Regenerate')
            }
        },
        error: function(data) {
            console.error('An error occured when saving element ' + inputId);
        }
    });
};

$(document).on('click', '.add', addElement);
$(document).on('click', '.remove', removeElement);
$(document).on('blur', 'input', saveElement);
$(document).on('change', 'select.restriction', saveElement);
$(document).on('change', 'select.choice', saveElement); // FIXME choice shouldn't be used that way