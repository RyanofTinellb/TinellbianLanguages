k = "dictionary_data.txt"
with open(k, "r") as f:
    text = f.read()
for i in "aiu":
    text = text.replace("href=\"../'" + i, "href=\"../" + i + "/'" + i)
with open(k, "w") as f:
    f.write(text)
