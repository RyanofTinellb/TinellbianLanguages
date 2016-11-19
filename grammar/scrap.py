from Hierarchy import *

hierarchy = Hierarchy("root")
node = hierarchy.add_node(hierarchy.root, "alpha")
node = hierarchy.add_node(node, "beta")
node = hierarchy.add_node(node, "gamma")
print([k.name for k in node.get_ancestry()])
