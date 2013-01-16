/**
 * 
 */
loadPaginationController = function()
{
	$('.begin').on('click', {page: 'first'}, loadFormPage);
	$('.end').on('click', {page: 'last'}, loadFormPage);
	$('.previous').on('click', {page: 'prev'}, loadFormPage);
	$('.next').on('click', {page: 'next'}, loadFormPage);
	$('.ctx_menu.button').on('click', {page: null}, loadFormPage);
}

loadFormPage = function(event)
{
	if(event.data.page) console.log('Changing to '+event.data.page+'...');
	else console.log('Changing to '+$(this).text()+'...');
}
