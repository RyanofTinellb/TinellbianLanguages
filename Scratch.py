page = ""
next_line = False
with open("dictionary_data.txt", "r") as f:
    for line in f:
        if line[:3] == "[6]":
            line = line[:-1] + "<div class=\"definition\">"
            next_line = True
        elif next_line:
            next_line = False
            line = line[:-1] + "</div>\n"
        page += line

with open("dictionary_data.txt", "w") as g:
    g.write(page)

