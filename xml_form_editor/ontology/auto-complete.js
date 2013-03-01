loadAutoComplete = function()
{
	var node;
	var parent;
	
	function split(val)
	{
		return val.split(/,\s*/);
	}


	$(".text").bind("keydown", function(event)
	{
		var test = $(this).parent().parent().prev();
			node = $(this).prev().html();
			parent = ((test.html() != "") ? test.html() : test.prev().html())
	
		if (event.keyCode === $.ui.keyCode.TAB && $(this).data("autocomplete").menu.active)
		{
			event.preventDefault();
		}
	});

	$(".text").autocomplete(
	{
		source : function(request, response)
		{			
			$.ajax(
			{
				url : "ontology/neo4j.php", //server script to process data
				type : 'GET',
				//Ajax events
				success : function(data)
				{
					if (data == "")
						response(data);
					else
					{
						if (data[0] == "<")
							console.error(data.toString());
						else
							response(split(data));
					}
				},
				error : function()
				{
					console.error("Problem importing the file");
				},
				// Form data
				data : 'term=' + request.term + '&node=' + node + '&parent=' + parent,
				//Options to tell JQuery not to process data or worry about content-type
				cache : false,
				contentType : false,
				processData : false
			});

		},
		search : function()
		{
			// custom minLength
			var term = this.value + '|test';
			if (term.length < 1)
			{
				return false;
			}
		},
		focus : function()
		{
			// prevent value inserted on focus
			return false;
		},
		select : function(event, ui)
		{
			// add the selected item
			this.value = ui.item.value;
			return false;
		}
	});
}
