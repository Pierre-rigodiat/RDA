$(document).ready(function(){
	// Moving to the next page
	// TODO Write generic function with AJAX loading...
	$('#tostep2').on('click', {page: 2}, moveTo);
});

moveTo = function(event)
{
	if(event.data.page==2)
	{
		console.log('--step2');
		window.location = 'index.php?step=2';
	}
	
	if(event.data.page==1)
	{
		console.log('--step1');
		window.location = 'index.php?step=1';
	}
};