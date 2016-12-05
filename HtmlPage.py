from Directory import *
import os


class HtmlPage:
    # @param source_file (string): name of the markdown file
    # @param destination (string): name of the highest level folder to create
    # @param template_file (string): path to the template from which to build new pages
    # @param leaf_level (integer): the heading number for leaves of the directory
    # @param stylesheet (string): name of the css stylesheet
    def __init__(self, destination, leaf_level):
        source_file = destination + "_data.txt"
        template_file = destination + "_template.txt"
        stylesheet = destination + "_style.css"
        self.alphabet = "aiupbtdcjkgmnqlrfsxh"
        self.directory = Directory(source_file, destination.capitalize())
        self.root = self.directory.get_root()
        self.destination = destination
        self.template_file = template_file
        self.leaf_level = leaf_level
        self.content = []
        self.node = self.directory.hierarchy.root
        self.stylesheet = stylesheet
        self.create_main_page()
        with open(source_file, 'r') as source:
            for line in source:
                if line[0] == "[":
                    try:
                        self.level = int(line[1])
                        if self.level <= self.leaf_level:
                            self.create_page()
                            self.content = []
                        self.node = self.directory.get_next_node(self.leaf_level)
                        if self.node.get_generation() <= leaf_level:
                            self.heading_node = self.node
                    except ValueError:
                        pass
                if line != "\n":
                    self.content.append(line[:-1])
                else:
                    self.content.append("<br>\n")
            self.create_page()

    def create_page(self):
        if len(self.content) == 0:
            return
        heading = int(self.content[0][1])
        with open(self.template_file, 'r') as template:
            page = ""
            text = template.readline()
            while text != "":
                text = text[:-1]
                if text[0] != "{":
                    page += text + "\n"
                elif text == "{title}":
                    page += self.get_title()
                elif text == "{toc}":
                    page += self.get_toc()
                elif text == "{nav-header}":
                    if self.destination == "grammar":
                        page += self.get_nav_header_grammar()
                    elif self.destination == "story":
                        page += self.get_nav_header_story()
                    elif self.destination == "dictionary":
                        page += self.get_nav_header_dictionary()
                    else:
                        pass
                elif text == "{nav-footer}":
                    page += self.get_nav_footer()
                elif text == "{stylesheet}":
                    page += self.get_stylesheet()
                elif text == "{content}":
                    page += self.get_content()
                text = template.readline()
        if heading < self.leaf_level:
            path = "/".join([self.name_in_url_form(node) for node in self.heading_node.get_ancestors()])
            path += "/" + self.name_in_url_form(self.heading_node)
            file_name = path + "/index.html"
        else:
            path = "/".join([self.name_in_url_form(node) for node in self.heading_node.get_ancestors()])
            file_name = path + "/" + self.name_in_url_form(self.heading_node) + ".html"
        try:
            os.makedirs(path)
        except os.error:
            pass
        with open(file_name, "w") as f:
            f.write(page)

    def get_title(self):
        ancestry = [self.sanitise(i.name) for i in self.heading_node.get_ancestors()]
        ancestry.reverse()
        return self.sanitise(self.heading_node.name) + " &lt; " + " &lt; ".join(ancestry)

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

    def get_toc(self):
        text = ""
        if self.heading_node.get_generation() < self.leaf_level:
            if self.heading_node.get_generation() < (self.leaf_level - 1):
                file_name = "/index.html"
            else:
                file_name = ".html"
            for child in self.heading_node.get_children():
                text += "<p><a href=\"" + self.name_in_url_form(child) + file_name + "\">"
                text += child.name + "</a></p>\n"
        return text

    def get_nav_header_grammar(self):
        text = ""
        level = self.heading_node.get_generation()
        ancestry = self.heading_node.get_ancestors()
        # top-level links
        for subject, direction, arrow, in \
                zip(["dictionary", "story"], ["left", "right"], ["&nwarr; $", "$ &nearr;"]):
            text += "<div class=\"" + direction + "\"><a href=\"" + (level + (level != self.leaf_level)) * "../"
            text += subject + "/index.html\">" + arrow.replace("$", subject.capitalize()) + "</a></div>\n"
        # medium-level side links
        for ancestor_level, ancestor in enumerate(ancestry):
            for index, arrow, direction in zip([-1, 1], ["&#x2190; $", "$ &#x2192;"], ["left", "right"]):
                try:
                    sister = ancestor.get_sister(index)
                    nav = "<div class=\"" + direction + "\"><a href=\""
                    nav += (level - ancestor_level + (level != self.leaf_level)) * "../"
                    nav += self.name_in_url_form(sister)
                    nav += "/index.html\">"
                    nav += arrow.replace("$", sister.name)
                    nav += "</a></div>\n"
                    text += nav
                except (IndexError, AttributeError):
                    pass
            text += "<div class=\"centre\"><a href=\""
            text += (level - ancestor_level - (level == self.leaf_level)) * "../"
            text += "index.html\">" + ancestor.name + "</a></div>\n"
        if level < self.leaf_level:
            file_name = "../$/index.html"
        else:
            file_name = "$.html"
        for index, arrow, direction in zip([-1, 1], ["&#x2190; $", "$ &#x2192;"], ["left", "right"]):
            try:
                sister = self.heading_node.get_sister(index)
                nav = "<div class=\"" + direction + "\"><a href=\""
                nav += file_name.replace("$", self.name_in_url_form(sister))
                nav += "\">"
                nav += arrow.replace("$", sister.name)
                nav += "</a></div>\n"
                text += nav
            except IndexError:
                pass
        text += "<div style=\"clear: both;\"></div>"
        return text

    def get_nav_header_story(self):
        text = ""
        level = self.heading_node.get_generation()
        # top-level links
        for subject, direction, arrow, in \
                zip(["grammar", "dictionary"], ["left", "right"], ["&nwarr; $", "$ &nearr;"]):
            text += "<div class=\"" + direction + "\"><a href=\"" + (level + (level != self.leaf_level)) * "../"
            text += subject + "/index.html\">" + arrow.replace("$", subject.capitalize()) + "</a></div>\n"
        # medium-level side links
        text += "<div class=\"centre\"><a href=\""
        text += (level - (level == self.leaf_level)) * "../"
        text += "index.html\">Story</a></div>\n"
        text += "<div class=\"cousins\">"
        categories = [i.name for i in self.root.children]
        for cousin, category in zip(self.heading_node.get_cousins(), categories):
            if self.heading_node is cousin:
                continue
            text += "<a href=\"" + (level - (level == self.leaf_level)) * "../"
            ancestors = cousin.get_ancestors()
            ancestors.pop(0)
            for ancestor in ancestors:
                text += self.name_in_url_form(ancestor) + "/"
            text += self.name_in_url_form(cousin)
            if level == self.leaf_level:
                text += ".html\">"
            else:
                text += "/index.html\">"
            text += category + "</a>\n"
        text += "</div>"
        if level >= 2:
            ancestry = self.heading_node.get_ancestors()
            ancestry.pop(0)
            # medium-level side links
            for a_level, ancestor in enumerate(ancestry):
                ancestor_level = a_level + 1
                if a_level:
                    for index, arrow, direction in zip([-1, 1], ["&#x2190; $", "$ &#x2192;"], ["left", "right"]):
                        try:
                            sister = ancestor.get_sister(index)
                            nav = "<div class=\"" + direction + "\"><a href=\""
                            nav += (level - ancestor_level + (level != self.leaf_level)) * "../"
                            nav += self.name_in_url_form(sister)
                            nav += "/index.html\">"
                            nav += arrow.replace("$", sister.name)
                            nav += "</a></div>\n"
                            text += nav
                        except (IndexError, AttributeError):
                            pass
                text += "<div class=\"centre\"><a href=\""
                text += (level - ancestor_level - (level == self.leaf_level)) * "../"
                text += "index.html\">" + ancestor.name + "</a></div>\n"
            if level < self.leaf_level:
                file_name = "../$/index.html"
            else:
                file_name = "$.html"
            for index, arrow, direction in zip([-1, 1], ["&#x2190; $", "$ &#x2192;"], ["left", "right"]):
                try:
                    sister = self.heading_node.get_sister(index)
                    nav = "<div class=\"" + direction + "\"><a href=\""
                    nav += file_name.replace("$", self.name_in_url_form(sister))
                    nav += "\">"
                    nav += arrow.replace("$", sister.name)
                    nav += "</a></div>\n"
                    text += nav
                except IndexError:
                    pass
            text += "<div style=\"clear: both;\"></div>"
        return text

    def get_nav_header_dictionary(self):
        text = ""
        level = self.heading_node.get_generation()
        ancestry = self.heading_node.get_ancestors()
        # top-level links
        for subject, direction, arrow, in \
                zip(["grammar", "story"], ["left", "right"], ["&nwarr; $", "$ &nearr;"]):
            text += "<div class=\"" + direction + "\"><a href=\"" + (level + (level != self.leaf_level)) * "../"
            text += subject + "/index.html\">" + arrow.replace("$", subject.capitalize()) + "</a></div>\n"
        text += "<div class=\"centre\"><a href=\"../index.html\">Dictionary</a></div>\n"
        text += "<div class=\"justify\">\n"
        name = self.name_in_url_form(self.heading_node)
        initial = ""
        for character in name:
            if character in self.alphabet:
                initial = character
                break
        for letter in self.alphabet:
            if letter != initial:
                text += "<a href=\"../" + letter + "/index.html\">" + letter.capitalize() + "</a> \n"
            elif level != self.leaf_level:
                text += "<span class=\"normal\">" + letter.capitalize() + "</span> "
            else:
                text += "<a href=\"../" + letter + "/index.html\"><span class=\"normal\">"
                text += letter.capitalize() + "</span></a> \n "
        text += "</div>\n"
        if level < self.leaf_level:
            file_name = "../$/index.html"
        else:
            file_name = "$.html"
        for index, arrow, direction in zip([-1, 1], ["&#x2190; $", "$ &#x2192;"], ["left", "right"]):
            try:
                sister = self.heading_node.get_sister(index)
                nav = "<div class=\"" + direction + "\"><a href=\""
                nav += file_name.replace("$", self.name_in_url_form(sister))
                nav += "\">"
                nav += arrow.replace("$", sister.name)
                nav += "</a></div>\n"
                text += nav
            except IndexError:
                pass
        text += "<div style=\"clear: both;\"></div>"
        return text

    def get_nav_footer(self):
        level = self.heading_node.get_generation()
        text = ""
        if level < self.leaf_level:
            text += "<div class=\"left\">"
            text += "<a href=\"../index.html\">"
            text += "&#x2191; Go up one level</a></div>\n"
        else:
            text += "<div class=\"left\">"
            text += "<a href=\"index.html\">"
            text += "&#x2191; Go up one level</a></div>\n"
        try:
            node = self.heading_node.get_next_node(self.leaf_level)
        except IndexError:
            text += "<div class=\"right\"><a href=\"" + (level - 1) * "../"
            text += "index.html\">"
            text += "Return to index &#x2191;</a></div>\n"
            text += "<div style=\"clear: both;\"></div>\n"
            return text
        next_level = node.get_generation()
        if next_level == self.leaf_level:
            file_name = ".html"
        else:
            file_name = "/index.html"
        text += "<div class=\"right\"><a href=\"" + max((level - next_level), 0) * "../"
        text += self.name_in_url_form(node) + file_name + "\">"
        text += "Next Page &#x2192;</a></div>\n"
        text += "<div style=\"clear: both;\"></div>\n"
        return text

    def get_stylesheet(self):
        generation = self.heading_node.get_generation()
        if generation < self.leaf_level:
            levels = generation + 1
        else:
            levels = generation
        line = "<link rel=\"stylesheet\" type=\"text/css\" href=\""
        line += levels * "../"
        line += self.stylesheet + "\">\n"
        line += "<link rel=\"icon\" type=\"image/png\" href=\""
        line += levels * "../" + "favicon.png\">\n"
        return line

    def get_content(self):
        text = ""
        in_table = False
        in_list = False
        table = []
        u_list = []
        generation = self.heading_node.get_generation()
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
                    text += self.change_to_heading(heading, generation, line[3:])
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
        level = "h" + str(heading - generation + 1) + ">"
        text = "<" + level + line + "</" + level + "\n"
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
    def name_in_url_form(node):
        name = node.name
        name = name.lower()
        name = name.replace("&#x294;", "''")
        name = name.replace("&#x2019;", "'")
        name = name.replace("&rsquo;", "'")
        name = name.replace("&#x202e;", "")
        for character in ["<span class=\"tinellbian\">", "</span>", "<small-caps>", "</small-caps>", "/", ".", ";",
                          " "]:
            name = name.replace(character, "")
        return name

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
        text = ""
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
        node = self.directory.get_root()
        node = node.get_next_node()
        template_file = self.destination + "_main_template.txt"
        destination_filename = self.destination + "/index.html"
        text = ""
        with open(template_file, "r") as template:
            for line in template:
                line = line[:-1]
                if line != "{toc}":
                    text += line + "\n"
                else:
                    while True:
                        generation = node.get_generation()
                        ancestors = node.get_ancestors()
                        ancestors.pop(0)
                        if generation < self.leaf_level:
                            new_file = "/index.html"
                        else:
                            new_file = ".html"
                        text += "<h" + str(generation) + "><a href=\""
                        for ancestor in ancestors:
                            text += self.name_in_url_form(ancestor) + "/"
                        text += self.name_in_url_form(node) + new_file + "\">"
                        text += node.get_name() + "</a></h" + str(generation) + ">\n"
                        try:
                            node = node.get_next_node(self.leaf_level)
                        except IndexError:
                            break
        try:
            os.makedirs(self.destination)
        except os.error:
            pass
        with open(destination_filename, "w") as destination_file:
            destination_file.write(text)
