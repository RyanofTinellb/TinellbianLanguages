# TinellbianLanguages
A collection of data on the constructed languages for the fictional universe Tinellb

The site is here: https://ryanoftinellb.github.io/TinellbianLanguages/

Includes:
* Grammar - https://ryanoftinellb.github.io/TinellbianLanguages/grammar/index.html
* Dictionary - https://ryanoftinellb.github.io/TinellbianLanguages/dictionary/index.html
* Story - https://ryanoftinellb.github.io/TinellbianLanguages/story/index.html

---
For each of these (with ~ replacing the above terms):
* ~_data.txt: the text, in markdown
* ~_style.css: the stylesheet for basic pages
* ~_template.txt: an html template for basic pages
* ~_main_template.txt: the html template for the main page
* ~_main_style.css: the stylesheet for main pages
* A folder ~ containing all the .html files.

In addition to these, are a number of Python programs, for the creation of the .html
* CreatePages.py: runs HtmlPage for each of the categories, and then creates the search index.
* HtmlPage.py: translates from markdown text to hypertext markup language.
* Directory.py: data structure for holding the directory structure of a section.
* tinellb.py: useful functions for creating pages in Tinellbian languages.
* edit_story.py: allows for the simultaneous editing of gloss, transliteration and english for paragraphs of the story
* edit_dictionary.py: allows for the edit of particular dictionary entries
* edit_grammar_story.py: allows for the edit of sections of grammar or the story.
