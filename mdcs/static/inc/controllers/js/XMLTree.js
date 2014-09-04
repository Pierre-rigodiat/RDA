showhide = function(event){
	console.log('BEGIN [test]');
	button = event.target
	parent = $(event.target).parent()
	$(parent.children()[2]).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse");
	}else{
		$(button).attr("class","expand");
	}
		
	console.log('END [test]');
}