selectElement = function(divElement)
{   
	console.log('BEGIN [selectElement()]');
    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>None</b>";

    $(function() {
	$("#dialog-select-element" ).dialog({ width: 700 });
        $("#dialog-select-element" ).dialog({
            modal: true,
            buttons: {
		Select: function() {
		    		doSelectElement(divElement);
                    $( this ).dialog( "close" );
                },
		Cancel: function() {
                    $( this ).dialog( "close" );
                }
	    }
        });
    });
	console.log('END [selectElement()]');
}

chooseElement = function(element)
{
    console.log('BEGIN [chooseElement(' + element + ')]');

    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b id=\"selectedElement\">" + element + "</b>";

    console.log('END [chooseElement(' + element + ')]');
}

doSelectElement = function(divElement)
{
    console.log('BEGIN [selectElement(' + divElement + ')]');

    var selectedElement = document.getElementById('selectedElement').innerHTML;
    divElement.onclick = function onclick(event) { selectElement(selectedElement,this); }
    //document.getElementById('elementSelected'+selectedElementId).innerHTML = "Current Selection: " + selectedElement;
	$(divElement).attr("value",selectedElement);
	$($(divElement).parent().children().last()).html("Current Selection: "+selectedElement);
    // reset for next selection
    document.getElementById('chosenElement').innerHTML = "Chosen Element: <b>None</b>";

    console.log('END [selectElement(' + divElement + ')]');
}