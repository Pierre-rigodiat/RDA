$(document).ready(function(){
	// Linking the event on all the + buttons
	$('#download').on('click', download);
	
	$('#tostep3').on('click', {page: 3}, moveTo);
});

/*download = function()
{	
	/*dhtmlx.modalbox({ 
		type:"confirm",
		title:"Download XML", 
		text:'Your download will start shortly, please enter the name of your xml file <div id="form_in_box"><div class="center"><input type="text" class="inform small" id="filename" name="filename" /><label class="main" for="filename">.xml</label></div></div>',
		buttons:["Cancel", "Download"],
		callback:function(index){
			if(index==1)
			{
				console.log('Downloading...');
				window.location = 'inc/ajax/download.php';
			}
		}
	});*/
	
	/*window.location = 'inc/ajax/download.php';
};*/