$('input[type="range"]').on('input', function() {

  var control = $(this),
    controlMin = control.attr('min'),
    controlMax = control.attr('max'),
    controlVal = control.val(),
    controlThumbWidth = control.data('thumbwidth');

  var range = controlMax - controlMin;
  
  var position = ((controlVal - controlMin) / range) * 100;
  var positionOffset = Math.round(controlThumbWidth * position / 100) - (controlThumbWidth / 2);
  var output = control.next('output');
  
  output
    .css('left', 'calc(' + position + '% - ' + positionOffset + 'px)')
    .text(controlVal);

});

// Generate a password string
function randString(id){
  var password_length = parseInt($('#inputRange').val());
  var dataSet = $(id).attr('data-character-set').split(',');  
  var possible = '';
  if($.inArray('a-z', dataSet) >= 0){
    possible += 'abcdefghijklmnopqrstuvwxyz';
  }
  if($.inArray('A-Z', dataSet) >= 0){
    possible += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  }
  if($.inArray('0-9', dataSet) >= 0){
    possible += '0123456789';
  }
  if($.inArray('#', dataSet) >= 0){
    possible += '![]{}()%&*$#^<>~@|';
  }
  var text = '';
  for(var i=0; i < password_length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

// Create a new password on page load
$('input[rel="gp"]').each(function(){
  $(this).val(randString($(this)));
});

// Create a new password
$(".getNewPass").click(function(){
  var field = $(this).closest('div').find('input[rel="gp"]');
  field.val(randString(field));
});

// Auto Select Pass On Focus
$('input[rel="gp"]').on("click", function () {
   $(this).select();
});


