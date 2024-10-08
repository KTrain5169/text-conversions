import pyperclip
import os
import sys
from tkinter import *
from tkinter import ttk
from functools import partial
from PIL import Image, ImageTk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library.TextConverter import TextConverter
converter = TextConverter()

def copy_to_clipboard(text):
    pyperclip.copy(text.get())

def add_text(text_input):
    ttk.Label( text=converter.reverse_text(text_input.get())).grid(row=2,column=2)
    ttk.Label( text=converter.text_flip(text_input.get())).grid(row=4,column=2)
    ttk.Label( text=converter.enchant_text(text_input.get())).grid(row=5,column=2)

def add_copy_buttons():
    ttk.Button(root, text="copy", command=partial(copy_to_clipboard, translate_text),).grid(row=2, column=1)

root = Tk()
root.title("Translator")
ico = Image.open('images/icon.ico')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

ttk.Label( text="Enter text to translate:").grid(column=0, row=0)
translate_text = Entry(root)
translate_text.grid(row=1, column=0)
ttk.Label( text="Reversed text:").grid(row=2,column=0)
ttk.Label( text="Fliped text:").grid(row=4,column=0)
ttk.Label( text="Enchanted text:").grid(row=5,column=0)
ttk.Button(root, text="Submit", command=partial(add_text, translate_text),).grid(row=1, column=1)
add_copy_buttons()

root.mainloop()
