configureAutocomplete($('#element5'), {
    source: "/modules/test/autocomplete",
    minLength: 0,
    response: function(event, ui) {
        var content = ui.content[1];

        while(ui.content.length !== 0) {
            ui.content.pop();
        }

        $.each(content, function(key, value) {
            ui.content.push({label: value, value: value});
        });
    }
})
