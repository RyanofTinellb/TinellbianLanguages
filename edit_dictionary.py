import Tkinter as tk
import tinellb
import os
import threading
from HtmlPage import *


class EditDictionary(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.heading = None
        self.go_button = None
        self.publish_button = None
        self.edit_text = None
        self.random_words = None
        self.random_word = tk.StringVar()
        self.old_page = ""
        self.entry = ""
        self.new_page = ""
        self.is_bold = False
        self.is_italic = False
        self.is_small_caps = False
        self.markdown = tinellb.Markdown()
        self.grid()
        self.create_widgets()
        os.chdir("C:/Users/Ryan/Documents/TinellbianLanguages")

    def create_widgets(self):
        self.heading = tk.Text(self, height=1, width=20, wrap=tk.NONE)
        self.heading.grid(sticky=tk.NE)
        self.heading.bind("<Return>", self.bring_entry)
        self.go_button = tk.Button(self, text="GO!", command=self.bring_entry)
        self.go_button.grid(row=1, column=1, sticky=tk.NW)
        self.publish_button = tk.Button(text="Publish", command=self.save)
        self.publish_button.grid(row=1, column=2, sticky=tk.NW)
        self.random_words = tk.Label(self, textvariable=self.random_word)
        self.random_words.grid(row=1, column=0)
        self.edit_text = tk.Text(self, height=27, width=88, font=('Courier New', '15'))
        self.edit_text.bind("<Control-r>", self.remove_hyperlinks)
        self.edit_text.bind("<Control-t>", self.add_high_lulani)
        self.edit_text.bind("<Control-b>", self.bold)
        self.edit_text.bind("<Control-r>", self.refresh_random)
        self.edit_text.bind("<Control-i>", self.italic)
        self.edit_text.bind("<Control-k>", self.small_caps)
        self.edit_text.bind("<Control-h>", self.add_hyperlink)
        self.edit_text.bind("<Control-s>", self.save)
        self.edit_text.bind("<Control-z>", self.bring_entry)
        self.edit_text.bind("<Control-q>", self.get_prefix)
        self.edit_text.bind("<Control-w>", self.get_suffix)
        self.edit_text.bind("<Control-n>", self.new_word)
        self.edit_text.grid(row=1, rowspan=19, column=1)

    def new_word(self, event=None):
        new_template = "[2]" + self.entry + "\n"
        new_template += "[3]High Lulani\n"
        new_template += "[4]" + tinellb.conversion(self.entry).replace(".", "") + "\n"
        new_template += "[5]<ipa>//</ipa>\n"
        new_template += "[6] <div class=\\\"definition\\\"></div>\n"
        self.edit_text.insert(1.0, new_template)
        self.edit_text.mark_set(tk.INSERT, "1.3")
        return "break"

    def refresh_random(self, event=None):
        text = "\n".join([tinellb.make_word() for i in range(10)])
        self.random_word.set(text)

    def get_prefix(self, event):
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

    def get_suffix(self, event):
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
        link = link.replace("&rsquo;", "\\'")
        if link[:9] == "&glottal;":
            link = "\\'" + link[9:]
        link = link.replace("&glottal;", "\\'\\'")
        if link[0] in ["\\", "-"]:
            letter = link[1]
        else:
            letter = link[0]
        link = "<a href=\\\"../" + letter + "/" + link + ".html\\\">" + text + "</a>"
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
        self.entry = self.heading.get(1.0, tk.END+"-1c")
        self.old_page = tinellb.find_entry("dictionary_data.txt", self.entry)
        self.new_page = self.markdown.to_markdown(self.old_page)
        self.edit_text.delete(1.0, tk.END)
        self.edit_text.insert(1.0, self.new_page)
        self.edit_text.focus_set()
        self.edit_text.mark_set(tk.INSERT, "1.0")
        return "break"

    def save(self, event=None):
        location = self.edit_text.index(tk.INSERT)
        self.new_page = self.edit_text.get(1.0, tk.END)
        self.new_page = self.markdown.to_markup(self.new_page)
        with open("dictionary_data.txt", "r") as dictionary:
            page = dictionary.read()
        page = page.replace(self.old_page, self.new_page)
        with open("dictionary_data.txt", "w") as dictionary:
            dictionary.write(page)
        self.bring_entry()
        self.edit_text.mark_set(tk.INSERT, location)
        t = threading.Thread(target=self.publish)
        t.start()
        return "break"

    @staticmethod
    def publish():
        HtmlPage("dictionary", 2)
        create_search()
        print("Done!")

app = EditDictionary()
app.master.title('Dictionary Edit')
app.mainloop()
