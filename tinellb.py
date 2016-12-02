def conversion(source_file, destination_file):
    with open (source_file, "r") as source:
        line = source.readline()
        page = ""
        while line != "":
            text = ""
            line = line.replace("&rdquo", "")
            line = line.replace("&ldquo;", "")
            line = line.replace("&rsquo;", "'")
            line = line.replace(" &#x294;", "'")
            line = line.replace("&#x2019;", "'")
            line = line.replace("&#x294;", "''")
            line = line.replace("<em>", "")
            line = line.replace("</em>", "")
            line = line.lower()
            for last, this in zip(line, line[1:]):
                if this == last:
                    text += ";"
                elif last == "'":
                    text += this
                elif this == "a":
                    text += last
                elif this == "i":
                    text += last.upper()
                elif this == "u":
                    index = "pbtdcjkgmnqlrfsxh".find(last)
                    text += "oOeEyY><UIAWwvzZV"[index]
                elif last + this == ". ":
                    text += " . "
                elif last + this == ", ":
                    text += " , "
                elif last + this == "! ":
                    text += " . "
                elif last + this == "? ":
                    text += " . "
                elif this == " ":
                    text += " / "
                elif last + this == "; ":
                    text += " , "
                elif last + this == ": ":
                    text += " , "
            text = text.replace("<", "&lt;")
            text = text.replace(">", "&gt;")
            page += "<span class=\"right\"><span class=\"tinellbian\">. " + text + " .</span></span>\n"
            line = source.readline()
    with open (destination_file, "w") as destination:
        destination.write(page)

conversion("Energy.txt", "Matter.txt")
