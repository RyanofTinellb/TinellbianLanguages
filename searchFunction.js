function dictionarysearch() {
	var text;
	var folder;
	var x;
	text = document.getElementById("search").value.toLowerCase();
	text = text.trim().replace(/[\u2019]/g, "'")
	text = text.replace(/[\u0294\u0660]/g, "''")
	for (var i = 0; i < text.length; i++) {
		x = text.charCodeAt(i)
		console.log(x)
	}
	if (text.startsWith("'")) {
	folder = text.charAt(1);
	} else {
	folder = text.charAt(0); }
	window.location.href = "../" + folder + "/" + text + ".html";
}