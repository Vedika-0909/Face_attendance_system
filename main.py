from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class Face_recognization_system:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")

        #first image
        img=Image.open (r"images\right_side.png")
        img=img.resize((500,130))
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)

          #Second image
        img1=Image.open (r"images\middle.webp")
        img1=img1.resize((500,130))
        self.photoimg1=ImageTk.PhotoImage(img1)

        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=500,y=0,width=500,height=130)
        #Third Image
        img2=Image.open (r"images\left_side.jpg")
        img2=img2.resize((500,130))
        self.photoimg2=ImageTk.PhotoImage(img2)

        f_lbl=Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1000,y=0,width=500,height=130)
        
         #Title
        title_lbl=Label(text="FACE RECOGNITION ATTENDANCE SYSTEM",font=("times new roman",35,"bold"),bg="black",fg="white")
        title_lbl.place(x=0,y=150,width=1530,height=45)

        #Student button
        img3=Image.open (r"images\student_detail.avif")
        img3=img3.resize((220,220))
        self.photoimg3=ImageTk.PhotoImage(img3)

        b1=Button(image=self.photoimg3,cursor="hand2")
        b1.place(x=100,y=200,width=210,height=200)

        b1_1=Button(text="Student Details",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="darkblue")
        b1_1.place(x=100,y=400,width=210,height=40)

       
        #Face recognition
        img4=Image.open (r"images\Face_Recognition.avif")
        img4=img4.resize((220,220))
        self.photoimg4=ImageTk.PhotoImage(img4)

        b1=Button(image=self.photoimg4,cursor="hand2")
        b1.place(x=450,y=200,width=210,height=200)

        b1_1=Button(text="Face Recognition",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="darkblue")
        b1_1.place(x=450,y=400,width=210,height=40)

        #Attendance
        img5=Image.open (r"images\Attendance.jpg")
        img5=img5.resize((220,220))
        self.photoimg5=ImageTk.PhotoImage(img5)

        b1=Button(image=self.photoimg5,cursor="hand2")
        b1.place(x=800,y=200,width=210,height=200)

        b1_1=Button(text="Attendance",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="darkblue")
        b1_1.place(x=800,y=400,width=210,height=40)

        #Help
        img6=Image.open (r"images\Help.jpg")
        img6=img6.resize((220,220))
        self.photoimg6=ImageTk.PhotoImage(img6)

        b1=Button(image=self.photoimg6,cursor="hand2")
        b1.place(x=1150,y=200,width=210,height=200)

        b1_1=Button(text="Help",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="darkblue")
        b1_1.place(x=1150,y=400,width=210,height=40)

        #Train data
        img7=Image.open (r"images\Train_Data.jpg")
        img7=img7.resize((220,220))
        self.photoimg7=ImageTk.PhotoImage(img7)

        b1=Button(image=self.photoimg7,cursor="hand2")
        b1.place(x=100,y=500,width=210,height=200)

        b1_1=Button(text="Train Data",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="darkblue")
        b1_1.place(x=100,y=700,width=210,height=40)

        #Photos
        img8=Image.open (r"images\Photos.jpg")
        img8=img8.resize((220,220))
        self.photoimg8=ImageTk.PhotoImage(img8)

        b1=Button(image=self.photoimg8,cursor="hand2")
        b1.place(x=450,y=500,width=210,height=200)

        b1_1=Button(text="Photos",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="darkblue")
        b1_1.place(x=450,y=700,width=210,height=40)

        #Developer
        img9=Image.open (r"images\Developer.avif")
        img9=img9.resize((220,220))
        self.photoimg9=ImageTk.PhotoImage(img9)

        b1=Button(image=self.photoimg9,cursor="hand2")
        b1.place(x=800,y=500,width=210,height=200)

        b1_1=Button(text="Train Data",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="darkblue")
        b1_1.place(x=800,y=700,width=210,height=40)

        #Exit
        img10=Image.open (r"images\Exit.jpg")
        img10=img10.resize((220,220))
        self.photoimg10=ImageTk.PhotoImage(img10)

        b1=Button(image=self.photoimg10,cursor="hand2")
        b1.place(x=1150,y=500,width=210,height=200)

        b1_1=Button(text="Exit",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="darkblue")
        b1_1.place(x=1150,y=700,width=210,height=40)




if __name__ == "__main__":
    root = Tk()
    obj = Face_recognization_system(root)
    root.mainloop()

