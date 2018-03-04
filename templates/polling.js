xmlhttp = new XMLHttpRequest();
function callServer(){
  var url = "https://yokosuka2018.herokuapp.com/last"
  xmlhttp.open("GET", url, true);
  xmlhttp.onreadystatechange = updatePage
  xmlhttp.send(null)
}
function updatePage(){
  // alert("updatePage() called with ready state of " + xmlhttp.readyState);
  if (xmlhttp.readyState == 4) {
    // alert(xmlhttp.status)
    var response = xmlhttp.responseText;
    console.log(response)
    // $('#apple').stop().animate({width:(200 + 5 * ary[0]).toString() + 'px'}, 200);
  }
}

$(function(){
    setInterval(function(){
      callServer();
    },500);
});
