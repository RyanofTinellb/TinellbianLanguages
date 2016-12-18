from Directory import *

word_list = {}
for name, leaf_level in [["grammar", 3], ["story", 3], ["dictionary", 2]]:
    level = 0
    directory = Directory(name, leaf_level)
    node = directory.root
    with open(name + "_data.txt", "r") as f:
        page = f.read()
        unaltered_page = page.replace('"', "##")
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
    while True:
        place = unaltered_page.find("<high-lulani>")
        other = unaltered_page.find("</high-lulani>")
        if place == -1:
            break
        unaltered_page = unaltered_page[:place] + unaltered_page[(other + 14):]
    while True:
        place = unaltered_page.find("<ipa>")
        other = unaltered_page.find("</ipa>")
        if place == -1:
            break
        unaltered_page = unaltered_page[:place] + unaltered_page[(other + 6):]
    page = page.split("\n")
    unaltered_page = unaltered_page.split("\n")
    for num, line_text in enumerate(zip(page, unaltered_page)):
        line, text = line_text
        if line == "":
            continue
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
        while True:
            place = text.find("[")
            other = text.find("]")
            if place == -1:
                break
            text = text[:place] + text[(other + 1):]
        while True:
            place = text.find("<")
            other = text.find(">")
            if place == -1:
                break
            text = text[:place] + text[(other + 1):]
        line = line.split(" ")
        for word in line:
            if word == "":
                continue
            extension = "/index.html" if node.generation() < leaf_level else ".html"
            link = "{\"url\": \"" + "/".join([i.url() for i in node.ancestors()]) + "/"
            link += node.url() + extension + "\", \"name\": \"" + node.name + "\", \"line\": \"" + text
            link += "\", \"num\": " + str(num) + "}"
            if word[:2] == "''":
                word = word[1:]
            if word in word_list:
                word_list[word].add(link)
            else:
                word_list[word] = {link}
dictionary_list = []
for word, links in word_list.items():
    links = list(links)
    links.sort()
    entry = "{\"term\": \"" + word + "\", \"results\": [" + ", ".join(links) + "]\n}"
    dictionary_list.append(entry)
dictionary_list.sort()
text = str("[" + ",\n".join(dictionary_list) + "]\n")
with open("searching.json", "w") as g:
    g.write(text)
