var periodicTablePopupOptions = {
    width: 1000,
    title: "Select Element",
    create: function(event, ui) {
        $(this).on('click', '.periodic-table td.p-elem', function(event) {
            var pTable = $(this).parent().parent();

            $.each(pTable.find('.selected'), function(index, element) {
                $(element).removeClass('selected')
            })

            $(this).addClass('selected');
        });
    },
    open: function(event, ui) {
        var selectedElement = openModule.find('.moduleDisplay .selected').text();

        if(selectedElement !== "") {
            console.log(selectedElement);
            $(this).find(".p-elem:contains('"+selectedElement+"')").addClass('selected');
        }
    },
    beforeClose: function(event, ui) {
        console.log($(this).find('.p-elem.selected'));
        $(this).find('.p-elem.selected').removeClass('selected');
    }
}

savePeriodicTableData = function() {
    var selectedElement = $('.active_dialog .periodic-table .selected');
    console.log(selectedElement);

    return {'selectedElement': selectedElement.text()};
}

configurePopUp(periodicTablePopupOptions, savePeriodicTableData);