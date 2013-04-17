/**
 * 
 */
loadViewXmlController = function()
{
	$('.btn.download-xml').on('click', downloadXml);	
}

downloadXml = function()
{
	console.log('[downloadXml] Downloading XML...');
	
	window.location = 'inc/controllers/php/downloadXml.php';
	
	console.log('[downloadXml] XML downloaded');
}
