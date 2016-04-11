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
                var elementClass = $element.attr('class');

                $.each($('.'+elementClass), function(index, occurence) {
                    showButton($(occurence), 'remove');
                });

                // Updating the class with the good parent
                $data.removeClass();
                $data.addClass(elementClass);
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
        console.error('No element to remove');
        return;
    }

    var $element = $($parents[0]),
        elementId = $element.attr('id');

    console.log("Removing " + elementId + "...");

    $.ajax({
        url : "/curate/remove-bis",
        type : "POST",
        dataType: "json",
        data : {
            id: elementId
        },
        success: function(data){
            if ( data.code === 1 ) {  // Remove buttons need to be hidden
                console.log('Buttons for ' + elementId + ' need to be hidden');
                var elementClass = $element.attr('class');

                $.each($('.'+elementClass), function(index, occurence) {
                    hideButton($(occurence), 'remove');
                });
            } else if ( data.code === 2 ) {  // Elements need to be rewritten
                console.log('Element ' + elementId + ' need to be rewritten');
                $element.after(data.html);
            }

            $element.remove();
            console.log("Element " + elementId + " successfully removed");
        },
        error: function() {
            console.error("An error occured while generating a new element.");
        }
    });
};

$(document).on('click', '.add', addElement);
$(document).on('click', '.remove', removeElement);