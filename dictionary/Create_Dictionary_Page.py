# Takes a marked-up text file, and transforms it into a set of webpages

# Lines beginning with something of the form [n] has style <hn>
# Lines with [1] begin a new file, and are used for titles
# Lines with [3] are also prefixed with the right-to-left embedding character
# [b], [i], [k] invoke strong, emphasis, small-caps respectively, and last until the next mark-up
#       or the next line


def convert():
    write_text = ""
    new_filename = ""
    with open('Dictionary.txt', 'r') as markup:
        line = markup.readline()
        while line != "":
            if line[0:3] == "[1]":
                if write_text == "":
                    line = line[3:-1]
                    new_filename = line.replace("&#x2019;", "'")
                    new_filename = new_filename.replace("&#x294;", "''")
                    write_text = start_new_file(line)
                else:
                    with open(new_filename + ".html", 'w') as new_file:
                        write_text += '<p class="back">&#x2190; <a href="../index.html">Go Back</a>!'
                        new_file.write(write_text)
                    line = line[3:-1]
                    write_text = start_new_file(line)
                    new_filename = line.replace("&#x2019;", "'")
                    new_filename = new_filename.replace("&#x294;", "''")
            elif line[0] == "[":
                if line[1] in ["2", "4", "5", "6"]:
                    write_text += "<h" + line[1] + ">" + line[3:-1] + "</h" + line[1] + ">\n"
                elif line[1] == "3":
                    write_text += "<h" + line[1] + ">&#x202e;" + line[3:-1] + "</h" + line[1] + ">\n"
                else:
                    write_text += "<p>" + line + "\n"
            else:
                write_text += "<p>" + line + "\n"
            line = markup.readline()
        with open(new_filename + ".html", 'w') as new_file:
            write_text += '<p class="back">&#x2190; hi<a href="../index.html">Go Back</a>!'
            new_file.write(write_text)


def start_new_file(line):
        next_line = '<html>\n<head>\n<title>' + line + '</title>\n'
        next_line += '<link rel="stylesheet" type="text/css" href="dictionary_entry.css">\n'
        next_line += '</head>\n<body>\n<h1>' + line + '</h1>\n'
        return next_line

convert()

