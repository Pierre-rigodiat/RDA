/**
 *	Website page loader call
 *  v0.1
 * 
 * 
 * 
 */

$(document).ready(function(){	
	loadPage($(location).attr('href'));
	
	$('.submenu').on('click', changePage);
});

/**
 * Function to load the content of a page. It is called after a click on a link 
 * @param {String} url
 * @return {String} JSON string with {"html": "htmlCode", "controller": "scriptName"}
 */
loadPage = function(url)
{
	$.ajax({
        url: 'inc/ajax.new/pageLoader.php',
        type: 'GET',
        success: function(data) {
        	// Change content
        	$('#main').html(data);
        	
        	console.log('[loadPage] '+url+' loaded');
        },
        error: function() {
            console.error("[loadPage] A problem occured during page loading.");
        },
        // Form data
        data: 'url='+url,
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

/**
 * 
 */
changePage = function()
{	
	// Update the submenu cursor
	$(this).parent().children('.current').attr('class', 'submenu');
	$(this).attr('class', 'submenu current');
	
	// Load content
	loadPage($(location).attr('href')+'?'+$(this).attr('id'));
}
