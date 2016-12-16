function dictionarysearch() {
	var text;
	var folder;
	text = document.getElementById("search").value.toLowerCase();
	if (text.startsWith("'")) {
	folder = text.charAt(1);
	} else {
	folder = text.charAt(0); }
	window.location.href = "../" + folder + "/" + text + ".html";
}