class Hierarchy:
    def __init__(self, name):
        self.root = Node(name)
        self.nodes = []

    def add_node(self, parent, name):
        if name not in parent.get_children_names():
            child = Node(name, parent)
            parent.children.append(child)
            self.nodes.append(child)
            return child

    def delete_node(self, node):
        node.parent.children.remove(node)
        self.nodes.remove(node)


    def get_node_names(self, name=""):
        node = self.get_node_names_iter(self.root, name)
        return node

    def get_node_names_iter(self, node, name):
        print(node.name)
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
    @staticmethod
    def get_sister(node, index):
        children = node.parent.children
        node_order = children.index(node)
        if len(children) > node_order + index:
            return children[node_order + index]
        else:
            return None

    def get_left_sister(self, node):
        return self.get_sister(node, -1)

    def get_right_sister(self, node):
        return self.get_sister(node, 1)


class Node:
    def __init__(self, name, parent=None):
        self.parent = parent
        self.name = name
        self.children = []

    def get_name(self):
        return self.name

    def get_children(self):
        return self.children

    def get_children_names(self):
        return [child.name for child in self.children]

    def get_parent(self):
        return self.parent

    def get_ancestry(self):
        node = self
        ancestry = []
        while node.parent is not None:
            ancestry.insert(0, node)
            node = node.parent
        return ancestry
