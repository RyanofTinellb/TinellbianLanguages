with open("Grammar.txt", 'r') as f:
    with open("New.txt", 'w') as g:
        line = f.readline()
        while line != "":
            if line[0] == "[":
                try:
                    level = int(line[1])
                except ValueError:
                    line = f.readline()
                    continue
                g.write(line)
            line = f.readline()