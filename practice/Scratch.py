with open('Grammar.txt', 'r') as f:
    text = f.read()
    with open('Replacements.txt', 'r') as g:
        old = g.readline()[:-1]
        new = g.readline()[:-1]
        while new != "":
            text = text.replace(old, new)
            old = g.readline()[:-1]
            new = g.readline()[:-1]
with open('Grammar.txt', 'w') as h:
    h.write(text)
