def do_replacements(filename, replacements):
    with open(filename, "r") as f:
        text = f.read()
    with open(replacements, "r") as g:
        old = g.readline()
        new = g.readline()
        while old != "" and new != "":
            old = old[:-1]
            new = new[:-1]
            text = text.replace(old, new)
            old = g.readline()
            new = g.readline()
    with open(filename, "w") as f:
        f.write(text)

do_replacements("Grammar.txt", "Replacements.txt")
