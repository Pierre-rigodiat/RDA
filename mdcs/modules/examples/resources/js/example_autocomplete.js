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
    minLength: 0
})
