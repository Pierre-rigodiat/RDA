var openModule = null;
var openPopUp = null;

closePopUp = function() {
//    var $activeDialog = $('.active_dialog');

    openPopUp.removeClass('active_dialog');
    openPopUp.dialog("destroy");

    openModule = null;
    openPopUp = null;
};

var popupOptions = {
    modal: true,
    buttons: {
        Cancel: closePopUp
    },
    close: function(event, ui) {
        closePopUp();
    }
}

configurePopUp = function(options, getDataFunction) {
    popupOptions = $.extend({}, popupOptions, options);

    var saveButton = {
        Save: function() {
            data = getDataFunction();
            saveModuleData(openModule, data);

            closePopUp();
        }
    };
    popupOptions["buttons"] = $.extend({}, saveButton, popupOptions["buttons"]);
}

$('body').on('click', '.mod_popup .open-popup', function(event) {
    event.preventDefault();
    openModule = $(this).parent().parent().parent();

    openModule.find('.mod_dialog').addClass('active_dialog');

    openPopUp = $('.active_dialog');
    openPopUp.dialog(popupOptions);
});