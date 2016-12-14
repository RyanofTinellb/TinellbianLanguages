import Tkinter as tk
import tinellb
import os
from HtmlPage import *


class EditDictionary(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.heading = None
        self.go_button = None
        self.finish_button = None
        self.publish_button = None
        self.edit_text = None
        self.old_page = ""
        self.new_page = ""
        self.is_bold = False
        self.is_italic = False
        self.is_small_caps = False
        self.markup = []
        self.markdown = []
        self.grid()
        self.create_widgets()
        os.chdir("C:/Users/Ryan/Documents/TinellbianLanguages")

    def create_widgets(self):
        self.heading = tk.Text(self, height=1, width=20, wrap=tk.NONE)
        self.heading.grid(sticky=tk.NE)
        self.heading.bind("<Return>", self.bring_entry)
        self.go_button = tk.Button(self, text="GO!", command=self.bring_entry)
        self.go_button.grid(row=1, column=1, sticky=tk.NW)
        self.finish_button = tk.Button(text="Finished", command=self.finish)
        self.finish_button.grid(row=1, column=1, sticky=tk.NW)
        self.publish_button = tk.Button(text="Publish", command=self.publish)
        self.publish_button.grid(row=1, column=3, sticky=tk.NW)
        self.edit_text = tk.Text(self, height=25, width=105, font=('Calibri', '15'))
        self.edit_text.bind("<Control-r>", self.remove_hyperlinks)
        self.edit_text.bind("<Control-t>", self.add_high_lulani)
        self.edit_text.bind("<Control-b>", self.bold)
        self.edit_text.bind("<Control-i>", self.italic)
        self.edit_text.bind("<Control-k>", self.small_caps)
        self.edit_text.bind("<Control-h>", self.add_hyperlink)
        self.edit_text.bind("<Control-s>", self.publish)
        self.edit_text.bind("<Control-z>", self.bring_entry)
        self.edit_text.bind("<Control-q>", self.grab_prefix)
        self.edit_text.bind("<Control-w>", self.grab_suffix)
        self.edit_text.grid(row=1, rowspan=19)

    def grab_prefix(self, event):
        try:
            text = self.edit_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.edit_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return "break"
        start = text.find("<")
        end = text.find(">")
        link = text[start:end+1]
        text = link + text.replace(link, "")
        self.edit_text.insert(tk.INSERT, text)
        return "break"

    def grab_suffix(self, event):
        try:
            text = self.edit_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.edit_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return "break"
        text = text.replace("</a>", "") + "</a>"
        self.edit_text.insert(tk.INSERT, text)
        return "break"

    def bold(self, event):
        if not self.is_bold:
            self.edit_text.insert(tk.INSERT, "[b]")
            self.is_bold = True
        else:
            self.edit_text.insert(tk.INSERT, "[/b]")
            self.is_bold = False
        return "break"
    
    def italic(self, event):
        if not self.is_italic:
            self.edit_text.insert(tk.INSERT, "[i]")
            self.is_italic = True
        else:
            self.edit_text.insert(tk.INSERT, "[/i]")
            self.is_italic = False
        return "break"
            
    def small_caps(self, event):
        if not self.is_small_caps:
            self.edit_text.insert(tk.INSERT, "[k]")
            self.is_small_caps = True
        else:
            self.edit_text.insert(tk.INSERT, "[/k]")
            self.is_small_caps = False
        return "break"

    def add_hyperlink(self, event):
        try:
            text = self.edit_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.edit_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return "break"
        link = text.lower()
        link = link.replace("[b]", "")
        link = link.replace("[/b]", "")
        link = link.replace("&rsquo;", "'")
        if link[:9] == "&glottal;":
            link = "'" + link[9:]
        link = link.replace("&glottal;", "''")
        if link[0] in ["'", "-"]:
            letter = link[1]
        else:
            letter = link[0]
        link = "<a href=\"../" + letter + "/" + link + ".html\">" + text + "</a>"
        self.edit_text.insert(tk.INSERT, link)
        return "break"

    def add_high_lulani(self, event):
        enter = False
        try:
            text = self.edit_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return "break"
        if self.edit_text.compare(tk.SEL_LAST, "==", tk.SEL_LAST + " lineend"):
            enter = True
        if text[:4] == "href":
            start = text.find("href")
            end = text.find(">")
            text = text[end+1:]
        while "<" in text:
            start = text.find("<")
            end = text.find(">")
            if end == -1:
                break
            text = text[:start] + text[end + 1:]
        if "." in text:
            period = True
        else:
            period = False
        text = text.replace("[b]", "")
        text = text.replace("[/b]", "")
        text = text.replace("</a>", "")
        text = tinellb.convert_line(text)
        if period:
            text = "." + text + "."
        text = "[hl]" + text + "[/hl]"
        text += "\n" if enter else " "
        self.edit_text.insert(tk.SEL_LAST+"+1c", text)
        self.edit_text.mark_set(tk.INSERT, tk.INSERT + "+" + str(len(text) + 1) + "c")
        return "break"

    def remove_hyperlinks(self, event):
        text = self.edit_text.get(tk.INSERT + " linestart", tk.INSERT + " lineend")
        self.edit_text.delete(tk.INSERT + " linestart", tk.INSERT + " lineend")
        text = text.replace("</a>", "")
        while True:
            start = text.find("<a ")
            if start == -1:
                break
            end = text.find(">", start)
            text = text[:start] + text[end+1:]
        self.edit_text.insert(tk.INSERT, text)

    def bring_entry(self, event=None):
        entry = self.heading.get(1.0, tk.END+"-1c")
        self.old_page = tinellb.find_entry("dictionary_data.txt", entry)
        self.new_page = self.make_replacements(self.old_page, False)
        self.edit_text.delete(1.0, tk.END)
        self.edit_text.insert(1.0, self.new_page)
        self.edit_text.focus_set()
        self.edit_text.mark_set(tk.INSERT, "1.0")
        return "break"

    def finish(self):
        self.new_page = self.edit_text.get(1.0, tk.END+"-1c")
        self.new_page = self.make_replacements(self.new_page)
        with open("dictionary_data.txt", "r") as dictionary:
            page = dictionary.read()
        page = page.replace(self.old_page, self.new_page)
        with open("dictionary_data.txt", "w") as dictionary:
            dictionary.write(page)
        self.edit_text.delete(1.0, tk.END)

    def publish(self, event=None):
        self.new_page = self.edit_text.get(1.0, tk.END+"-1c")
        self.new_page = self.make_replacements(self.new_page)
        with open("dictionary_data.txt", "r") as dictionary:
            page = dictionary.read()
        page = page.replace(self.old_page, self.new_page)
        with open("dictionary_data.txt", "w") as dictionary:
            dictionary.write(page)
        HtmlPage("dictionary", 2)
        self.edit_text.delete(1.0, tk.END)
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


app = EditDictionary()
app.master.title('Dictionary Edit')
app.mainloop()
