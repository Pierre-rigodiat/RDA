delayFunction = function(func, delay)
{
  var timer = null;

    return function(){
        var context = this,
          args = arguments;

        clearTimeout(timer);
        timer = window.setTimeout(
          function(){
              func.apply(context, args);
          },
          delay
        );
    };
}

saveData = function()
{
  console.log('Save data...');

  var data = $('#selectedElement>ul').children();
  var dataString = '';

  data.each(function(index)
  {
    var elementName = $(this).find('.elemName').text();
    var qty = $(this).find('.qty').val();
    var err = $(this).find('.err').val();
    var pur = $(this).find('.pur').val();

    dataString += elementName + '=' + qty + ';' + err + ';' + pur + ';';

    if( index != data.length - 1 ) dataString += '&';
  });

  console.log(dataString);

  // Ajax query to save data inside the module
  $.ajax({
      url: 'parser/_plugins/periodicTable/controllers/php/saveData.php',
      type: 'GET',
      success: function(data) {
        //$('#selectedElement').html(data);
      },
      error: function() {
          console.error("[saveData] A problem occured.");
      },
      // Form data
      data: dataString
  });


}

var delay = 500;
$(document).on('keyup', delayFunction(saveData, delay));



/**
 * Toggle an element of the periodic table
 *
 */
toggleElement = function()
{
  var element = $(this)/*.children('.symbol')*/.text();
  var action = '';

  if($(this).is('.selected'))
  {
    $(this).removeClass('selected');
    action = 'r';
  }
  else
  {
    $(this).addClass('selected');
    action = 'a';
  }

  // Ajax query to add the element to a list in memory
  $.ajax({
      url: 'parser/_plugins/periodicTable/controllers/php/manageElement.php',
      type: 'GET',
      success: function(data) {
        $('#selectedElement').html(data);
      },
      error: function() {
          console.error("[toggleElement] A problem occured during page loading.");
      },
      // Form data
      data: {
        a:action,
        e:$.trim(element)
      },
  });

  return;
}





