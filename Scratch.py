from Directory import *

directory = Directory("dictionary_data.txt", "dictionary")
k = directory.get_root()
k = k.children[0]
while True:
    try:
        k = k.get_next_node(1)
        print(k.get_name())
    except IndexError:
        break

