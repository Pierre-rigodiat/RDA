/**
 * 
 */
loadViewXmlController = function()
{
	$('.download.xml').on('click', downloadXml);	
}

downloadXml = function()
{
	console.log('[downloadXml] Downloading XML...');
	
	window.location = 'inc/ajax.new/downloadXml.php';
	
	console.log('[downloadXml] XML downloaded');
}
