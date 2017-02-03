var custom_view_done;
var timeout;
var first_occurence = true;

initSearch = function(listRefinements, keyword, resource) {
    selectRadio(resource);
    select_hidden_schemas(resource)
	initResources();
    //$("#refine_resource_type").children("input:radio[value="+resource+"]").click();
	loadRefinements(resource, listRefinements, keyword);
}

selectRadio = function(radio) {
    var radio_btns = $("#refine_resource_type").children("input:radio")
	for(var i = 0; i < radio_btns.length; i++) {
	    selected_val = $(radio_btns[i]).val();
	    if (selected_val == radio) {
	        $(radio_btns[i]).click();
	        $("#icons_table").find("td").each(function(){
		        	$(this).removeClass("selected_resource");
		        	if ($(this).attr("value") == selected_val){
		        		$(this).addClass("selected_resource");
		        	}
	        	});
	    }
	}
}


update_url = function() {
    console.log('update url');
    if ( first_occurence) {
        console.log('update url but not ready');
        return ;
    }
    var refinements = [];
    $('*[id^="tree_"]').each(function() {
        getSelectedRefinements($(this), refinements);
    });


	var keyword = $("#id_search_entry").val();
	var role = $('input[name=resource_type]:checked', '#refine_resource_type').val();
	$.ajax({
        url : "/explore/update_url",
        type : "GET",
        dataType: "json",
        data : {
            keyword: keyword,
            role: role,
            refinements: refinements,
        },
        success: function(data) {
            History.pushState("", "", data.url);
        }
    });
}

/**
 * Set keywords
 */
set_keyword = function(keyword) {
    console.log('put keywords from url');
    var list_keyword = keyword.split('&amp;');
    for (var i=0 ; i<list_keyword.length ; i++) {
        $("#id_search_entry").tagit("createTag", list_keyword[i]);
    }
}

/**
 * Load refinement queries
 */
selectRefinementQueries = function(listRefinement) {
    console.log('select the refinements from url');
	var list_refinements = listRefinement.split('&amp;');

    $('*[id^="tree_"]').each(function() {
        var root = $(this).fancytree('getTree');
        for (var i = 0; i < list_refinements.length; i++) {
            var node = root.getNodeByKey(list_refinements[i]);
            if (node != null) {
                node.setSelected(true);
            }
        }
    });
}

select_hidden_schemas = function (selected_val) {
// update the value of the search form
    if (selected_val == 'all') {
        // check all options
        $("#id_my_schemas").find("input").each(function () {
            $(this).prop("checked", true);
        });
    } else {
        // uncheck all options except the selected one
        $("#id_my_schemas").find("input").each(function () {
            if ($(this).val() == selected_val) {
                $(this).prop("checked", true);
            } else {
                $(this).removeAttr("checked");
            }
        });
    }
}
initResources = function(){
    console.log('init resources');
	// get radio to refine resource type
	var radio_btns = $("#refine_resource_type").children("input:radio");
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
		        	if ($(this).attr("value") == 'datacollection') {
                        $(this).addClass("selected_resource");
                    }
	        	});
	        }else {
                $("#icons_table").find("td").each(function () {
                    $(this).removeClass("selected_resource");
                    if ($(this).attr("value") == selected_val) {
                        $(this).addClass("selected_resource");
                    }
                });
            }

			// update refinements options based on the selected schema
			loadRefinements(selected_val, '', '');

			// update filters: if custom, switch to default simple
			if ($("#results_view").val() == "custom"){
				$("#results_view").val("simple");
			}
			filter_result_display($("#results_view").val());
			custom_view_done = false;
            select_hidden_schemas(selected_val);
	    };
	}
	console.log('fin init resources');
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
	$("#config_custom").css('display','none');
	
	if (filter == 'simple'){
		$(".nmrr_line").hide();
		$(".nmrr_line.line_publisher").show();
		$(".nmrr_line.line_creator").show();
		$(".nmrr_line.line_subject").show();
	}else if (filter == 'detailed'){
		$(".nmrr_line").show();
	}else if (filter == 'custom'){
		$("#config_custom").css('display','');
		if (custom_view_done == true){
	    	$(".nmrr_line").hide();
			$("#custom_view").children("input:checked").each(function(){
				$(".nmrr_line." + $(this).val()).show();
			});
		}
		else{
			configure_custom_view();
		}
	}
}


configure_custom_view = function(){
	if (custom_view_done == false){
		load_custom_view($('input[name=resource_type]:checked').val());
		custom_view_dialog();
	}else{
		custom_view_dialog();
	}
}


custom_view_dialog = function(){	
    $( "#dialog-custom-view" ).dialog({
        modal: true,
        height: 500,
        width: 400,
        buttons: {
            Cancel: function() {
            	$( this ).dialog( "close" );
            },
            Apply: function() {
            	$( this ).dialog( "close" );
            	$(".nmrr_line").hide();
    			$("#custom_view").children("input:checked").each(function(){
    				$(".nmrr_line." + $(this).val()).show();
    			});
            }
        },
        close: function(){
        	custom_view_done = true;
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
 * AJAX call, gets query results
 * @param numInstance
 */
get_results_keyword_refined = function(numInstance){
    if (first_occurence) {
        return ;
    }
    update_url();
	// clear the timeout
	clearTimeout(timeout);
	// send request if no parameter changed during the timeout
    timeout = setTimeout(function(){
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
            	registries: getRegistries(),
            },
            beforeSend: function( xhr ) {
                $("#loading").addClass("isloading");
            },
            success: function(data){
            	if (data.resultString.length == 0){
            		// get no results
            		$("#results").html("No results found");
            		// get no results
            		$("#results_infos").html("0 results");
            	}
            	else{
            		// get result count
            		if(data.count > 1)
            	        $("#results_infos").html(data.count + " results");
                    else
                        $("#results_infos").html(data.count + " result");
            		// get results
            		$("#results").html(data.resultString);
            		// filter the view
            		filter_result_display($("#results_view").val());
            	}
            	$(".description").shorten({showChars: 350,
                    ellipsesText: "",
                    moreText: "... show more",
                    lessText: " show less",
                });
            },
            complete: function(){
                $("#loading").removeClass("isloading");
            }
        });
    }, 1000);
}

// clear all refinements
clearRefinements = function(){
	$("#refine_resource").find('input:checked').prop('checked',false);
	get_results_keyword_refined();
}

updateRefinementsOccurrences = function(avoid_tree){
    var keyword = $("#id_search_entry").val();
	$.ajax({
        url : "/explore/get_results_occurrences",
        type : "GET",
        dataType: "json",
        data : {
            keyword: keyword,
            schemas: getSchemas(),
            refinements: loadRefinementQueries(),
            allRefinements: getAllRefinements(),
            onlySuggestions: false,
            registries: getRegistries(),
        },
        beforeSend: function( xhr ) {

        },
        success: function(data){
            $.map(data.items, function (item) {
                var text = $("#"+item.text_id)
                text.html(item.nb_occurrences);
                if(item.nb_occurrences == 0)
                    text.closest('span').fadeTo(500, 0.2);
                else
                    text.closest('span').fadeTo(500, 1);
            });
        },
        complete: function(){

        }
    });
}

/**
 * Load refinement queries
 */
loadRefinementQueries = function(){
	var dict = [];
    $('*[id^="tree_"]').each(function(){
        var refinements = [];
        getSelectedRefinements($(this), refinements);
        if(!$.isEmptyObject(refinements))
        {
            dict.push({
                key:   this.id,
                value: refinements
            });
        }
    });

	return JSON.stringify(dict);
}


getSelectedRefinements = function (tree, refinements){
    var nodes = tree.fancytree('getRootNode').tree.getSelectedNodes();
    $(nodes).each(function() {
        refinements.push($(this)[0].key);
    });
}

getAllRefinements = function(avoid_tree=""){
    var dict = [];

    $('*[id^="tree_"]:not(#tree_'+avoid_tree+')').each(function(){
        var refinements = [];
        var nodes = $(this).fancytree('getRootNode').getChildren();
        getRefinementsChildren(nodes, refinements);
        dict.push({
            key:   this.id,
            value: refinements
        });
    });

	return JSON.stringify(dict);
}


getRefinementsChildren = function(children, refinements)
{
   if(children === undefined)
        return;

    $(children).each(function() {
        refinements.push($(this)[0].key);
        var nodes = $(this)[0].getChildren();
        getRefinementsChildren(nodes, refinements);
    });
}


loadRefinements = function(schema, listRefinements, keyword){
    console.log('load refinements');
	$("#refine_resource").html('');
	$.ajax({
        url : "/explore/load_refinements",
        type : "GET",
        dataType: "json",
        data : {
        	schema:schema,
        },
        success: function(data){
            $("#refine_resource").html(data.template);
            $.map(data.items, function (item) {
                initFancyTree(item.div_id, item.json_data);
            });
            if (first_occurence) {
                console.log('load refinements + first occ');
                selectRefinementQueries(listRefinements);
                set_keyword(keyword);
                first_occurence = false;
            }
            updateRefinementsOccurrences();
            initFilters();
	        custom_view_done = false;
	        get_results_keyword_refined();
        }
    });
}

initFancyTree = function(div_id, json_data) {

    $("#tree_"+div_id).fancytree({
      extensions: ["glyph", "wide"],
      checkbox: true,
      icon: false,
      glyph: glyph_opts,
      selectMode: 3,
      source: JSON.parse(json_data),
      toggleEffect: { effect: "drop", options: {direction: "left"}, duration: 400 },
      wide: {
        iconWidth: "1em",
        iconSpacing: "0.5em",
        levelOfs: "1.5em"
      },
      init: function(event, data) {
        $("#tree_"+div_id+" ul").addClass("fancytree-colorize-selected");
        // Render all nodes even if collapsed
        $(this).fancytree("getRootNode").render(force=true, deep=true);
      },
      select: function(event, data){
          if (! first_occurence) {
              updateRefinementsOccurrences(div_id);
                get_results_keyword_refined();
          }
      }
    });
}

glyph_opts = {
    map: {
      doc: "glyphicon glyphicon-file",
      docOpen: "glyphicon glyphicon-file",
      checkbox: "glyphicon glyphicon-unchecked",
      checkboxSelected: "glyphicon glyphicon-check",
      checkboxUnknown: "glyphicon glyphicon-share",
      dragHelper: "glyphicon glyphicon-play",
      dropMarker: "glyphicon glyphicon-arrow-right",
      error: "glyphicon glyphicon-warning-sign",
      expanderClosed: "glyphicon glyphicon-menu-right",
      expanderLazy: "glyphicon glyphicon-menu-right",
      expanderOpen: "glyphicon glyphicon-menu-down",
      folder: "glyphicon glyphicon-folder-close",
      folderOpen: "glyphicon glyphicon-folder-open",
      loading: "glyphicon glyphicon-refresh glyphicon-spin"
    }
};
