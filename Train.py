from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2
import cv2
import os
import numpy as np


class Train:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management - Face Attendance")
        self.root.geometry("1530x790+0+0")
        self.root.config(bg="white")

        # ----------------- TITLE -----------------
        title_lbl = Label(self.root, text="TRAIN DATA SET", 
                          font=("times new roman", 35, "bold"),
                          bg="darkgreen", fg="white")
        title_lbl.place(x=0, y=0, width=1530, height=50)

        # ----------------- LEFT IMAGE -----------------
        img_left = Image.open("images/Trainpy.jpg").resize((700, 550))
        self.photo_left = ImageTk.PhotoImage(img_left)

        lbl_left = Label(self.root, image=self.photo_left, bg="white")
        lbl_left.place(x=50, y=100, width=700, height=550)

        # ----------------- RIGHT FRAME -----------------
        right_frame = Frame(self.root, bd=3, bg="white", relief=RIDGE)
        right_frame.place(x=800, y=100, width=650, height=550)

        head = Label(right_frame, text="Training Information",
                     font=("times new roman", 20, "bold"),
                     bg="white", fg="darkblue")
        head.pack(pady=15)

        info_text = """
This process will train the system by reading all 
captured face images from your dataset folder.

Steps:
1. System scans each student's image folder.
2. Converts face images to grayscale.
3. Extracts face features using LBPH algorithm.
4. Saves trained model for recognition.
        """

        lbl_info = Label(right_frame, text=info_text,
                         font=("times new roman", 14),
                         justify=LEFT, bg="white")
        lbl_info.pack(pady=10)

        # ----------------- TRAIN BUTTON -----------------
        train_btn = Button(right_frame, text="START TRAINING",
                           command=self.train_classifier,
                           font=("times new roman", 18, "bold"),
                           bg="green", fg="white",
                           relief=RAISED, cursor="hand2")
        train_btn.pack(pady=40)

    # --------------------- TRAINING FUNCTION ---------------------
    def train_classifier(self):
        data_dir = "data"   # your dataset folder

        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Dataset folder not found!")
            return

        faces = []
        ids = []

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith("jpg") or file.endswith("png"):
                    img_path = os.path.join(root, file)
                    img = Image.open(img_path).convert('L')  # grayscale

                    image_np = np.array(img, "uint8")
                    id = int(os.path.split(root)[-1])
                    faces.append(image_np)
                    ids.append(id)

        ids = np.array(ids)

        # LBPH Training
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")

        messagebox.showinfo("Result", "Training Completed Successfully!")
if __name__ == "__main__":
    root = Tk()
    # start maximized so frames get full area
    try:
        root.state('zoomed')
    except:
        # fallback: set large geometry
        root.geometry("1600x900+0+0")
    root.resizable(True, True)
    app = Train(root)
    root.mainloop()
