saveCurrentChoiceValue = function($choice) {
    var choiceId = $choice.parent().attr('id');
    var choiceValue = $choice.val();

    $.ajax({
        'url': '/curate/save_element',
        'type': 'POST',
        'dataType': 'json',
        'data': {
            'id': choiceId,
            'value': choiceValue
        },
        'success': function(data) {
            console.log('Element ' + choiceId + ' saved');
        },
        'error': function(data) {
            console.error('An error occured when saving element ' + choiceId);
        }
    });
};

updateChoiceBranch = function($choice, previousChoiceValue) {
    var choiceId = $choice.attr('id');
    var currentChoiceValue = $choice.val();
    var $choiceParent = $choice.parent();

    console.log('Editing tree for ' + choiceId + '...');

    // --------------------------------------------------
    // Find previous element and hide it
    var $previousValueElementList = $choiceParent.find('#'+previousChoiceValue);
    if ( $previousValueElementList.size() != 0 ) {
        console.log('Previous element found, hiding it...');

        var $formBranch = $($previousValueElementList[0]);
        $formBranch.addClass('hidden');
    } else {
        console.warn('Previous element not found, a rendering error might be the cause!');
    }

    // --------------------------------------------------
    // Update form with the new branch
    var $currentValueElementList = $choiceParent.find('#'+currentChoiceValue);
    if ( $currentValueElementList.size() == 0 ) {  // Branch does not exist yet
        console.log('Element ' + currentChoiceValue + ' does not exist, generating it...');

        $.ajax({
            'url': '/curate/generate_choice',
            'type': 'POST',
            'datatype': 'html',
            'data': {
                'id': currentChoiceValue
            },
            'success': function(data) {
                // Add the selected branch to the form
                var $generatedForm = $(data);
                $choice.after($generatedForm);

                // Update the id of the current option (new branch has a different id due to re-generation)
                $choice.find("option:selected").attr('value', $generatedForm.attr('id'));

                // If new modules are included, we need to load the resources
                initModules();
                console.log('Element ' + currentChoiceValue + ' succesfully generated');
            },
            'error': function(data) {
                console.error('An error occured when generating element ' + currentChoiceValue);
            }
        });
    } else {  // Branch exists (need to be toggle)
        console.log('Element ' + currentChoiceValue+' already exists. Displaying it');
        saveCurrentChoiceValue($choice);

        var $formBranch = $($currentValueElementList[0]);
        $formBranch.removeClass('hidden');
    }
};

selectChoice = function(event) {
    event.preventDefault();

    var $choice = $(this);
    var choiceId = $choice.parent().attr('id');

    var previousChoiceValue = null;

    // --------------------------------------------------
    // Getting previous value for the choice
    console.log('Getting previous value of element ' + choiceId + '...');

    var getPreviousValue = $.ajax({
        'url': '/curate/element_value',
        'type': 'POST',
        'dataType': 'json',
        'data': {
            'id': choiceId
        }
    });

    // --------------------------------------------------
    // Success case: Update the form
    var getPreviousValueSuccess = function(data) {
        previousChoiceValue = data.value;
        console.log('Choice ' + choiceId + ' had value: ' + previousChoiceValue);

        updateChoiceBranch($choice, previousChoiceValue); // Update the branch
    };

    // --------------------------------------------------
    // Error case: Send error message
    var getPreviousValueError = function() {
        console.error('An error occured when reading element ' + choiceId);
    };

    // --------------------------------------------------
    // Setting up the request
    getPreviousValue.done(getPreviousValueSuccess);
    getPreviousValue.fail(getPreviousValueError);
};

$(document).on('change', 'select.choice', selectChoice);