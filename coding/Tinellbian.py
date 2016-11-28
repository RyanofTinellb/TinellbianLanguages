# Changes a string of transliteration into Tinellbian script.


def english_to_lulani(text):
    output = unichr(8238) + ". "
    this_char = ""
    for letter in text:
        last_char = this_char
        this_char = letter.tolower()
        if this_char == "a":
            if last_char in ['pbtdcjkgmnqlrfsxh']:
                output += this_char
        elif this_char == "i":
            if last_char in ['pbtdcjkgmnqlrfsxh']:
                output += this_char.toupper()
        elif this_char == "u":
            if last_char == "p":
                output += "o"
            elif last_char == "b":
                output += "O"
            elif last_char == "t":
                output += "e"
            elif last_char == "d":
                output += "E"
            elif last_char == "c":
                output += "y"
            elif last_char == "j":
                output += "Y"
            elif last_char == "k":
                output += "<"
            elif last_char == "g":
                output += ">"
            elif last_char == "m":
                output += "A"
            elif last_char == "n":
                output += "I"
            elif last_char == "q":
                output += "O"
            elif last_char == "r":
                output += "w"
            elif last_char == "l":
                output += "W"
            elif last_char == "f":
                output += "v"
            elif last_char == "s":
                output += "z"
            elif last_char == "x":
                output += "Z"
            elif last_char == "h":
                output += "V"
