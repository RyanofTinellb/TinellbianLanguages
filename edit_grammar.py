import Tkinter as tk
from HtmlPage import *


class EditPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.headings = []
        self.grammar_button = None
        self.story_button = None
        self.go_button = None
        self.finish_button = None
        self.edit_text = None
        self.which_var = tk.StringVar()
        self.old_page = ""
        self.new_page = ""
        self.file_name = ""
        self.markup = []
        self.markdown = []
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        for i in range(3):
            heading = tk.Text(height=1, width=20)
            heading.grid(sticky=tk.NE, row=i, column=1)
            self.headings.append(heading)
        self.go_button = tk.Button(text="GO!", width=10, command=self.bring_entry)
        self.go_button.grid(row=0, column=2, sticky=tk.NW)
        self.finish_button = tk.Button(text="Finished", width=10, command=self.finish)
        self.finish_button.grid(row=1, column=2, sticky=tk.NW)
        self.which_var.set("grammar")
        self.grammar_button = tk.Radiobutton(text="Grammar", width=7, variable=self.which_var, value="grammar")
        self.grammar_button.grid(row=2, column=2, sticky=tk.NW)
        self.story_button = tk.Radiobutton(text="Story", width=7, variable=self.which_var, value="story")
        self.story_button.grid(row=2, column=3, sticky=tk.NW)
        self.edit_text = tk.Text(height=22, width=105, font=('Calibri', '15'), wrap=tk.WORD)
        self.edit_text.grid(column=2, columnspan=5)

    def bring_entry(self):
        entries = []
        for i in range(3):
            entry = self.headings[i].get(1.0, tk.END)
            if entry == "\n":
                break
            entries.append(entry)
        page = ""
        in_page = False
        level = 0
        last_level = len(entries) - 1
        self.file_name = self.which_var.get()
        with open(self.file_name + "_data.txt", "r") as article:
            for line in article:
                if line == "[" + str(level+1) + "]" + entries[level]:
                    if level == last_level:
                        in_page = True
                        page += line
                    else:
                        level += 1
                elif in_page:
                    try:
                        if line[0] == "[" and int(line[1]) <= (last_level + 1):
                            break
                    except ValueError:
                        pass
                    page += line
        self.old_page = page
        self.new_page = self.make_replacements(self.old_page, False)
        self.edit_text.delete(1.0, tk.END)
        self.edit_text.insert(1.0, self.new_page)

    def finish(self):
        self.new_page = self.edit_text.get(1.0, tk.END+"-1c")
        self.new_page = self.make_replacements(self.new_page)
        with open(self.file_name + "_data.txt", "r") as article:
            page = article.read()
        page = page.replace(self.old_page, self.new_page)
        with open(self.file_name + "_data.txt", "w") as article:
            article.write(page)
        HtmlPage(self.file_name, 3)
        self.edit_text.delete(1.0, tk.END)

    def make_replacements(self, text, to_markup=True):
        if not len(self.markup):
            with open("replacements.txt", "r") as replacements:
                for line in replacements:
                    up, down = line.split(",")
                    self.markup.append(up)
                    self.markdown.append(down[:-1])
        if to_markup:
            source, destination = self.markdown, self.markup
        else:
            source, destination = self.markup, self.markdown
        for first, second in zip(source, destination):
            text = text.replace(first, second)
        return text

app = EditPage()
app.master.title('Edit Page')
app.mainloop()
