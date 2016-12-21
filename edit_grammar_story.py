import Tkinter as tk
import os
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
        self.is_small_caps = False
        self.is_italics = False
        self.is_bold = False
        self.markup = []
        self.markdown = []
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        for i in range(3):
            heading = tk.Entry(self, width=20)
            heading.grid(sticky=tk.NE, row=i, column=1)
            self.headings.append(heading)
        self.headings[0].bind("<Return>", self.insert_chapter)
        self.headings[1].bind("<Return>", self.insert_heading)
        self.headings[2].bind("<Return>", self.bring_entry)
        self.go_button = tk.Button(self, text="GO!", width=10, command=self.bring_entry)
        self.go_button.grid(row=0, column=2, sticky=tk.NW)
        self.finish_button = tk.Button(self, text="Finished", width=10, command=self.finish)
        self.finish_button.grid(row=1, column=2, sticky=tk.NW)
        self.which_var.set("grammar")
        self.grammar_button = tk.Radiobutton(self, text="Grammar", variable=self.which_var, value="grammar")
        self.grammar_button.grid(row=2, column=2, sticky=tk.W)
        self.story_button = tk.Radiobutton(self, text="Story", variable=self.which_var, value="story")
        self.story_button.grid(row=2, column=3, sticky=tk.W)
        self.edit_text = tk.Text(self, height=23, width=110, font=('Calibri', '15'), wrap=tk.WORD)
        self.edit_text.bind("<Control-BackSpace>", self.delete_word)
        self.edit_text.bind("<Control-s>", self.finish)
        self.edit_text.bind("<Control-k>", self.small_caps)
        self.edit_text.bind("<Control-i>", self.italics)
        self.edit_text.bind("<Control-b>", self.bold)
        self.edit_text.grid(column=2, columnspan=150)
    
    def small_caps(self, event=None):
        if self.is_small_caps:
            self.edit_text.insert(tk.INSERT, "[/k]")
            self.is_small_caps = False
        else:
            self.edit_text.insert(tk.INSERT, "[k]")
            self.is_small_caps = True
        return "break"

    def bold(self, event=None):
        if self.is_bold:
            self.edit_text.insert(tk.INSERT, "[/b]")
            self.is_bold = False
        else:
            self.edit_text.insert(tk.INSERT, "[b]")
            self.is_bold = True
        return "break"

    def italics(self, event=None):
        if self.is_italics:
            self.edit_text.insert(tk.INSERT, "[/i]")
            self.is_italics = False
        else:
            self.edit_text.insert(tk.INSERT, "[i]")
            self.is_italics = True
        return "break"
            
    def insert_chapter(self, event):
        self.headings[1].focus_set()
        return "break"

    def insert_heading(self, event=None):
        self.headings[2].focus_set()
        return "break"

    def delete_word(self, event):
        if self.edit_text.get(tk.INSERT + "-1c") in ".,;:?!":
            self.edit_text.delete(tk.INSERT + "-1c wordstart", tk.INSERT)
        else:
            self.edit_text.delete(tk.INSERT + "-1c wordstart -1c", tk.INSERT)
        return "break"

    def bring_entry(self, event=None):
        entries = []
        for i in range(3):
            entry = self.headings[i].get()
            if entry == "":
                break
            entries.append(entry)
        page = ""
        in_page = False
        level = 0
        last_level = len(entries) - 1
        self.file_name = self.which_var.get()
        with open(self.file_name + "_data.txt", "r") as article:
            os.chdir("c:/users/ryan/documents/tinellbianLanguages")
            for line in article:
                if line == "[" + str(level+1) + "]" + entries[level] + "\n":
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
        self.edit_text.focus_set()
        return "break"

    def finish(self, event=None):
        if self.old_page == "":
            return "break"
        self.new_page = self.edit_text.get(1.0, tk.END+"-1c")
        self.new_page = self.make_replacements(self.new_page)
        with open(self.file_name + "_data.txt", "r") as article:
            page = article.read()
        page = page.replace(self.old_page, self.new_page)
        with open(self.file_name + "_data.txt", "w") as article:
            article.write(page)
        HtmlPage(self.file_name, 3)
        create_search()
        self.old_page = self.new_page
        return "break"

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
