class Hierarchy:
    def __init__(self, name):
        self.root = Node(name)
        self.nodes = []
        self.node_index = -1

    def add_node(self, parent, name):
        if name not in parent.get_children_names():
            child = Node(name, parent)
            parent.children.append(child)
            self.nodes.append(child)
            return child

    def delete_node(self, node):
        node.parent.children.remove(node)
        self.nodes.remove(node)

    def get_next_node(self):
        self.node_index += 1
        if self.node_index <= len(self.nodes):
            return self.nodes[self.node_index]

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

    def has_children(self):
        return len(self.children) > 0

    def get_ancestors(self):
        node = self
        ancestry = []
        while node.parent is not None:
            node = node.parent
            ancestry.insert(0, node)
        return ancestry

    # @return: how deep in the tree the particular node is
    def get_generation(self):
        return len(self.get_ancestors())

    def get_sister(self, index):
        children = self.parent.children
        node_order = children.index(self)
        if len(children) > node_order + index >= 0:
            return children[node_order + index]
        else:
            raise IndexError('No such sister')

    def get_left_sister(self):
        return self.get_sister(-1)

    def get_right_sister(self):
        return self.get_sister(1)

    # @param level: the lowest level of nodes to return
    def get_next_node(self, level=100):
        if level == 1:
                next_node = self.get_right_sister()
        elif self.has_children() and self.get_generation() < level:
            return self.children[0]
        else:
            next_node = self.get_next_node_iter(self.parent)
        return next_node

    def get_next_node_iter(self, node):
        if node.parent is None:
            raise IndexError('No more nodes')
        try:
            right = node.get_right_sister()
            return right
        except IndexError:
            right = self.get_next_node_iter(node.parent)
        return right
