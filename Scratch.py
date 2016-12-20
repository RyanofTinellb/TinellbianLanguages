page = ""
with open("dictionary_data.txt", "r") as f:
    for line in f:
        page += line + (line[:3] == "[6]") * "<span class=\"hidden\"></span>"
with open("dictionary_data.txt", "w") as g:
    g.write(page)

