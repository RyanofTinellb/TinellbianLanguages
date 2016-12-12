page = ""
with open("dictionary_data.txt", "r") as g:
    for line in g:
        if line.startswith("[4]&#x202e;"):
            line = line.replace("&#x202e;", "<high-lulani>") + "</high-lulani>"
        page += line
with open("dictionary_data.txt", "w") as f:
    f.write(page)