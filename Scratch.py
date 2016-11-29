old = '<a href="[\\t].html">[\\t]</a>\n[r]genitive\n<a href="pagu.html">pagu</a>\n<a href="ba.html">'
old += 'ba</a>\n<a href="disi.html">disi</a>\n<a href="qa.html">qa</a>'
with open("Dictionary.txt", "r") as f:
    text = f.read()
text = text.replace(old, "")
with open("Dictionary.txt", "w") as g:
    g.write(text)

print(old)