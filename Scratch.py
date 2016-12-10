from Directory import *

d = Directory("grammar")
page = ""
i = d.root
while True:
    j = d.root
    while True:
        page += i.name + "--> "
        page += i.hyperlink(j) + "\n"
        try:
            j = j.next_node()
        except IndexError:
            break
    try:
        i = i.next_node()
    except IndexError:
        break
with open("prac.html", "w") as f:
    f.write(page)