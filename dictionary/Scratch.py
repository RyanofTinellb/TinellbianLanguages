with open('Grammar.txt', 'r') as f:
    with open('Replacement.txt', 'raf') as g:
        line = f.readline()
        while line != "":
            if line[0:3] == "[3]":
                line = line.replace("<", "&lt;")
                line = line.replace(">", "&gt;")
            g.write(line)
            line = f.readline()