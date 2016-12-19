import random

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
            if line[:3] in ["[1]", "[2]"] and in_entry:
                return page
            elif line[:3] == "[2]" and not is_in_order(line[3:-1], entry):
                in_entry = True
                page += line
            elif in_entry:
                page += line
        return page


def random_scaled_pick(from_list, scale):
    try:
        pick = from_list[[i < random.randint(1, sum(scale)) for i in [sum(scale[:i])
                                                                      for i in range(len(scale))]].index(False)]
    except ValueError:
        pick = from_list[-1]
    return pick


def make_word():
    consonant_scale = [10, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 24, 27, 32, 38, 47, 62, 82]
    consonants = ['b', 'g', 'j', 'f', 'h', 'd', 'p', 'r', 't', 'm', 'c', 'x', 'q', 'n', 'k', 'l', unichr(8217), 's']
    vowel_scale = [4, 2, 1]
    vowels = ['a', 'i', 'u']
    syllable = [1, 2, 3, 4]
    syllable_scale = [7, 18, 15, 2]
    num = random_scaled_pick(syllable, syllable_scale)
    new_word = ""
    for i in range(num):
        new_word += random_scaled_pick(consonants, consonant_scale)
        if random.random() > 0.2 and i > 0:
            new_word += new_word[-1]
            if new_word[-2:] == '**':
                new_word = new_word[:-2] + unichr(660)
        new_word += random_scaled_pick(vowels, vowel_scale)
    return new_word
