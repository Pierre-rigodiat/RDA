var openModule = null;

closePopUp = function() {
    $('.active_dialog').dialog("close");
    $('.active_dialog').removeClass('active_dialog');
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
            console.log(data);

            saveModuleData(openModule, data);
            closePopUp(openModule);
        }
    };
    popupOptions["buttons"] = $.extend({}, saveButton, popupOptions["buttons"]);
}

$('.mod_popup').on('click', '.open-popup', function(event) {
    event.preventDefault();

    console.log('open dialog');
    openModule = $(this).parent().parent().parent();

    var moduleURL = openModule.find('.moduleURL').text();
    var moduleURLRegExp = new RegExp('/', 'g');
    moduleURL = moduleURL.replace(moduleURLRegExp, '--');

    openModule.find('.mod_dialog').addClass(moduleURL);

    $('.'+moduleURL).addClass('active_dialog');
    $('.'+moduleURL).dialog(popupOptions);
});