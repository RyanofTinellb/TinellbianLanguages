from Hierarchy import *


class Directory:
    def __init__(self, main_file, name):
        self.main_file = main_file
        self.name = name
        with open(main_file, 'r') as source:
            self.hierarchy = Hierarchy(name)
            current_chapter = [self.hierarchy.root]
            line = source.readline()
            while line != "":
                if line[0] == "[":
                    try:
                        level = int(line[1])
                        heading = line[3:-1]
                    except ValueError:
                        line = source.readline()
                        continue
                    if level == len(current_chapter):
                        node = self.hierarchy.add_node(current_chapter[-1], heading)
                        current_chapter.append(node)
                    elif level < len(current_chapter):
                        current_chapter = current_chapter[:level]
                        node = self.hierarchy.add_node(current_chapter[-1], heading)
                        current_chapter.append(node)
                    else:
                        raise ValueError('We\'ve skipped a level, somewhere')
                line = source.readline()

    def get_next_node(self, level):
        return self.hierarchy.get_next_node()
