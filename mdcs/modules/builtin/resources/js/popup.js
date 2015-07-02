var openModule = null;

closePopUp = function() {
    var $activeDialog = $('.active_dialog');

    $activeDialog.removeClass('active_dialog');
    $activeDialog.dialog("close");
    $activeDialog.dialog("destroy");

};

var popupOptions = {
    modal: true,
    buttons: {
        Cancel: closePopUp
    }
}

configurePopUp = function(options, getDataFunction) {
    popupOptions = $.extend({}, popupOptions, options);

    var saveButton = {
        Save: function() {
            data = getDataFunction();
            saveModuleData(openModule, data);
            closePopUp(openModule);
        }
    };
    popupOptions["buttons"] = $.extend({}, saveButton, popupOptions["buttons"]);
}

$('body').on('click', '.mod_popup .open-popup', function(event) {
    console.log("Opening module popup...")

    event.preventDefault();
    openModule = $(this).parent().parent().parent();

    // TODO Redo a $.ajax GET to reparse the module
    var moduleURL = openModule.find('.moduleURL').text();
    /*$.ajax({
        url: '/modules/'+moduleURL,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log(data);
        },
        error: function() {
            console.error('Problem @ module loading');
        }
    });*/

    //var moduleURLRegExp = new RegExp('/', 'g');
    //moduleURL = moduleURL.replace(moduleURLRegExp, '--');

    openModule.find('.mod_dialog').addClass('active_dialog');
    $('.active_dialog').dialog(popupOptions);
});