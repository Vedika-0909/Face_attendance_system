from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2
import cv2
import os
import numpy as np


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management - Face Attendance")
        self.root.geometry("1530x790+0+0")
        self.root.config(bg="white")

        title = Label(self.root,text="FACE RECOGNITION",font=("times new roman",35,"bold"),bg="white",fg="green")
        title.place(x=0, y=0,width=1530,height=45)

        img_top=Image.open(r"images\facial-recognition.avif")
        img_top=img_top.resize((650,700))
        self.photoimg_top=ImageTk.PhotoImage(img_top)

        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55, width=650,height=700)

       














if __name__ == "__main__":
    root = Tk()
    obj=Face_Recognition(root)
    root.mainloop()