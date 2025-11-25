from tkinter import *
from PIL import Image, ImageTk
import os

class Developer:
    def _init_(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Developer")

        # Developer Image
        img_bottom = Image.open("images/developer.png")
        img_bottom = img_bottom.resize((800, 350))
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        lbl = Label(self.root, image=self.photoimg_bottom)
        lbl.place(x=350, y=150, width=800, height=350)

        # Info Text
        info_lbl = Label(self.root,
                         text="Hello! My name is Samruddhi.\nI designed this Face Attendance System.",
                         font=("times new roman", 20, "bold"))
        info_lbl.place(x=350, y=520)