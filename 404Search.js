if (window.location.href.indexOf("?") != -1) {
	search();
}
function search() {
	document.getElementById("results").innerHTML = "Searching...";
	var url = "/searching.json";
	var xmlhttp = new XMLHttpRequest();
	var andButton = document.getElementById("and")
	xmlhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var text = JSON.parse(this.responseText);
			var terms = getTerms();
			if (andButton.checked) {andSearch(text, terms)}
				else {orSearch(text, terms);}
		}
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}

// returns array of terms
function getTerms() {
	var markup = ["%E2%80%99", "'", "%c3%bb", "$u", "%27", "'", "\u0294", "''", "\u00ec", "$e", "%29", ")", "\u0157", ",r",	"%20", "+", "%24", "$", "%25", "%",
	"%3b", " "];
	var url = window.location.href;
	url  = url.split("?");
	var searchString = url[1].split("&");
	var andOr = searchString[1].split("=")[1];
	if (andOr == "or") {document.getElementById("or").checked = true}
	var text = searchString[0].split("=")[1];
	for (i = 0; i < markup.length; i += 2) {
		text = text.split(markup[i]).join(markup[i+1]).toLowerCase();
	}
	document.getElementById("term").value = text.split("+").join(" ");
	return text.split("+").filter(function (i) {return i != "";});	
}

// builds array of results containing any search term
// @param arr: raw json array (usually from file)
// @param String[] terms: search terms
function orSearch(arr, terms) {
	output = new Array;
		arr = arr.filter(function (item, pos, ary) {return terms.indexOf(ary[pos].t) != -1;});
		arr = arr.map(function (item) {return item.r});
		if (arr.length > 0) {
			arr = arr.reduce(function (a, b) {return a.concat(b);});
			arr = keySort(arr);
	}
	display(arr, "results", terms);
}

// builds array of results containing all search terms
function andSearch(arr, terms) {
	len = terms.length - 1
	arr = arr.filter(function (item, pos, ary) {return terms.indexOf(ary[pos].t) != -1;});
	arr = arr.map(function (item) {return item.r});
	intersection = intersect(arr);
	if (arr.length > 0) {
		arr = arr.reduce(function (a, b) {return a.concat(b);});
		arr = keySort(arr);
		arr = arr.filter(function (item) {return intersection.indexOf(item.u) != -1;});
	}
	display(arr, "results", terms);
}

// returns an array containing only the intersection
function intersect(arr) {
	output = new Array;
	if (arr.length == 0) {return;}
	arr = arr.filter(function (item) {return item.length > 0;});
	arr = arr.sort(function (a,b) {return a.length > b.length ? true : false;});
	// check for each item in the first/shortest array
	for (var i = 0; i < arr[0].length; i++) {
		inIntersection = true;
		url = arr[0][i].u;
		// check in every other array
		for (var j = 1; j < arr.length; j++) {
			inArray = arr[j].map(function (item) {return item.u == url;}).reduce(function(a,b) {return a || b});
			if (!inArray) {
				inIntersection = false; break;
			}
		}
		if (inIntersection) {output.push(arr[0][i].u)}
	}
	return output;
}

// checks equality of entries
function equal(a, b) {
	return a.u == b.u && a.l == b.l;
}

// checks for equality of urls
function equalUrl(a,b) {
	return a.u == b.u
}

// only keeps unique entries
// arr must be sorted
function uniqueLines(arr) {
	return arr.filter(function(item, pos, ary) {
		return !pos || !equal(item, ary[pos - 1]);
	});
}

// sorts by url and line number
function keySort(arr) {
	return arr.sort(function (a,b) {
		return (a.u > b.u ? 1 : (a.u < b.u ? -1 : (a.n < b.n ? -1 : (a.n > b.n ? 1 : 0))))});
}

// capitalises first letter
function capitalise(string) {
	if (string.length == 0) {return ""}
	if (string.startsWith("&rsquo;")) {
		return string.replace("&rsquo;", "&#x294;");
	} else {
		return string.charAt(0).toUpperCase() + string.slice(1);
	}
}
	

// displays results as list
// @param Array arr: results array
	var markdown = ["&acirc;", "$a", "&ecirc;", "$e", "&icirc;", "$i", "&ocirc;", "$o", "&ucirc;","$u", "&ecirc;", "$e", "&acirc;", "$a", "&ecirc;", "$e", "&agrave;", ")a", "&egrave;", ")e", "&igrave;", ")i", "&ograve;", ")o", "&ugrave;", ")u", "&#x14d;", "_o", "&#x2b0;", "+h", "&#x255;", ",c", "&#x14b;", ",n", "&rsquo;", "'", "&#x294;", "''", "&#x2b1;", "$h", "&#x268;", "-i", "&#x25f;", "=j", "&#x28e;", "$l", "&#x272;", "$n", "&#x279;", "$r", "&#x157;", ",r", "&#x259;", "!e", "&#x289;", "-u", "&#x16b;", "_u"]
function display(arr, id, terms) {
	if (arr.length == 0) {
		document.getElementById(id).innerHTML = "Search term(s) not found";
		return;
	}
	arr = uniqueLines(arr)
	var text = "<ol>"
	for (var i = 0; i < arr.length; i++) {
		lines = new Array;
		first_url = arr[i].u;
		new_url = first_url;
		while (new_url == first_url) {
			lines.push(arr[i].l);
			i++;
			if (i >= arr.length) {break;}
			new_url = arr[i].u;
		}
		i--
		line = lines.join(" &hellip; ");
		// bold search terms
		for (var j = 0; j < terms.length; j++) {
			term = terms[j];
			for (var k = 0; k < markdown.length; k += 2) {
				term = term.split(markdown[k+1]).join(markdown[k])
			}
			line = line.split(term).join("<b>" + term + "</b>");
			term = capitalise(term);
			line = line.split(term).join("<b>" + term + "</b>");
		}
		line = line.replace(/b>/g, "strong>");
		//<li><a href="blah/index.html">Blah</a>: foo blah bar </li>
		text += "<li><a href=\"" + arr[i].u + "\">" + arr[i].a + "</a>: " + line + "</li>";
	}
	text += "</ol>";
	document.getElementById(id).innerHTML = text;
}