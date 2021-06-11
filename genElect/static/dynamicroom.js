var path = '/api/rooms/offer';

function checkRooms(event) {
  if (event && event.target.id == 'room')
    return
  dict = $('form').serializeArray()
  $.ajax({
      type: 'POST',
      url: path,
      data: JSON.stringify(dict), // or JSON.stringify ({name: 'jonas'}),
      contentType: "application/json",
      dataType: 'json'
  }).done(function(data){
    $('#room').empty();
    $.each(data, function(k,v){
      $('#room').append($("<option></option>").attr("value", v[0]).text(v[1]));
    });
  });
}

$('.form-control').change(function(event){
  checkRooms(event);
});

$(document).ready(function() {
  checkRooms(null);
});
