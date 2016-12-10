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
        text = self.top_level_links()
        text += self.medium_level_links(0, 3)
        return text

    def nav_header_story(self):
        text = self.top_level_links()
        # medium-level side links
        text += "<div class=\"centre\">" + self.current.hyperlink(self.root) + "</div>\n"
        text += "<div class=\"cousins\">"
        categories = [i.name for i in self.root.children]
        for cousin, category in zip(self.current.cousins(), categories):
            if self.current is cousin:
                continue
            text += self.current.hyperlink(cousin, category) + "\n"
        text += "</div>"
        if self.current.generation() >= 2:
            text += self.medium_level_links(1, 10, [0])
        return text

    def nav_header_dictionary(self):
        text = self.top_level_links()
        for child in self.root.children:
            if child is self.current:
                text += "<span class=\"normal\">" + child.name + "</span>"
            elif child is self.current.parent:
                text += "<span class=\"normal\">" + self.current.hyperlink(child) + "</span> \n"
            else:
                text += self.current.hyperlink(child) + " \n"
        text += "</div>\n"
        return text

    def nav_footer(self):
        text = "<div class=\"left\">" + self.current.hyperlink(self.current.parent, "&uarr; Go up one level") + "</div>"
        text += "<div class=\"right\">"
        try:
            text += self.current.hyperlink(self.current.next_node(), "Next page &rarr;")
        except IndexError:
            text += self.current.hyperlink(self.root)
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
        in_table = False
        in_list = False
        table = []
        u_list = []
        for line in self.content:
            if in_table:
                if line[:4] != "[/t]":
                    table.append(line)
                else:
                    text += self.make_table(table)
                    in_table = False
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
                        in_table = True
                        table = [line[3:]]
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
    def make_table(table):
        text = "<table>\n<tr>\n"
        first_row = True
        for cell in table:
            if cell[:3] == "[r]":
                text += "</tr>\n<tr>\n<th>"
                text += cell[3:] + "</th>\n"
                first_row = False
            else:
                if not first_row:
                    text += "<td>" + cell + "</td>\n"
                else:
                    text += "<th>" + cell + "</th>\n"
        text += "</tr>\n</table>"
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
        with open(template_file, "r") as template:
            for line in template:
                line = line[:-1]
                if line != "{toc}":
                    text += line + "\n"
                else:
                    while True:
                        try:
                            node = node.next_node()
                        except IndexError:
                            break
                        text += "<h" + str(node.generation()) + ">"
                        text += self.root.hyperlink(node)
                        text += "</h" + str(node.generation()) + ">\n"
        try:
            os.makedirs(self.name)
        except os.error:
            pass
        with open(destination_filename, "w") as destination_file:
            destination_file.write(text)
