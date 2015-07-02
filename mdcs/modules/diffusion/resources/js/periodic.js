var periodicTablePopupOptions = {
    width: 1000,
    title: "Select Element",
    create: function(event, ui) {
        // Selection highlight
        $(this).on('click', '.periodic-table td.p-elem', function(event) {
            var pTable = $(this).parent().parent();

            $.each(pTable.find('.selected'), function(index, element) {
                $(element).removeClass('selected')
            })

            $(this).addClass('selected');
        });
    },
    open: function(event, ui) {
        var selectedElement = openModule.find('.moduleResult').text();

        if(selectedElement !== "") {
            $(this).find(".p-elem").removeClass('selected');
            $(this).find(".p-elem:contains('"+selectedElement+"')").addClass('selected');
        }
    },
    beforeClose: function(event, ui) {
        console.log("before close")
        console.log(openModule.find('.p-elem.selected'));
        openModule.find('.p-elem.selected').removeClass('selected');
    }
}

savePeriodicTableData = function() {
    console.log("save");

    var selectedElement = $('.active_dialog .periodic-table .selected').text();
    console.log(selectedElement);

    return {'selectedElement': selectedElement};
}

configurePopUp(periodicTablePopupOptions, savePeriodicTableData);