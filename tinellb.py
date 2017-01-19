import random


def convert_sentence(source):
    if source == "***":
        return source
    page = "[hl]." + convert_line(source) + ".[/hl]"
    return page


def convert_word(source):
    text = "[hl]\\(" + convert_line(source) + "\\)[/hl]"
    return text


def convert_line(line):
    text = ""
    for item in ["[i]", "[b]", "[k]", "[/b]", "[/i]", "[/k"]:
        line = line.replace(item, "")
    for item in "\" ":
        line = line.replace(item + "''", item + "'")
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
    return text


def interlinear(english, transliteration, gloss):
    italic = False
    if english == "***":
        return "***\n"
    literal = gloss[gloss.find(" | [r]"):]
    text = "[t]" + english + literal + " | [r]"
    transliteration = morpheme_split(transliteration)
    gloss = morpheme_split(gloss)
    for t_word, g_word in zip(transliteration, gloss):
        if t_word[0][:3] == "[i]":
            t_word[0] = t_word[0][3:]
            italic = True
        if italic:
            text += "[t][i]"
            text += "[/i]\\- | [i]".join(t_word) + "[/i] | [r]"
            text += "\\- | ".join(g_word) + " | [/t] | "
        else:
            text += "[t]"
            text += "\\- | ".join(t_word) + " | [r]"
            text += "\\- | ".join(g_word) + " | [/t] | "
        if t_word[-1][-4:] == "[/i]":
            italic = False
    text += "[/t]\n"
    return text


def morpheme_split(source):
    source = source.split(" ")
    source = [word.split("\\-") for word in source]
    return source


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
        new = word.replace(i + i, i)
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
        pick = from_list[[i <= random.randint(1, sum(scale)) for i in [sum(scale[:i])
                                                                       for i in range(len(scale))]].index(False) - 1]
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
        if random.random() > 0.9 and i > 0:
            new_word += new_word[-1]
            if new_word[-2:] == '**':
                new_word = new_word[:-2] + unichr(660)
        new_word += random_scaled_pick(vowels, vowel_scale)
    return new_word


class Markdown:
    def __init__(self):
        self.markup = []
        self.markdown = []
        with open("c:/users/ryan/documents/tinellbianlanguages/main/replacements.html", "r") as replacements:
            for line in replacements:
                line = line.split(" ")
                down, up = line[0], line[1]
                self.markup.append(up)
                self.markdown.append(down)
        self.source = None
        self.destination = None

    def to_markup(self, text):
        while True:
            try:
                open_brace = text.index("{") + 1
                close_brace = text.index("}")
                if close_brace <= open_brace:
                    raise ValueError
            except ValueError:
                break
            link = text[open_brace:close_brace].lower()
            if link[:2] in ["''", "\\-"]:
                link = link[1:]
            if link[0] in "'-":
                cat = link[1]
            else:
                cat = link[0]
            link = link.replace("'", "\\'")
            link = link.replace("&#x20;", "")
            link = "<a href=\\\"../" + cat + "/" + link + ".html\\\">"
            text = text[:open_brace-1] + link + text[open_brace:close_brace] + "</a>" + text[close_brace+1:]
        self.source, self.destination = self.markdown[::-1], self.markup[::-1]
        return self.convert(text)

    def to_markdown(self, text):
        while True:
            try:
                open_a = text.index("<a")
                close_a = text.index(">", open_a) + 1
            except ValueError:
                break
            text = text.replace("</a>", "}")
            text = text[:open_a] + "{" + text[close_a:]
        self.source, self.destination = self.markup, self.markdown
        return self.convert(text)

    def convert(self, text):
        for first, second in zip(self.source, self.destination):
            text = text.replace(first, second)
        return text
