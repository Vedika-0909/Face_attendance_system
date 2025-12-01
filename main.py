from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from student import StudentApp
import subprocess
import os


class Face_recognization_system:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")

        # -------------------- STUDENT DETAILS FUNCTION --------------------
        def student_details():
            self.new_window = Toplevel(self.root)
            self.app = StudentApp(self.new_window)

        self.student_details = student_details

        # -------------------- OPEN PHOTOS --------------------------
        def open_photos():
            os.startfile("data")

        self.open_photos = open_photos

        # -------------------- OPEN TRAIN DATA ----------------------
        def open_train():
            try:
                subprocess.run(["python", "train.py"], check=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open Train.py\n{e}")

        self.open_train = open_train

        # -------------------- FACE RECOGNITION FUNCTION ----------------------
        def open_face_recognition():
            face_file = "Face_recognition.py"
            if os.path.exists(face_file):
                subprocess.Popen(["python", face_file])
            else:
                messagebox.showerror("Error", "Face_recognition.py file not found!")

        self.open_face_recognition = open_face_recognition

        # -------------------- OPEN ATTENDANCE ----------------------
        def open_attendance():
            try:
                subprocess.Popen(["python", "Attendance.py"])
            except Exception as e:
                messagebox.showerror("Error", f"Attendance.py could not be opened\n{e}")

        self.open_attendance = open_attendance

        # -------------------- EXIT FUNCTION ------------------------
        def exit_dashboard():
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                self.root.destroy()

        self.exit_dashboard = exit_dashboard

        # -------------------- DEVELOPER WINDOW --------------------
        def open_developer_window():
            try:
                from developer import DeveloperUI
                new_win = Toplevel(self.root)
                DeveloperUI(new_win)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open Developer window\n{e}")

        self.open_developer_window = open_developer_window


        # -------------------- HELP WINDOW --------------------
        def open_help_window():
            try:
                from Help import HelpUI
                new_win = Toplevel(self.root)
                HelpUI(new_win)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open Help window\n{e}")

        self.open_help_window = open_help_window



        # -------------------- UI START ------------------------------
        # First image
        img = Image.open(r"images\right_side.png")
        img = img.resize((500, 130))
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=500, height=130)

        # Second image
        img1 = Image.open(r"images\middle.webp")
        img1 = img1.resize((500, 130))
        self.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=500, y=0, width=500, height=130)

        # Third image
        img2 = Image.open(r"images\left_side.jpg")
        img2 = img2.resize((500, 130))
        self.photoimg2 = ImageTk.PhotoImage(img2)
        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=1000, y=0, width=500, height=130)

        # Title
        title_lbl = Label(text="FACE RECOGNITION ATTENDANCE SYSTEM",
                          font=("times new roman", 35, "bold"),
                          bg="black", fg="white")
        title_lbl.place(x=0, y=150, width=1530, height=45)

        # ------------------- STUDENT BUTTON -------------------
        img3 = Image.open(r"images\student_detail.avif")
        img3 = img3.resize((220, 220))
        self.photoimg3 = ImageTk.PhotoImage(img3)
        b1 = Button(self.root, image=self.photoimg3, cursor="hand2", command=self.student_details)
        b1.place(x=100, y=200, width=210, height=200)
        b1_1 = Button(self.root, text="Student Details", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="white", fg="darkblue",
                      command=self.student_details)
        b1_1.place(x=100, y=400, width=210, height=40)

        # ------------------- FACE RECOGNITION BUTTON -------------------
        img4 = Image.open(r"images\Face_Recognition.avif")
        img4 = img4.resize((220, 220))
        self.photoimg4 = ImageTk.PhotoImage(img4)
        b2 = Button(self.root, image=self.photoimg4, cursor="hand2",
                    command=self.open_face_recognition)
        b2.place(x=450, y=200, width=210, height=200)
        b2_1 = Button(self.root, text="Face Recognition", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="white", fg="darkblue",
                      command=self.open_face_recognition)
        b2_1.place(x=450, y=400, width=210, height=40)

        # ------------------- ATTENDANCE BUTTON -------------------
        img5 = Image.open(r"images\Attendance.jpg")
        img5 = img5.resize((220, 220))
        self.photoimg5 = ImageTk.PhotoImage(img5)
        b3 = Button(self.root, image=self.photoimg5, cursor="hand2", command=self.open_attendance)
        b3.place(x=800, y=200, width=210, height=200)
        b3_1 = Button(self.root, text="Attendance", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="white", fg="darkblue",
                      command=self.open_attendance)
        b3_1.place(x=800, y=400, width=210, height=40)

        # ------------------- HELP BUTTON -------------------
        img6 = Image.open(r"images\Help.jpg")
        img6 = img6.resize((220, 220))
        self.photoimg6 = ImageTk.PhotoImage(img6)
        b4 = Button(self.root, image=self.photoimg6, cursor="hand2",command=open_help_window)
        b4.place(x=1150, y=200, width=210, height=200)
        b4_1 = Button(self.root, text="Help", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="white", fg="darkblue",command=open_help_window)
        b4_1.place(x=1150, y=400, width=210, height=40)

        # ------------------- TRAIN DATA BUTTON -------------------
        img7 = Image.open(r"images\Train_Data.jpg")
        img7 = img7.resize((220, 220))
        self.photoimg7 = ImageTk.PhotoImage(img7)
        b5 = Button(self.root, image=self.photoimg7, cursor="hand2", command=self.open_train)
        b5.place(x=100, y=500, width=210, height=200)
        b5_1 = Button(self.root, text="Train Data", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="white", fg="darkblue",
                      command=self.open_train)
        b5_1.place(x=100, y=700, width=210, height=40)

        # ------------------- PHOTOS BUTTON -------------------
        img8 = Image.open(r"images\photo.jpg")
        img8 = img8.resize((220, 220))
        self.photoimg8 = ImageTk.PhotoImage(img8)
        b6 = Button(self.root, image=self.photoimg8, cursor="hand2", command=self.open_photos)
        b6.place(x=450, y=500, width=210, height=200)
        b6_1 = Button(self.root, text="Photos", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="white", fg="darkblue",
                      command=self.open_photos)
        b6_1.place(x=450, y=700, width=210, height=40)

        # ------------------- DEVELOPER BUTTON -------------------
        img9 = Image.open(r"images\Developer.png")
        img9 = img9.resize((220, 220))
        self.photoimg9 = ImageTk.PhotoImage(img9)
        b7 = Button(self.root, image=self.photoimg9, cursor="hand2",command=open_developer_window)
        b7.place(x=800, y=500, width=210, height=200)
        b7_1 = Button(self.root, text="Developer", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="white", fg="darkblue",command=open_developer_window)
        b7_1.place(x=800, y=700, width=210, height=40)

        # ------------------- EXIT BUTTON -------------------
        img10 = Image.open(r"images\Exit.jpg")
        img10 = img10.resize((220, 220))
        self.photoimg10 = ImageTk.PhotoImage(img10)
        b8 = Button(self.root, image=self.photoimg10, cursor="hand2", command=self.exit_dashboard)
        b8.place(x=1150, y=500, width=210, height=200)
        b8_1 = Button(self.root, text="Exit", cursor="hand2",
                      font=("times new roman", 15, "bold"),
                      bg="white", fg="darkblue",
                      command=self.exit_dashboard)
        b8_1.place(x=1150, y=700, width=210, height=40)


if __name__ == "__main__":
    root = Tk()
    obj = Face_recognization_system(root)
    root.mainloop()
