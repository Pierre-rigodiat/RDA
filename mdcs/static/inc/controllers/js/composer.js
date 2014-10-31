$(document).on('click', function(event) {
  if (!$(event.target).closest('#XMLHolder').length) {
    $("#menu").remove();
  }
});


showhide = function(event){
	console.log('BEGIN [showhide]');
	button = event.target
	parent = $(event.target).parent()
	$(parent.children()[3]).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse");
	}else{
		$(button).attr("class","expand");
	}
		
	console.log('END [showhide]');
}

var target;

var showMenuSequence=function(event){
	$("#menu").remove();
	
	target = event.target;
	$("<ul id='menu' style='position:absolute;z-index:9999;'>" + 
      "<li><span onclick='displayInsertElementSequenceDialog()'>Add Element</span></li>" +
      "</ul>")
		.menu()
		.appendTo("body")
		.position({
	        my: "left top",
	        at: "left bottom",
	        of: event.target
	      }).show();
};		

displayInsertElementSequenceDialog = function()
{
 $(function() {
	$("#table_types").find(".btn.insert").each(function(){
		$(this).attr('onclick','insertElementSequence(event)');
	});
    $( "#dialog-insert-element-sequence" ).dialog({
      modal: true,
      width: 600,
      height: 400,
      buttons: {
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });
}

insertElementSequence = function(event){
	console.log(target);
	
	// change the sequence style
	parent = $(target).parent()
	if ($(parent).attr('class') == "element"){
		$(parent).before("<span class='collapse' style='cursor:pointer;' onclick='showhide(event);'></span>");
		$(parent).after("<ul></ul>");
		$(parent).attr('class','category');
	}
	
	insertButton = event.target;
	typeName = $(insertButton).parent().siblings(':first').text();
	typeID = $(insertButton).parent().siblings(':first').attr('templateid');
	namespace = $(target).text().split(":")[0];
	
	current = $(target).parent().siblings('.path');
	xpath = $(current).text();	
	current = $(current).parent().parent().parent().siblings('.path');
	while(current != null){
		current_path = $(current).text() ;
		if (current_path.contains("schema")){
			current = null;
		}else{			
			xpath = current_path + "/" + xpath;	
			current = $(current).parent().parent().parent().siblings('.path');
		}		
	}
	
	// add the new element
	$(parent).parent().find("ul").append("<li>" +
											"<div class='element-wrapper'>" +
												"<span class='newElement'>" +
													"<span>" +namespace + ":element : "+ "</span>" +													
												"</span>" +
												"<span class='name'>"+ typeName +"</span>" +
												"<span class='type'>"+ typeName +"</span>" +
											"</div>"+
										"</li>")
	
	$( "#dialog-insert-element-sequence" ).dialog("close");
	
	Dajaxice.compose.insertElementSequence(Dajax.process, {"typeID": typeID, "xpath":xpath, "typeName": typeName});
}



