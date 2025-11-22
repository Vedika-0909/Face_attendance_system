
import os
import threading
import queue
import time
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# ---------- CONFIG ----------
# dataset folder where images are stored (your case: data/)
DATASET_PATH = "data"   # <-- change if your folder name is different
# example image to show on left (optional). I used the uploaded sample path.
EXAMPLE_IMAGE = r"/mnt/data/9d7a09c2-d8e1-49e0-88f5-e35345a35bba.png"

# minimum number of images required per student to include them in training
MIN_IMAGES_PER_STUDENT = 5

# output model path
MODEL_DIR = "models"
MODEL_FILENAME = "classifier.xml"
# ----------------------------

class TrainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management - Face Attendance (Train Data)")
        try:
            self.root.state('zoomed')
        except:
            self.root.geometry("1200x800")
        self.root.config(bg="white")

        self.q = queue.Queue()

        title_lbl = Label(self.root, text="TRAIN DATA SET",
                          font=("times new roman", 34, "bold"),
                          bg="darkgreen", fg="white")
        title_lbl.pack(side=TOP, fill=X)

        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Left: image / illustration
        left_frame = Frame(main_frame, bg="white")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # load sample image (safe)
        try:
            img = Image.open(EXAMPLE_IMAGE).resize((650, 650))
        except Exception:
            img = Image.new("RGB", (650, 650), (245, 245, 245))
        self.left_photo = ImageTk.PhotoImage(img)
        lbl_left = Label(left_frame, image=self.left_photo, bg="white")
        lbl_left.pack(padx=10, pady=10)

        # Right: info + controls
        right_frame = Frame(main_frame, width=420, bg="white")
        right_frame.pack(side=RIGHT, fill=Y, padx=10)

        head = Label(right_frame, text="Training Information",
                     font=("times new roman", 18, "bold"),
                     bg="white", fg="darkblue")
        head.pack(pady=8)

        info_text = (
            "This will train LBPH recognizer using images in the dataset folder.\n\n"
            "Filename format expected: user.<ID>.<imgno>.jpg\n"
            "Example: user.435.1.jpg  (ID = 435)\n\n"
            f"Students with fewer than {MIN_IMAGES_PER_STUDENT} images will be skipped."
        )
        lbl_info = Label(right_frame, text=info_text, font=("times new roman", 11),
                         justify=LEFT, bg="white")
        lbl_info.pack(pady=8)

        # Live variables
        self.current_student_var = StringVar(value="Current Student: -")
        self.loaded_images_var = StringVar(value="Images Loaded: 0")
        self.total_images_var = StringVar(value="Total Images: 0")

        lbl_cur = Label(right_frame, textvariable=self.current_student_var,
                        font=("times new roman", 13), bg="white")
        lbl_cur.pack(pady=(12,2))

        lbl_loaded = Label(right_frame, textvariable=self.loaded_images_var,
                           font=("times new roman", 12), bg="white")
        lbl_loaded.pack()

        lbl_total = Label(right_frame, textvariable=self.total_images_var,
                          font=("times new roman", 12), bg="white")
        lbl_total.pack()

        self.progress = ttk.Progressbar(right_frame, orient=HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=12)

        self.train_btn = Button(right_frame, text="START TRAINING", font=("times new roman", 14, "bold"),
                                bg="green", fg="white", width=18, command=self.start_training_thread, cursor="hand2")
        self.train_btn.pack(pady=8)

        # Text log
        self.log_text = Text(right_frame, width=48, height=14, bg="#f7f7f7")
        self.log_text.pack(pady=8)

        # Poll queue
        self.root.after(200, self.process_queue)

    def ui_push(self, typ, msg=None, **kwargs):
        self.q.put((typ, msg, kwargs))

    def process_queue(self):
        try:
            while True:
                typ, msg, kw = self.q.get_nowait()
                if typ == "log":
                    self.log_text.insert(END, msg + "\n")
                    self.log_text.see(END)
                elif typ == "update":
                    if "student" in kw:
                        self.current_student_var.set(f"Current Student: {kw['student']}")
                    if "loaded" in kw:
                        self.loaded_images_var.set(f"Images Loaded: {kw['loaded']}")
                    if "total" in kw:
                        self.total_images_var.set(f"Total Images: {kw['total']}")
                elif typ == "progress":
                    val = kw.get("value", 0)
                    self.progress['value'] = val
                elif typ == "done":
                    messagebox.showinfo("Result", msg or "Training Completed!")
                    self.train_btn.config(state=NORMAL)
        except queue.Empty:
            pass
        self.root.after(200, self.process_queue)

    def start_training_thread(self):
        self.train_btn.config(state=DISABLED)
        t = threading.Thread(target=self.train_classifier, daemon=True)
        t.start()

    def train_classifier(self):
        # Validate dataset path
        dataset_path = DATASET_PATH
        if not os.path.exists(dataset_path):
            self.ui_push("log", f"Dataset folder not found: {dataset_path}")
            self.ui_push("done", "Dataset folder missing.")
            return

        # gather all image files
        image_files = [f for f in os.listdir(dataset_path)
                       if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        if len(image_files) == 0:
            self.ui_push("log", "No images found in dataset folder.")
            self.ui_push("done", "Dataset empty.")
            return

        # group files by student id extracted from filename format user.<id>.<imgno>.jpg
        student_map = {}   # id -> list of filenames
        for fname in image_files:
            parts = fname.split(".")
            # expected: ["user", "<id>", "<imgno>", "jpg"]
            if len(parts) < 3:
                self.ui_push("log", f"Skipping unexpected filename: {fname}")
                continue
            try:
                sid = int(parts[1])
            except Exception:
                self.ui_push("log", f"Skipping file with non-int id: {fname}")
                continue
            student_map.setdefault(sid, []).append(fname)

        # filter students with fewer than MIN_IMAGES_PER_STUDENT
        filtered_students = []
        total_images = 0
        for sid, flist in sorted(student_map.items()):
            if len(flist) >= MIN_IMAGES_PER_STUDENT:
                filtered_students.append((sid, sorted(flist)))
                total_images += len(flist)
            else:
                self.ui_push("log", f"Skipping student {sid}: only {len(flist)} image(s) (need >= {MIN_IMAGES_PER_STUDENT})")

        if total_images == 0:
            self.ui_push("log", "No students meet minimum image requirement.")
            self.ui_push("done", "No valid data to train.")
            return

        self.ui_push("update", None, total=total_images)
        self.ui_push("log", f"Training on {len(filtered_students)} students, {total_images} total images.")

        faces = []
        ids = []
        processed = 0

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # iterate students
        for sid, flist in filtered_students:
            self.ui_push("update", None, student=sid)
            self.ui_push("log", f"Processing student {sid} with {len(flist)} images...")
            for fname in flist:
                img_path = os.path.join(dataset_path, fname)
                try:
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        self.ui_push("log", f"Could not read image: {img_path}")
                        continue

                    # Attempt face detection and crop; if fails use full image
                    faces_rects = face_cascade.detectMultiScale(img, 1.1, 4)
                    if len(faces_rects) > 0:
                        x, y, w, h = faces_rects[0]
                        face_img = img[y:y+h, x:x+w]
                    else:
                        face_img = img

                    # resize to consistent size
                    face_resized = cv2.resize(face_img, (200, 200))
                    faces.append(face_resized)
                    ids.append(sid)

                    processed += 1
                    percent = int((processed / total_images) * 100)
                    self.ui_push("update", None, loaded=processed)
                    self.ui_push("progress", None, value=percent)
                    self.ui_push("log", f"Loaded {fname} ({processed}/{total_images})")
                except Exception as e:
                    self.ui_push("log", f"Error processing {img_path}: {e}")

        # finalize training
        if len(faces) == 0:
            self.ui_push("log", "No valid faces collected. Training aborted.")
            self.ui_push("done", "Training failed.")
            return

        self.ui_push("log", "Starting LBPH training...")
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, np.array(ids))

            if not os.path.exists(MODEL_DIR):
                os.makedirs(MODEL_DIR)
            model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)
            recognizer.write(model_path)

            self.ui_push("log", f"Model saved to: {model_path}")
            self.ui_push("done", "Training Completed Successfully!")
        except Exception as e:
            self.ui_push("log", f"Training error: {e}")
            self.ui_push("done", "Training failed.")

if __name__ == "__main__":
    root = Tk()
    app = TrainApp(root)
    root.mainloop()
