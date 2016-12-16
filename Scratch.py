from Directory import *

word_list = {}
for name, leaf_level in [["grammar", 3], ["story", 3], ["dictionary", 2]]:
    level = 0
    directory = Directory(name, leaf_level)
    node = directory.root
    with open(name + "_data.txt", "r") as f:
        page = f.read()
    page = page.lower()
    page = page.replace("&rsquo;", "'")
    page = page.replace("&igrave;", "i")
    page = page.replace("&ldquo;", " ")
    page = page.replace("&rdquo;", " ")
    page = page.replace("&#x294;", "''")
    punctuation = '*?!.,;:()-^='
    for character in punctuation:
        page = page.replace(character, " ")
    while True:
        place = page.find("<high lulani>")
        other = page.find("</high lulani>")
        if place == -1:
            break
        page = page[:place] + page[(other + 14):]
    while True:
        place = page.find("<ipa>")
        other = page.find("</ipa>")
        if place == -1:
            break
        page = page[:place] + page[(other + 6):]
    page = page.split("\n")
    for line in page:
        if line == "":
            continue
        print(line)
        if line[0] == "[":
            try:
                level = int(line[1])
                if level <= leaf_level:
                    node = node.next_node()
            except ValueError:
                pass
        while True:
            place = line.find("[")
            other = line.find("]")
            if place == -1:
                break
            line = line[:place] + line[(other + 1):]
        while True:
            place = line.find("<")
            other = line.find(">")
            if place == -1:
                break
            line = line[:place] + line[(other + 1):]
        line = line.split(" ")
        for word in line:
            extension = "/index.html" if node.generation() < leaf_level else ".html"
            link = "<a href=\""
            link += "/".join([i.url() for i in node.ancestors()]) + "/" + node.url() + extension
            link += "\">" + node.url() + "</a>"
            if word[:2] == "''":
                word = word[1:]
            if word in word_list:
                word_list[word].add(link)
            else:
                word_list[word] = {link}
dictionary_list = []
for word, links in word_list.items():
    dictionary_list.append("<div class=\"" + word + "\">" + word + ":\n" + "\n".join(links) + "</div>\n\n")
dictionary_list.sort()
text = "".join(dictionary_list)
with open("Searching.html", "w") as g:
    g.write(text)
