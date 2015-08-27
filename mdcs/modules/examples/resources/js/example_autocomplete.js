configureAutocomplete({
    source: function(request, response) {
        var term = request.term;

        $.ajax({
            url: '/modules/examples/autocomplete',
            method: 'POST',
            data: {
                'data': term
            },
            success: function(data) {
                var textData = $(data).find('.moduleDisplay').text();
                var re = new RegExp("'", 'g');

                textData = textData.replace(re, '\"');
                console.log(textData);

                var jsonData = JSON.parse(textData);
                response(jsonData);
            }
        });
    },
    minLength: 0,
    /*response: function(event, ui) {
        var content = ui.content[1];

        while(ui.content.length !== 0) {
            ui.content.pop();
        }

        $.each(content, function(key, value) {
            ui.content.push({label: value, value: value});
        });
    }*/
})
