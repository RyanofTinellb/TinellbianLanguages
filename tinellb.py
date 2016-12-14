def conversion(source_file, destination_file):
    page = ""
    with open (source_file, "r") as source:
        for line in source:
            line = convert_line(line)
            page += "<high-lulani>. " + line + " .</high-lulani>\n"
            line = source.readline()
    with open (destination_file, "w") as destination:
        destination.write(page)


def convert_line(line):
    text = ""
    line = line.replace("&rdquo", "")
    line = line.replace("&ldquo;", "")
    line = line.replace("&rsquo;", "'")
    line = line.replace(" &#x294;", "'")
    line = line.replace("&#x2019;", "'")
    line = line.replace("&#x294;", "''")
    line = line.replace("&glottal;", "''")
    line = line.lower()
    if line[:2] == "''":
        line = line[1:]
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
    return text


# @return boolean: true if first < second in tinellbian alphabetical order
def is_in_order(first, second):
    first, first_double_letter = make_replacements(first)
    second, second_double_letter = make_replacements(second)
    if first == second:
        if first_double_letter is second_double_letter:
            return False
        elif first_double_letter:
            return False
        else:
            return True
    for letter in zip(first, second):
        if letter[0] == letter[1]:
            continue
        else:
            letter_index = list(("aiu'pbtdcjkgmnqlrfsxh".find(i) for i in letter))
            if letter_index[0] > letter_index[1]:
                return False
            else:
                return True
    if len(first) == len(second):
        if first_double_letter:
            return False
        elif second_double_letter:
            return True
    elif len(first) > len(second):
        return False
    else:
        return True


def make_replacements(word):
    double_letter = False
    word = word.lower()
    word = word.replace("&#x294;", "''")
    word = word.replace("&#x2019;", "'")
    word = word.replace("&rsquo;", "'")
    for i in "pbtdcjkgmnqlrfsxh":
        new = word.replace(i+i, i)
        if new != word:
            double_letter = True
            word = new
        new = word.replace("''", "'")
        if new != word:
            double_letter = True
            word = new
    for i in "aiu":
        word = word.replace("-" + i, "'" + i)
    word = word.replace("-", "")
    return word, double_letter


def find_entry(source, entry):
    in_entry = False
    page = ""
    with open(source, "r") as dictionary:
        for line in dictionary:
            if line[:3] in ["[1]", "[1]"] and in_entry:
                return page
            elif line[:3] == "[2]" and not is_in_order(line[3:-1], entry):
                in_entry = True
                page += line
            elif in_entry:
                page += line
        return page
