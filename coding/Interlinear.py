english = []
gloss = []
transliteration = []
page = ""
with open("English.txt", "r") as f:
    for line in f:
        english.append(line)
with open("Gloss.txt", "r") as f:
    for line in f:
        gloss.append(line[:-1])
with open("Transliteration.txt", "r") as f:
    for line in f:
        transliteration.append(line[:-1])
for e,g,t in zip(english, gloss, transliteration):
    page += "[t]" + e + "[r]"
    for t_word, g_word in zip(t.split(" "), g.split(" ")):
        page += "<table><tr>"
        split_word = t_word.split("-")
        for morpheme in split_word[:-1]:
            page += "<td>" + morpheme + "-</td>"
        page += "<td>" + split_word[-1] + "</td>"
        page += "</tr><tr>"
        split_word = g_word.split("-")
        for morpheme in split_word[:-1]:
            page += "<td>" + morpheme + "-</td>"
        page += "<td>" + split_word[-1] + "</td>"
        page += "</tr></table>"
    page += "\n[/t]\n"
with open("Interlinear.txt", "w") as f:
    f.write(page)
