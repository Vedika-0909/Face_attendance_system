from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import  messagebox


class Help:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition - Attendance System")
        self.root.geometry("1530x790+0+0")
        self.root.config(bg="white")
                
                
        title_lbl=Label(self.root, text="HELP DESK", font=("times new roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0,y=0,width=1530,height=45)

        img_top=Image.open(r"images\Helpdesk.png")
        img_top=img_top.resize((1530,720))
        self.photoimg_top=ImageTk.PhotoImage(img_top)

        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55, width=1530,height=720)

        title_lbl2=Label(self.root, text="For any help Connect with Us", font=("times new roman", 25, "bold"), fg="green")
        title_lbl2.place(x=550,y=150)

        help_label=Label(f_lbl,text="Email:developerteam4@gmail.com",font=("times new roman", 20, "bold"), fg="Black")
        help_label.place(x=540, y=260)

        help_label1=Label(f_lbl,text="Mob No:9876543210",font=("times new roman", 20, "bold"), fg="Black")
        help_label1.place(x=610, y=210)      






if __name__ == "__main__":
    root = Tk()
    obj = Help(root)
    root.mainloop()
