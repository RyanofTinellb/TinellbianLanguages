with open('Dictionary.txt', 'r') as f:
    with open('../index.html', 'w') as g:
        new_text = "<head>\n<title>Lulani Wordlist</title>\n"
        new_text += '<link rel="stylesheet" type="text/css" href="wordlist.css">\n'
        new_text += "<body>\n<ul>"
        g.write(new_text)
        line = f.readline()
        while line != "":
            if line[0:3] == "[1]":
                word = line[3:-1]
                hyperlink_title = word.replace("&#x2019;", "'")
                hyperlink_title = hyperlink_title.replace("&#x294;", "''")
                new_text = '<li><a href="dictionary/' + hyperlink_title + '.html">'
                new_text += word + "</a><br>\n"
                g.write(new_text)
            line = f.readline()
        new_text = "</ul></body>\n"
        g.write(new_text)
