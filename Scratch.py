from tinellb import *

t = Markdown()
page = ""
with open("dictionary_data.txt", "r") as f:
    for line in f:
        line = t.to_markdown(line)
        line = line.replace("{(- ", "(- {")
        line = line.replace("{-) ", "-) {")
        line = line.replace("{&uarr; ", "&uarr; {")
        line = line.replace("{&darr; ", "&darr; {")
        line = line.replace("{&mdash; ", "&mdash; {")
        line = t.to_markup(line)
        print(line)
        page += line
with open("dictionary_data.txt", "w") as g:
    g.write(page)