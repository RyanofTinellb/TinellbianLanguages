import Tkinter as tk
import sys
import os
import tinellb
from HtmlPage import HtmlPage
from HtmlPage import create_search


class EditStory(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.chapter = 1
        self.paragraph = 1
        self.english = tk.Text(self)
        self.transliteration = tk.Text(self)
        self.gloss = tk.Text(self)
        self.windows = [[self.english, 1], [self.transliteration, 3], [self.gloss, 5]]
        self.publish_button = tk.Button(self, text="Push", command=self.publish)
        self.up_button = tk.Button(self, text=unichr(8593), command=self.previous_chapter)
        self.down_button = tk.Button(self, text=unichr(8595), command=self.next_chapter)
        self.left_button = tk.Button(self, text=unichr(8592), command=self.previous_paragraph)
        self.right_button = tk.Button(self, text=unichr(8594), command=self.next_paragraph)
        self.is_bold = False
        self.is_italic = False
        self.is_small_cap = False
        self.english_stars = "<span class=\\\"centre\\\">*&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;&nbsp;&nbsp;*</span>"
        self.tinellbian_stars = "<span class=\\\"centre\\\"><high-lulani>.</high-lulani>&nbsp;&nbsp;&nbsp;&nbsp;" \
                                "<high-lulani>.</high-lulani>&nbsp;&nbsp;&nbsp;&nbsp;<high-lulani>.</high-lulani>" \
                                "</span>"
        self.page = ""
        self.story = []
        self.markdown = tinellb.Markdown()
        self.grid()
        self.create_window()
        self.top = self.winfo_toplevel()
        self.top.state("zoomed")
        self.open_file()

    def create_window(self):
        self.left_button.grid(row=0, column=0)
        self.right_button.grid(row=0, column=1)
        self.up_button.grid(row=0, column=2)
        self.down_button.grid(row=0, column=3)
        self.publish_button.grid(row=0, column=4, sticky=tk.W)
        font = ('Calibri', 16)
        for window, i in self.windows:
            window.configure(height=7, width=108, wrap=tk.WORD, font=font)
            window.bind("<Control-b>", self.bold)
            window.bind("<Control-i>", self.italic)
            window.bind("<Control-k>", self.small_cap)
            window.bind("<Control-s>", self.publish)
            window.bind("<Next>", self.next_paragraph)
            window.bind("<Prior>", self.previous_paragraph)
            window.bind("<Control-Next>", self.next_chapter)
            window.bind("<Control-Prior>", self.previous_chapter)
            window.bind("<KeyPress-minus>", self.insert_hyphen)
            window.grid(row=i, column=4, columnspan=5)

    @staticmethod
    def insert_hyphen(event=None):
        event.widget.insert(tk.INSERT, "\-")
        return "break"

    def bold(self, event=None):
        if self.is_bold:
            event.widget.insert(tk.INSERT, "[/b]")
        else:
            event.widget.insert(tk.INSERT, "[b]")
        self.is_bold = not self.is_bold
        return "break"
    
    def italic(self, event=None):
        if self.is_italic:
            event.widget.insert(tk.INSERT, "[/i]")
        else:
            event.widget.insert(tk.INSERT, "[i]")
        self.is_italic = not self.is_italic
        return "break"
    
    def small_cap(self, event=None):
        if self.is_small_cap:
            event.widget.insert(tk.INSERT, "[/k]")
        else:
            event.widget.insert(tk.INSERT, "[k]")
        self.is_small_cap = not self.is_small_cap
        return "break"

    def open_file(self):
        os.chdir("c:/users/ryan/documents/tinellbianLanguages")
        with open("story_data.txt") as story:
            self.page = story.read()
        self.initialise()

    def initialise(self):
        self.page = self.markdown.to_markdown(self.page)
        self.story = self.page.split('[1]')
        for i, section in enumerate(self.story):
            self.story[i] = section.split('[3]')
            for j, chapter in enumerate(self.story[i]):
                count = self.story[i][j].count("\n") - self.story[1][j].count("\n")
                self.story[i][j] = (chapter + count * "\n").split('\n')
        self.chapter = len(self.story[1]) - 1
        self.paragraph = self.story[3][self.chapter].index("") - 1
        self.refresh()

    def refresh(self):
        try:
            self.story[3][self.chapter][self.paragraph] = \
                self.story[3][self.chapter][self.paragraph].replace(chr(7), "\-")
        except IndexError:
            pass
        if self.story[1][self.chapter][self.paragraph] == self.english_stars:
            for textbox, index in self.windows:
                textbox.delete(1.0, tk.END)
                textbox.insert(1.0, "***")
        else:
            for textbox, index in self.windows:
                textbox.delete(1.0, tk.END)
                try:
                    textbox.insert(1.0, self.story[index][self.chapter][self.paragraph])
                except IndexError:
                    pass
        
    def next_paragraph(self, event=None):
        self.paragraph += 1
        self.refresh()
        return "break"
        
    def previous_paragraph(self, event=None):
        if self.paragraph > 0:
            self.paragraph -= 1
            self.refresh()
        return "break"

    def next_chapter(self, event=None):
        self.chapter += 1
        self.paragraph = 1
        self.refresh()
        return "break"

    def previous_chapter(self, event=None):
        if self.chapter > 0:
            self.chapter -= 1
            self.paragraph = 1
            self.refresh()
        return "break"

    def publish(self, event=None):
        for window, i in self.windows:
            self.story[i][self.chapter][self.paragraph] = window.get(1.0, tk.END + "-1c")
        english, transliteration, gloss = [self.story[i][self.chapter][self.paragraph] for i in [1, 3, 5]]
        if english == "***":
            for i in range(1, 6):
                if i == 2:
                    self.story[i][self.chapter][self.paragraph] = self.tinellbian_stars
                else:
                    self.story[i][self.chapter][self.paragraph] = self.english_stars
        else:
            self.story[4][self.chapter][self.paragraph] = tinellb.interlinear(english, transliteration, gloss)
            self.story[2][self.chapter][self.paragraph] = tinellb.conversion(transliteration.replace("\-", ""))
        for i, section in enumerate(self.story):
            for j, chapter in enumerate(section):
                self.story[i][j] = "\n".join(chapter)
        for i, section in enumerate(self.story):
            self.story[i] = "[3]".join(section)
        self.story[3] = self.story[3].replace("\-", chr(7))
        self.page = "[1]".join(self.story)
        while True:
            self.page = self.page.replace("\n\n", "\n")
            if self.page.count("\n\n") == 0:
                break
        self.write_file()
        self.initialise()
        return "break"

    def write_file(self):
        self.page = self.markdown.to_markup(self.page)
        with open("story_data.txt", "w") as story:
            story.write(self.page)
        HtmlPage("story", 3)
        create_search()

app = EditStory()
app.master.title('Story Edit')
app.mainloop()
