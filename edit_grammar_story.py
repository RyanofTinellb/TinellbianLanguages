import Tkinter as tk
import os
import thread
from HtmlPage import *


class EditPage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.headings = []
        self.grammar_button = None
        self.story_button = None
        self.go_button = None
        self.finish_button = None
        self.finish_text = tk.StringVar()
        self.finish_text.set("Save")
        self.edit_text = tk.Text(self, height=23, width=110, font=('Calibri', '15'), wrap=tk.WORD)
        self.which_var = tk.StringVar()
        self.is_bold = tk.IntVar()
        self.is_italic = tk.IntVar()
        self.is_small_caps = tk.IntVar()
        self.bold_button = tk.Checkbutton(self, text="B", command=self.bold, variable=self.is_bold)
        self.italic_button = tk.Checkbutton(self, text="I", command=self.italic, variable=self.is_italic)
        self.small_cap_button = tk.Checkbutton(self, text="K", command=self.small_caps, variable=self.is_small_caps)
        self.old_page = ""
        self.new_page = ""
        self.file_name = ""
        self.markdown = tinellb.Markdown()
        self.grid()
        self.top = self.winfo_toplevel()
        self.top.state("zoomed")
        self.create_widgets()

    def create_widgets(self):
        for i in range(3):
            heading = tk.Entry(self, width=20)
            heading.grid(sticky=tk.NE, row=i, column=1)
            self.headings.append(heading)
        self.headings[0].bind("<Return>", self.insert_chapter)
        self.headings[1].bind("<Return>", self.insert_heading)
        self.headings[2].bind("<Return>", self.bring_entry)
        self.go_button = tk.Button(self, text="Load", width=10, command=self.bring_entry)
        self.go_button.grid(row=0, column=2, sticky=tk.NW)
        self.finish_button = tk.Button(self, textvariable=self.finish_text, width=10, command=self.finish)
        self.finish_button.grid(row=1, column=2, sticky=tk.NW)
        self.which_var.set("grammar")
        self.bold_button.grid(row=1, column=3, sticky=tk.W)
        self.italic_button.grid(row=1, column=4, sticky=tk.W)
        self.small_cap_button.grid(row=1, column=5, sticky=tk.W)
        self.grammar_button = tk.Radiobutton(self, text="Grammar", variable=self.which_var, value="grammar")
        self.grammar_button.grid(row=2, column=2, sticky=tk.W)
        self.story_button = tk.Radiobutton(self, text="Story", variable=self.which_var, value="story")
        self.story_button.grid(row=2, column=3, columnspan=2, sticky=tk.W)
        self.edit_text.bind("<KeyPress>", self.edit_text_changed)
        self.edit_text.bind("<Control-BackSpace>", self.delete_word)
        self.edit_text.bind("<Control-s>", self.finish)
        self.edit_text.bind("<Control-k>", self.small_caps)
        self.edit_text.bind("<Control-i>", self.italic)
        self.edit_text.bind("<Control-b>", self.bold)
        self.edit_text.bind("<Control-t>", self.table)
        self.edit_text.bind("<KeyPress-|>", self.insert_pipe)
        self.edit_text.grid(column=2, columnspan=150)

    def insert_pipe(self, event=None):
        self.edit_text.insert(tk.INSERT, " | ")
        return "break"

    def table(self, event=None):
        self.edit_text.insert(tk.INSERT, "[t]\n[/t]")
        self.edit_text.mark_set(tk.INSERT, tk.INSERT + "-5c")
        return "break"
    
    def small_caps(self, event=None):
        if event:
            self.is_small_caps.set(-1 * self.is_small_caps.get() + 1)
        if self.is_small_caps.get():
            self.edit_text.insert(tk.INSERT, "[k]")
        else:
            self.edit_text.insert(tk.INSERT, "[/k]")
        return "break"

    def bold(self, event=None):
        if event:
            self.is_bold.set(-1 * self.is_bold.get() + 1)
        if self.is_bold.get():
            self.edit_text.insert(tk.INSERT, "[b]")
        else:
            self.edit_text.insert(tk.INSERT, "[/b]")
        return "break"

    def italic(self, event=None):
        if event:
            self.is_italic.set(-1 * self.is_italic.get() + 1)
        if self.is_italic.get():
            self.edit_text.insert(tk.INSERT, "[i]")
        else:
            self.edit_text.insert(tk.INSERT, "[/i]")
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

    def edit_text_changed(self, event=None):
        self.finish_text.set("*Save")

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
        self.edit_text.insert(tk.INSERT, "Hello")
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
        self.new_page = self.markdown.to_markdown(self.old_page)
        self.edit_text.delete(1.0, tk.END)
        self.edit_text.insert(1.0, self.new_page)
        self.edit_text.focus_set()
        self.finish_text.set("Save")
        return "break"

    def finish(self, event=None):
        self.finish_text.set("Save")
        if self.old_page == "":
            return "break"
        self.new_page = self.edit_text.get(1.0, tk.END+"-1c")
        self.new_page = self.markdown.to_markup(self.new_page)
        with open(self.file_name + "_data.txt", "r") as article:
            page = article.read()
        page = page.replace(self.old_page, self.new_page)
        with open(self.file_name + "_data.txt", "w") as article:
            article.write(page)
        thread.start_new_thread(self.publish, ())
        self.old_page = self.new_page
        return "break"

    def publish(self):
        HtmlPage(self.file_name, 3)
        create_search()

app = EditPage()
app.master.title('Edit Page')
app.mainloop()
