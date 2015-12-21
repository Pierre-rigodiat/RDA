var custom_view_done;

initSearch = function(){
	initResources();
	loadRefinements('all');
	initFilters();	
	custom_view_done = false;
}


initResources = function(){
	// select all resources by default
	$("#refine_resource_type").children("input:radio[value=all]").prop("checked", true);
	$("#id_my_schemas").find("input").each(function(){
		$(this).prop("checked", true);
	});
	
	// get radio to refine resource type
	var radio_btns = $("#refine_resource_type").children("input:radio")
	for(var i = 0; i < radio_btns.length; i++) {
		// when value change
		radio_btns[i].onclick = function() {
			// get the value
	        selected_val = $(this).val();
			
			// update selected icon
	        if (selected_val == 'repository'
	        	|| selected_val == 'projectarchive'
	        		|| selected_val == 'database'){
	        	$("#icons_table").find("td").each(function(){
		        	$(this).removeClass("selected_resource");
		        	if ($(this).attr("value") == 'datacollection'){
		        		$(this).addClass("selected_resource");
		        	}	        	
	        	});
	        }else{
	        	$("#icons_table").find("td").each(function(){
		        	$(this).removeClass("selected_resource");
		        	if ($(this).attr("value") == selected_val){
		        		$(this).addClass("selected_resource");
		        	}	        	
	        	});
	        }	        
			
			// update refinements options based on the selected schema
			loadRefinements(selected_val);
			
			// update filters: if custom, switch to default simple
			if ($("#results_view").val() == "custom"){
				$("#results_view").val("simple");
			}
			filter_result_display($("#results_view").val());
			custom_view_done = false;

	        // update the value of the search form
	        if (selected_val == 'all'){
	        	// check all options
	        	$("#id_my_schemas").find("input").each(function(){
	        		$(this).prop("checked", true);
	        	});
	        }else{
	        	// uncheck all options except the selected one
	        	$("#id_my_schemas").find("input").each(function(){
	        		if ($(this).val() == selected_val){
	        			$(this).prop("checked",true);
	        		}else{
	        			$(this).removeAttr("checked");
	        		}	        		
	        	});
	        }
	        get_results_keyword_refined();
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


dialog_detail = function(id){
	$.ajax({
        url : "/explore/detail_result_keyword?id=" + id,
        type : "GET",
        success: function(data){
        	console.log(data);
        	$("#result_detail").html(data);
        	
        	$(function() {
                $( "#dialog-detail-result" ).dialog({
                    modal: true,
                    buttons: {
                        Ok: function() {
                        $( this ).dialog( "close" );
                        }
                    }
                });
            });
        }
    });
	
}


initFilters = function(){
	// Set filter to simple by default
	$("#results_view").val("simple");
	
	// update view on filter change
	$("#results_view").on('change',function(){
		filter_result_display($("#results_view").val());
	});
}


filter_result_display = function(filter){
	if (filter == 'simple'){
		$(".nmrr_line").hide();
		$(".nmrr_line.line_publisher").show();
		$(".nmrr_line.line_type").show();
	}else if (filter == 'detailed'){
		$(".nmrr_line").show();
	}else if (filter == 'custom'){
		if (custom_view_done == true){
	    	$(".nmrr_line").hide();
			$("#custom_view").children("input:checked").each(function(){
				$(".nmrr_line." + $(this).val()).show();
			});
		}
	}
}


configure_custom_view = function(){
	if ($('input[name=resource_type]:checked').val() == 'all'){
	    $( "#dialog-custom-view-error" ).dialog({
	        modal: true,
	        buttons: {
	            OK: function() {
	            	$( this ).dialog( "close" );
	            	$("#results_view").val("simple");
	            }
	        }
	    });
	}
	else{
		if (custom_view_done == false){
			load_custom_view($('input[name=resource_type]:checked').val());
			custom_view_dialog();
		}else{
			custom_view_dialog();
		}
	}		
}


custom_view_dialog = function(){
    $( "#dialog-custom-view" ).dialog({
        modal: true,
        buttons: {
            Cancel: function() {
            	$( this ).dialog( "close" );
            },
            Apply: function() {
            	$( this ).dialog( "close" );
            	custom_view_done = true;
            	$(".nmrr_line").hide();
    			$("#custom_view").children("input:checked").each(function(){
    				$(".nmrr_line." + $(this).val()).show();
    			});
            }
        }
    });
}


/**
 * Load custom view
 */
load_custom_view = function(schema){
	$.ajax({
        url : "/explore/custom-view?schema=" + schema,
        type : "GET",
        dataType: "json",
        success: function(data){
        	if('custom_fields' in data){
        		$("#custom_view").html(data.custom_fields);
        	}
    	}
    });
}


/**
 * Load refinement queries
 */
loadRefinementQueries = function(){
	var refinements = [];
	$("#refine_resource").find("input:checked").each(function(){
		query = $(this).closest("div.refine_criteria").attr("query");
		val = $(this).val();
		refinements.push(query + ":" + val);
	});
	console.log(refinements);

	return refinements;
}


/**
 * AJAX call, gets query results
 * @param numInstance
 */
get_results_keyword_refined = function(numInstance){
    $("#results").html('Please wait...');
    var keyword = $("#id_search_entry").val();
    $.ajax({
        url : "/explore/get_results_by_instance_keyword",
        type : "GET",
        dataType: "json",
        data : {
        	keyword: keyword,
        	schemas: getSchemas(),
        	refinements: loadRefinementQueries(),
        	onlySuggestions: false,
        },
        beforeSend: function( xhr ) {
            $("#loading").addClass("isloading");
        },
        success: function(data){
        	if (data.resultString.length == 0){
        		// get no results
        		$("#results").html("No results found");
        	}
        	else{
        		// get results
        		$("#results").html(data.resultString);
        		// filter the view
        		filter_result_display($("#results_view").val());
        	}
        },
        complete: function(){
            $("#loading").removeClass("isloading");
        }
    });
}

