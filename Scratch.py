filename = "dictionary_data.txt"
with open (filename, "r") as f:
    page = f.read()
page = page.replace("/<high-lulani>", "</high-lulani>")
with open (filename, "w") as g:
    g.write(page)