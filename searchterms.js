function searchterms() {
  var url = "searching.json";
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var text = JSON.parse(this.responseText);
      display(text, "results");
    }
  };
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
}

// displays results as list
// @param Array arr: results array
function display(arr, id) {
  var words = [];
  for (var word in arr['terms']) {
    words.push(word);
  }
  words.sort();
  var disp = '<ol>';
  for (word in words) {
    disp += '<li>' + words[word] + '</li>\n';
  }
  disp += '</ol>';
  document.getElementById(id).innerHTML = disp;
}