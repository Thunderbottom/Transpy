/**
 * Created by mussaimo on 5/31/16.
 */
$(function() {
  $('#btnTrans').click(function() {
    $('#alert').hide();
    $('#info').hide();
    if (!(translate_form.inputString.value && translate_form.inputIter.value)) {
      $('#alert').show();
    }
    else{
      if (parseInt(translate_form.inputIter.value) > 52) {
        $('#info').show();
      }
      $('#loader').show();
      $.ajax({
        url: '/translateText',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
          $('#loader').hide();
          respdiv = document.getElementById("stuff");
          respdiv.innerHTML = response;
        },
        error: function(error) {
          $('#loader').hide();
          console.log(error);
        }
      });
    }
  });
});
