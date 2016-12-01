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
        self.directory = Directory(source_file, destination)
        self.destination = destination
        self.template_file = template_file
        self.leaf_level = leaf_level
        self.content = []
        self.node = self.directory.hierarchy.root
        self.stylesheet = stylesheet
        self.create_main_page()
        with open(source_file, 'r') as source:
            line = source.readline()
            while line != "":
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
                line = source.readline()
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
                    page += self.get_nav_header()
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
        ancestry = [i.name for i in self.heading_node.get_ancestors()]
        ancestry.reverse()
        return self.heading_node.name + " &lt; " + " &lt; ".join(ancestry)

    def get_toc(self):
        text = ""
        if self.heading_node.get_generation() < self.leaf_level:
            if self.heading_node.get_generation() < (self.leaf_level - 1):

                for child in self.heading_node.get_children():
                    text += "<p><a href=\"" + self.name_in_url_form(child) + "/index.html\">"
                    text += child.name + " &#x2192;</a></p> "
            else:
                for child in self.heading_node.get_children():
                    text += "<p><a href=\"" + self.name_in_url_form(child) + ".html\">"
                    text += child.name + " &#x2192;</a></p> "
        return text

    def get_nav_header(self):
        text = ""
        ancestry = self.heading_node.get_ancestors()
        ancestry = ancestry[1:]
        for ancestor in ancestry:
            level = ancestor.get_generation()
            if level < self.leaf_level:
                file_name = "/index.html"
            else:
                file_name = ".html"
            level = self.leaf_level - level
            text += "<p><a href=\"" + (level * "../") + self.name_in_url_form(ancestor) + file_name + "\">"
            text += ancestor.name + "</a></p>\n"
        level = self.heading_node.get_generation()
        sisters = []
        if level < self.leaf_level:
            file_name = "../$/index.html"
        else:
            file_name = "$.html"
        for index, arrow, direction in zip([-1, 1], ["&#x2190; $", "$ &#x2192;"], ["left", "right"]):
            try:
                sister = self.heading_node.get_sister(index)
                nav = "<p class=\"" + direction + "\"><a href=\""
                nav += file_name.replace("$", self.name_in_url_form(sister))
                nav += "\">"
                nav += arrow.replace("$", sister.name)
                nav += "</a></p>"
                text += nav
            except IndexError:
                pass
        text += "<div style=\"clear: both;\"></div>"
        return text

    def get_nav_footer(self):
        level = self.heading_node.get_generation()
        text = ""
        if level < self.leaf_level:
            text += "<p class=\"left\">"
            text += "<a href=\"../index.html\">"
            text += "&#x2191; Go up one level</a></p>\n"
        else:
            text += "<p class=\"left\">"
            text += "<a href=\"index.html\">"
            text += "&#x2191; Go up one level</a></p>\n"
        try:
            node = self.heading_node.get_next_node(self.leaf_level)
        except IndexError:
            text += "<p class=\"right\"><a href=\"" + (level - 1) * "../"
            text += "index.html\">"
            text += "Return to index &#x2191;</a></p>"
            text += "<div style=\"clear: both;\"></div>"
            return text
        next_level = node.get_generation()
        if next_level == self.leaf_level:
            file_name = ".html"
        else:
            file_name = "/index.html"
        text += "<p class=\"right\"><a href=\"" + max((level - next_level),0) * "../"
        text += self.name_in_url_form(node) + file_name + "\">"
        text += "Next Page &#x2192;</a></p>"
        text += "<div style=\"clear: both;\"></div>"
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
                if line[:4] != "[\\t]":
                    table.append(line)
                else:
                    text += self.make_table(table)
                    in_table = False
            elif in_list:
                if line[:4] not in ["[\\l]", "[\\n]"]:
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
        name = name.replace(" ", "")
        name = name.replace("&#x294;", "''")
        name = name.replace("&#x2019;", "'")
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
            line = template.readline()
            while line != "":
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
                line = template.readline()
        with open(destination_filename, "w") as destination_file:
            destination_file.write(text)
