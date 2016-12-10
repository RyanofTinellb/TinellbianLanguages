import Tkinter as tk
from tinellb import find_entry
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
        self.markup = []
        self.markdown = []
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.heading = tk.Text(self, height=1, width=20, wrap=tk.NONE)
        self.heading.grid(sticky=tk.NE)
        self.go_button = tk.Button(self, text="GO!", command=self.bring_entry)
        self.go_button.grid(row=1, column=1, sticky=tk.NW)
        self.finish_button = tk.Button(text="Finished", command=self.finish)
        self.finish_button.grid(row=1, column=1, sticky=tk.NW)
        self.publish_button = tk.Button(text="Publish", command=self.publish)
        self.publish_button.grid(row=1, column=3, sticky=tk.NW)
        self.edit_text = tk.Text(self, height=25, width=105, font=('Calibri', '15'))
        self.edit_text.grid(row=1, rowspan=19)

    def bring_entry(self):
        entry = self.heading.get(1.0, tk.END+"-1c")
        self.old_page = find_entry("dictionary_data.txt", entry)
        self.new_page = self.make_replacements(self.old_page, False)
        self.edit_text.delete(1.0, tk.END)
        self.edit_text.insert(1.0, self.new_page)

    def finish(self):
        self.new_page = self.edit_text.get(1.0, tk.END+"-1c")
        self.new_page = self.make_replacements(self.new_page)
        with open("dictionary_data.txt", "r") as dictionary:
            page = dictionary.read()
        page = page.replace(self.old_page, self.new_page)
        with open("dictionary_data.txt", "w") as dictionary:
            dictionary.write(page)
        self.edit_text.delete(1.0, tk.END)

    def publish(self):
        self.new_page = self.edit_text.get(1.0, tk.END+"-1c")
        self.new_page = self.make_replacements(self.new_page)
        with open("dictionary_data.txt", "r") as dictionary:
            page = dictionary.read()
        page = page.replace(self.old_page, self.new_page)
        with open("dictionary_data.txt", "w") as dictionary:
            dictionary.write(page)
        HtmlPage("dictionary", 2)
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


app = EditDictionary()
app.master.title('Dictionary Edit')
app.mainloop()
