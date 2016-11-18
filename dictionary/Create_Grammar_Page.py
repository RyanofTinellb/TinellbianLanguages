# new pages begin with a [1], [2] or [3]
# keep track of heading level
#

line = " "
with open('Grammar.txt', 'r') as grammar:
    while line != "":
        line = grammar.readline()
        if line[0] == "[":
            try:
                level = int(line[1]) - 1
            except ValueError:
                break
            text_list = [line[3:]]
            if text != "":
                with open(text_list[level] + )
            text = "<html><head><title>" + text_list[level-1] + "</title>"
            text += "<link rel=\"stylesheet\" type=\"text/css\" href=\"grammar_page.css\">"
            text += "<div class=\"content\"><h1>" + text_list[0] + "</h1>"

