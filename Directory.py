import os


class Directory:
    def __init__(self, name, leaf_level=3):
        os.chdir("c:/users/ryan/documents/tinellbianlanguages/" + name)
        source_file = "data.txt"
        with open(source_file, 'r') as source:
            self.hierarchy = Hierarchy(name.capitalize(), leaf_level)
            self.root = current = self.hierarchy.root
            for line in source:
                if line[0] == "[":
                    try:
                        level = int(line[1])
                        if level > leaf_level:
                            continue
                        heading = line[3:-1]
                    except ValueError:
                        continue
                    if level == current.generation() + 1:
                        current = self.hierarchy.add_node(current, heading)
                    elif level <= current.generation():
                        while level != current.generation() + 1:
                            current = current.parent
                        current = self.hierarchy.add_node(current, heading)
                    else:
                        continue


class Hierarchy:
    def __init__(self, name, leaf_level):
        self.root = Node(name, None, leaf_level)
        self.leaf_level = leaf_level

    def add_node(self, parent, name):
        child = Node(name, parent, self.leaf_level)
        parent.children.append(child)
        return child

    def get_node_names(self, name=""):
        node = self.get_node_names_iter(self.root, name)
        return node

    def get_node_names_iter(self, node, name):
        if node.name == name:
            return node
        else:
            for child in node.children:
                if child.name == name:
                    return child
                else:
                    node = self.get_node_names_iter(child, name)
                    if node:
                        return node


class Node:
    def __init__(self, name, parent, leaf_level=3):
        self.parent = parent
        self.name = name
        self.children = []
        self.leaf_level = leaf_level

    def delete(self):
        self.parent.children.remove(self)

    def url(self, extend=False):
        name = self.name.lower()
        name = name.replace("&#x294;", "''")
        for character in ("&#x2019;", "&rsquo;"):
            name = name.replace(character, "'")
        for character in ["<high-lulani>", "</high-lulani>", "<small-caps>", "</small-caps>", "/", ".", ";", " "]:
            name = name.replace(character, "")
        extension = ".html" if self.generation() == self.leaf_level else "/index.html"
        return name + extension if extend else name

    def has_children(self):
        return len(self.children) > 0

    def ancestors(self):
        node = self
        ancestry = []
        while node.parent is not None:
            node = node.parent
            ancestry.insert(0, node)
        return ancestry

    # @return: how deep in the tree the particular node is
    def generation(self):
        return len(self.ancestors())

    def sister(self, index):
        children = self.parent.children
        node_order = children.index(self)
        if len(children) > node_order + index >= 0:
            return children[node_order + index]
        else:
            raise IndexError('No such sister')

    def previous_sister(self):
        return self.sister(-1)

    def next_sister(self):
        return self.sister(1)

    def next_node(self):
        if self.has_children():
            return self.children[0]
        else:
            try:
                next_node = self.next_sister()
            except IndexError:
                next_node = self.next_node_iter(self.parent)
        return next_node

    def next_node_iter(self, node):
        if node.parent is None:
            raise IndexError('No more nodes')
        try:
            right = node.next_sister()
            return right
        except IndexError:
            right = self.next_node_iter(node.parent)
        return right

    def descendants(self):
        descendants = set(self.children)
        for child in self.children:
            descendants.update(child.descendants())
        return descendants

    # returns self, descendants, ancestors and sisters of ancestors
    def family(self):
        family = set([])
        for ancestor in self.ancestors():
            family.update(ancestor.children)
        family.update(self.descendants())
        return family

    def cousins(self):
        node = self
        indices = []
        while node.parent is not None:
            indices.insert(0, node.parent.children.index(node))
            node = node.parent
        indices.pop(0)
        cousins = []
        for child in node.children:
            cousin = child
            for index in indices:
                cousin = cousin.children[index]
            cousins.append(cousin)
        return cousins

    # @param destination (as Node): the page being linked to
    # source and destination must be within the same hierarchy
    def hyperlink(self, destination, template="$", just_href=False):
        if self is destination:
            return template.replace("$", destination.name)
        change = 0 if self.generation() == self.leaf_level else 1
        try:

            extension = ".html" if destination.generation() == self.leaf_level else "/index.html"
            self_ancestors = self.ancestors() + [self]
            destination_ancestors = destination.ancestors() + [destination]
            ancestor_list = zip(self_ancestors, destination_ancestors)
            direct = destination in self_ancestors
            try:
                common = [i != j for i, j in ancestor_list].index(True)
            except ValueError:
                common = len(ancestor_list)
            down = destination.url() if direct else "/".join([node.url() for node in destination_ancestors[common:]])
            up = self.generation() + change - (destination.generation() if direct else common)
            href = "href=\"" + up * "../" + down + extension + "\""
            link = "<a " + href + ">" + template.replace("$", destination.name) + "</a>"
        except AttributeError:
            up = self.generation() + change
            href = "href=\"" + up * "../" + destination + "\""
            link = "<a " + href + ">" + template.replace("$", destination) + "</a>"
        return href if just_href else link
