var start = null
var end = null;
$(document).ready(function(){
  fetchTimes();
  setInterval(fetchTimes, 60000); // get times on a 60 second interval in case they're updated
});

// fetch times from api
function fetchTimes() {
  $.getJSON("/api/regtime", function(data){
    start = new Date(data['starttime']);
    end = new Date(data['endtime']);
  });
}

updateHeading();
setInterval(updateHeading, 1000);

function niceTime(diff) {
  str = ""
  var days = Math.floor(diff / (1000 * 60 * 60 * 24));
  var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((diff % (1000 * 60)) / 1000);
  if (days > 0)
    str += days + "d " + hours + "h " + minutes + "m " + seconds + "s"
  else
    str += hours + "h " + minutes + "m " + seconds + "s"
  return str;
}

function updateHeading() {
  now = new Date();
  str = ""
  if (start > now && end > now)
  {
    diff = start - now;
    str = "Registration starts in " + niceTime(diff);
  }
  else if (start <= now && end > now)
  {
    diff = end - now;
    str = "Registration is active for another " + niceTime(diff);
  }
  else if (start == null || end == null)
    str = "Loading registration info...";
  else
    str = "Registration is inactive";
  document.getElementById('countdown').textContent = str;
}
