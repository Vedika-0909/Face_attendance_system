from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class Face_recognization_system:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")

        title_lbl = Label(self.root)
        title_lbl.pack(pady=20)


if __name__ == "__main__":
    root = Tk()
    obj = Face_recognization_system(root)
    root.mainloop()
