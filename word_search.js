/* Goes directly to an inputted word*/

function word_search() {
	var text;
	var folder;
	var first_letter;
	text = document.getElementById("search").value.toLowerCase();
	text = text.trim().replace(/[\u2019]/g, "'")
	text = text.replace(/[\u0294\u0660]/g, "''")
	for (var i = 0; i < text.length; i++) {
		first_letter = text.charCodeAt(i);
	}
	if (text.startsWith("'") || text.startsWith("-")) {
		folder = text.charAt(1);
	} else {
		folder = text.charAt(0);
	}
		window.location.href = "../" + folder + "/" + text + ".html";
}
