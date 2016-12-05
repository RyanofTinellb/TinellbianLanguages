from Directory import *

d = Directory("story_data.txt", "story")
k = d.get_root()
k = k.children[4]
for i in k.get_cousins():
    print i.name
