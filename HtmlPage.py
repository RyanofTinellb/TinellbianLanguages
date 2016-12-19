from Directory import *
import os


class HtmlPage:
    def __init__(self, name, leaf_level):
        source_file = name + "_data.txt"
        self.template_file = name + "_template.txt"
        self.stylesheet = name + "_style.css"
        self.directory = Directory(name, leaf_level)
        self.root = self.directory.root
        self.name = name
        self.leaf_level = leaf_level
        self.content = []
        self.current = self.directory.root.next_node()
        self.create_main_page()
        with open(source_file, 'r') as source:
            for line in source:
                if line[0] == "[":
                    try:
                        self.level = int(line[1])
                        if self.level <= self.leaf_level and len(self.content):
                            self.create_page()
                            self.content = []
                            self.current = self.current.next_node()
                    except ValueError:
                        pass
                if line != "\n":
                    self.content.append(line[:-1])
                else:
                    self.content.append("<br>\n")
            self.create_page()

    def create_page(self):
        replacements = [["title", self.title], ["toc", self.toc], ["nav-footer", self.nav_footer],
                        ["stylesheet", self.stylesheet_and_icon], ["content", self.contents]]
        if self.name == "grammar":
            nav_header = self.nav_header_grammar
        elif self.name == "story":
            nav_header = self.nav_header_story
        elif self.name == "dictionary":
            nav_header = self.nav_header_dictionary
        else:
            nav_header = None
        replacements.append(["nav-header", nav_header])
        with open(self.template_file, 'r') as template:
            page = template.read()
        for placeholder, replacement in replacements:
            page = page.replace("{" + placeholder + "}", replacement())
        path = "/".join([node.url() for node in self.current.ancestors()])
        file_name = path + "/" + self.current.url(True)
        path += "/" + self.current.url() if self.current.generation() != self.leaf_level else ""
        try:
            os.makedirs(path)
        except os.error:
            pass
        with open(file_name, "w") as f:
            f.write(page)

    def title(self):
        ancestry = [self.sanitise(ancestor.name) for ancestor in self.current.ancestors()]
        ancestry.reverse()
        return self.sanitise(self.current.name) + " &lt; " + " &lt; ".join(ancestry)

    @staticmethod
    def sanitise(name):
        if "[" not in name and "<" not in name:
            return name
        bracket = False
        text = ""
        for character in name:
            if character in "[<":
                bracket = True
            elif character in "]>":
                bracket = False
            elif not bracket:
                text += character
        text = text.replace("&#x202e;", "")
        return text

    def toc(self):
        text = ""
        if self.current.generation() < self.leaf_level:
            for child in self.current.children:
                text += "<p>" + self.current.hyperlink(child) + "</p>\n"
        return text

    def top_level_links(self):
        text = ""
        subjects = ["grammar", "dictionary", "story"]
        subjects.remove(self.name)
        directions = ["left", "right"]
        arrows = ["&nwarr; $", "$ &nearr;"]
        for subject, direction, arrow, in zip(subjects, directions, arrows):
            text += "<div class=\"" + direction + "\">"
            text += self.current.hyperlink(subject + "/index.html", arrow.replace("$", subject.capitalize()))
            text += "</div>\n"
        return text

    def medium_level_links(self, minimum=0, maximum=10, no_sisters=None):
        no_sisters = [] if no_sisters is None else no_sisters
        text = ""
        ancestry = self.current.ancestors()
        ancestry.append(self.current)
        for count, ancestor in enumerate(ancestry[minimum:maximum+1]):
            for index, arrow, direction in zip([-1, 1], ["&#x2190; $", "$ &#x2192;"], ["left", "right"]):
                if count not in no_sisters:
                    try:
                        sister = ancestor.sister(index)
                        text += "<div class=\"" + direction + "\">" + self.current.hyperlink(sister, arrow) + "</div>\n"
                    except (IndexError, AttributeError):
                        pass
            if self.current is not ancestor:
                text += "<div class=\"centre\">" + self.current.hyperlink(ancestor) + "</div>\n"
        text += "<div style=\"clear: both;\"></div>\n"
        return text

    def nav_header_grammar(self):
        text = "<ul class=\"level-1\">" + "<li class=\"link\">" + self.current.hyperlink(self.root) + "</li>"
        node = self.root
        family = self.current.family()
        level = 1
        while True:
            if node in family:
                line = self.current.hyperlink(node)
            else:
                line = ""
            if node is self.current:
                line = "<span class=\"normal\">" + line + "</span>\n"
            if line:
                old_level = level
                level = node.generation()
                if level > old_level:
                    text += "<ul class=\"level-" + str(level) + "\">"
                elif level < old_level:
                    text += (old_level - level) * "</ul>\n"
                text += "<li>" + line + "</li>\n"
            try:
                node = node.next_node()
            except IndexError:
                break
        text += (level - 1) * "</ul>\n"
        text += "<li class=\"link\">" + self.current.hyperlink("Search.html", "Site Search") + "</li>"
        for link in ["story", "dictionary"]:
            text += "<li class=\"link\">" + self.current.hyperlink(link + "/index.html", link.capitalize()) + "</li>\n"
        text += "</ul>\n"
        return text

    def nav_header_story(self):
        text = "<ul><li>" + self.current.hyperlink("story/index.html", "Story") + "</li>"
        text += "<ul>"
        categories = [i.name for i in self.root.children]
        for cousin, category in zip(self.current.cousins(), categories):
            if self.current is cousin:
                continue
            text += "<li>" + self.current.hyperlink(cousin, category) + "</li>\n"
        text += "</ul>"
        text += "<li class=\"up-arrow\">" + self.current.hyperlink(self.current.parent, "Go up one level") + "</li>"
        text += "<li class=\"link\">" + self.current.hyperlink("Search.html", "Site Search") + "</li>"
        for link in ["grammar", "dictionary"]:
            text += "<li class=\"link\">" + self.current.hyperlink(link + "/index.html", link.capitalize()) + "</li>\n"
        text += "</ul>\n"
        return text

    def nav_header_dictionary(self):
        text = self.current.hyperlink(self.root) + "<br>"
        for child in self.root.children:
            if child is self.current:
                text += "<span class=\"normal\">" + child.name + "</span> \n"
            elif child is self.current.parent:
                text += "<span class=\"normal\">" + self.current.hyperlink(child) + "</span> \n"
            else:
                text += self.current.hyperlink(child) + " \n"
            if child.name == "K":
                text += "<span class=\"no-space\"> </span>"
        text += "<br>" + self.current.hyperlink("Search.html", "Site Search")
        for link in ["grammar", "story"]:
            text += "<br>" + self.current.hyperlink(link + "/index.html", link.capitalize())
        return text

    def nav_footer(self):
        text = "<div class=\"right\">"
        try:
            text += self.current.hyperlink(self.current.next_node(), "Next page &rarr;")
        except IndexError:
            text += self.current.hyperlink(self.root, "Return to Menu &uarr;")
        text += "</div>\n<div style=\"clear: both;\"></div>\n"
        return text

    def stylesheet_and_icon(self):
        text = "<link rel=\"stylesheet\" type=\"text/css\" "
        text += self.current.hyperlink(self.root.url() + "_style.css", "", True) + ">\n"
        text += "<link rel=\"icon\" type=\"image/png\" "
        text += self.current.hyperlink("favicon.png", "", True) + ">\n"
        return text

    def contents(self):
        text = ""
        in_table = 0
        in_list = False
        first_row = False
        u_list = []
        for line in self.content:
            if in_table:
                if line[:6] == "[r][t]":
                    first_row = False
                    in_table += 1
                    text += "</tr>\n<tr><td>\n<table><tr><td>" + line[6:] + "</td>\n"
                elif line[:3] == "[t]":
                    first_row = False
                    in_table += 1
                    text += "<table><tr><td>" + line[3:] + "</td>\n"
                elif line[:3] == "[r]" and in_table == 1:
                    first_row = False
                    text += "</tr>\n<tr><th>" + line[3:] + "</th>\n"
                elif line[:3] == "[r]":
                    first_row = False
                    text += "</tr>\n<tr><td>" + line[3:] + "</td>\n"
                elif line[:4] == "[/t]":
                    in_table -= 1
                    text += "</tr></table>\n"
                elif first_row:
                    text += "<th>" + line + "</th>"
                else:
                    text += "<td>" + line + "</td>"
            elif in_list:
                if line[:4] not in ["[/l]", "[/n]"]:
                    u_list.append(line)
                else:
                    text += self.make_list(u_list, line[2])
                    in_list = False
            elif line[0] == "[":
                try:
                    heading = int(line[1])
                    text += self.change_to_heading(heading, self.current.generation(), line[3:])
                except ValueError:
                    if line[:3] == "[t]":
                        in_table += 1
                        text += "<table><tr><th>" + line[3:] + "</th>"
                        first_row += 1
                    elif line[:3] in ["[l]", "[n]"]:
                        in_list = True
                        u_list = [line[3:]]
                    else:
                        text += self.markup(line)
            else:
                text += "<p>" + line + "</p>\n"
        return text

    @staticmethod
    def change_to_heading(heading, generation, line):
        level = str(heading - generation + 1)
        text = "<h" + level + ">" + line + "</h" + level + ">\n"
        return text

    @staticmethod
    def markup(line):
        category = line[1]
        line = line[3:]
        if category == "f":
            text = "<p class=\"example\">" + line + "</p>\n"
        elif category == "e":
            text = "<p class=\"example_no_lines\">" + line + "</p>\n"
        else:
            text = line + "\n"
        return text

    @staticmethod
    def make_list(u_list, table_type):
        if table_type == "l":
            table_type = "ul"
        elif table_type == "n":
            table_type = "ol"
        else:
            raise ValueError('Invalid Table Type')
        text = "<" + table_type + ">\n"
        for item in u_list:
            text += "<li>" + item + "</li>\n"
        text += "</" + table_type + ">\n"
        return text

    def create_main_page(self):
        node = self.root
        template_file = self.name + "_main_template.txt"
        destination_filename = self.name + "/index.html"
        text = ""
        level = 0
        with open(template_file, "r") as template:
            for line in template:
                line = line[:-1]
                if line != "{toc}":
                    text += line + "\n"
                else:
                    while True:
                        try:
                            node = node.next_node()
                            old_level = level
                            level = node.generation()
                        except IndexError:
                            break
                        if level > old_level:
                            text += "<ul class=\"level-" + str(level) + "\">"
                        elif level < old_level:
                            text += (old_level - level) * "</ul>\n"
                        text += "<li>" + self.root.hyperlink(node) + "</li>\n"
                    text += level * "</ul>\n"
        try:
            os.makedirs(self.name)
        except os.error:
            pass
        with open(destination_filename, "w") as destination_file:
            destination_file.write(text)


def create_search():
    word_list = {}
    for name, leaf_level in [["grammar", 3], ["dictionary", 2], ["story", 3]]:
        level = 0
        directory = Directory(name, leaf_level)
        node = directory.root
        with open(name + "_data.txt", "r") as f:
            page = f.read()
            unaltered_page = page.replace('"', "##")
        page = page.lower()
        page = page.replace("&rsquo;", "'")
        page = page.replace("&igrave;", "i")
        page = page.replace("&ecirc;", "e")
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
                if word in ["", "&rarr", "&larr", "&darr", "&uarr", "&mdash"]:
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
