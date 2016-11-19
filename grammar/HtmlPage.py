from Directory import *


class HtmlPage:
    def __init__(self, name, source_file, destination, template):
        self.directory = Directory(source_file, name)
        with open(source_file, 'r') as source:
            line = source.readline()
            text = ""
            node = self.directory.hierarchy.root
            while line != "":
                print(line)
                if line[0] == "[":
                    try:
                        level = int(line[1])
                        if level < 3:
                            text += self.new_page(level, line, template, node)
                    except ValueError:
                        text += self.continue_page(line)
                line = source.readline()

    @staticmethod
    def new_page(level, line, template_file, node):
        with open(template_file, 'r') as template:
            page = ""
            text = template.readline()
            while text != "":
                if text[0] != "{":
                    page += text
                elif text == "{title}":
                    page += self.get_title(node)
                text = template.readline()
        return page

    @staticmethod
    def continue_page(line):
        return "Hey!"

    @staticmethod
    def get_title(node):