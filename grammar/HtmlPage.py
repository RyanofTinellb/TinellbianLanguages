from Directory import *


class HtmlPage:
    def __init__(self, name, source_file, destination, template):
        self.directory = Directory(source_file, name)
        with open(source_file, 'r') as source:
            line = " "
            text = ""
            while line != "":
                line = source.readline()
                if line[0] == "[":
                    try:
                        level = int(line[1])
                        if level < 3:
                            text += self.new_page(level, line, template)
                    except ValueError:
                        text += self.continue_page(line)

    @staticmethod
    def new_page(level, line, template_file):
        with open()
        with open(template_file, 'r') as template:
            text = " "
            while text != "":
                text = template.readline()
        return "Hey!"

    @staticmethod
    def continue_page(line):
        return "Hey!"
