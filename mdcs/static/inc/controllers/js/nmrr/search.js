initSearch = function(){
	initResources();
	loadRefinements();
}


initResources = function(){
	// select all resources by default
	$("#refine_resource_type").children("input:radio[value=all]").attr("checked","checked")
	
	// get radio to refine resource type
	var radio_btns = $("#refine_resource_type").children("input:radio")
	for(var i = 0; i < radio_btns.length; i++) {
		// when value change
		radio_btns[i].onclick = function() {
			// update refinements options based on the selected schema
			loadRefinements($(this).val());
			// update values for the search
			// get the value
	        selected_val = $(this).val();
	        // update the value of the search form
	        if (selected_val == 'all'){
	        	// check all options
	        	$("#id_my_schemas").find("input").each(function(){
	        		$(this).attr("checked","checked");
	        	});
	        }else{
	        	// uncheck all options except the selected one
	        	$("#id_my_schemas").find("input").each(function(){
	        		if ($(this).val() == selected_val){
	        			$(this).attr("checked","checked");
	        		}else{
	        			$(this).removeAttr("checked");
	        		}	        		
	        	});
	        }
	        
	    };
	}
}



loadRefinements = function(schema){
	$.ajax({
        url : "/explore/load_refinements",
        type : "GET",
        dataType: "json",
        data : {
        	schema:schema,
        },
        success: function(data){
        	$("#refine_resource").html(data.refinements);
        }
    });
}