var targetNodes         = $("#xsdForm"); // 
var MutationObserver    = window.MutationObserver || window.WebKitMutationObserver;
var autoKeyObserver     = new MutationObserver (autoKeyHandler);
var obsConfig           = {childList: true, subtree:true};

// init number of keys to 0
var nbAutoKey = 0 

// Add a target node to the observer. Can only add one node at a time.
// Every time the form is updated, keyrefs will be updated 
targetNodes.each ( function () {
	autoKeyObserver.observe (this, obsConfig);
} );

function autoKeyHandler (mutationRecords) {
	current_nbAutoKey = $(".mod_auto_key").length;
	console.log('previous: ' + nbAutoKey);
	console.log('current: ' + current_nbAutoKey);
	// number of keys has changed
	if (current_nbAutoKey != nbAutoKey){
		// a key has been added (or more)
		if (current_nbAutoKey > nbAutoKey){
			console.log('Keys have been added.')
			nbAutoKey = current_nbAutoKey;
		    $.ajax({
		        url : "/modules/curator/get-updated-keys",
		        type : "GET",
		        dataType: "json",
		        success: function(data){
		        	console.log(data);
		        	for (key_name in data){
		        		console.log(key_name);
		        		console.log(data[key_name]['tagIDs']);
		        		var i;
		        		for (i = 0; i < data[key_name]['tagIDs'].length; ++i) {
		        		    tagID = data[key_name]['tagIDs'][i];
		        		    console.log(tagID);
		        		    // build the new options
		        		    options = ''
		        		    for (j = 0; j < data[key_name]['ids'].length; ++j) {
		        		    	id = data[key_name]['ids'][j]
		        		    	console.log(id);
		        		    	options += "<option value='" + id + "'>" + id + "</option>"
		        		    }
		        		    console.log(options)
		        			var select = $("#" + tagID).children("div.module").children(".moduleContent").find("select");
		        		    selectedOption = select.val();
		        		    // set the new options
		        		    select.html(options);
		        		    select.val(selectedOption);
				        }
		    		}
		    	}
		    });
		} else { // a key has been removed (or more)
			console.log('Keys have been removed.')
		}
	} 
}