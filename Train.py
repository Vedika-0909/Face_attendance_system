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
# Folder containing subfolders named by student ID
DATASET_PATH = r"data"

# Example image shown initially (uploaded file path available in this session)
EXAMPLE_IMAGE = r"/mnt/data/Screenshot 2025-11-22 150913.png"

# Minimum images per student (set to 1 for quick test; increase to 3-5 for real training)
MIN_IMAGES_PER_STUDENT = 1

MODEL_DIR = "models"
MODEL_FILENAME = "classifier.xml"
FACE_SIZE = (200, 200)

# Preview display size (left panel)
PREVIEW_SIZE = (650, 650)
# ----------------------------

class TrainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Attendance - Train Data")

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

        # Left UI (preview)
        left_frame = Frame(main_frame, bg="white")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Load initial example image (if exists) otherwise blank
        if EXAMPLE_IMAGE and os.path.exists(EXAMPLE_IMAGE):
            try:
                pil_img = Image.open(EXAMPLE_IMAGE).convert("RGB").resize(PREVIEW_SIZE)
            except Exception:
                pil_img = Image.new("RGB", PREVIEW_SIZE, (245, 245, 245))
        else:
            pil_img = Image.new("RGB", PREVIEW_SIZE, (245, 245, 245))

        self.left_photo = ImageTk.PhotoImage(pil_img)
        self.left_img_label = Label(left_frame, image=self.left_photo, bg="white")
        self.left_img_label.pack(padx=10, pady=10)

        # Right UI (controls + info)
        right_frame = Frame(main_frame, width=420, bg="white")
        right_frame.pack(side=RIGHT, fill=Y, padx=10)

        Label(right_frame, text="Training Information",
              font=("times new roman", 18, "bold"),
              bg="white", fg="darkblue").pack(pady=8)

        Label(right_frame,
              text=("Dataset format:\n"
                    "data/<student_id>/*.jpg or .png (folder name must be numeric)\n\n"
                    "During training, preview on the left updates with the current image."),
              font=("times new roman", 11),
              justify=LEFT, bg="white").pack(pady=8)

        self.current_student_var = StringVar(value="Current Student: -")
        self.loaded_images_var = StringVar(value="Images Loaded: 0")
        self.total_images_var = StringVar(value="Total Images: 0")

        Label(right_frame, textvariable=self.current_student_var,
              font=("times new roman", 13), bg="white").pack(pady=(12,2))
        Label(right_frame, textvariable=self.loaded_images_var,
              font=("times new roman", 12), bg="white").pack()
        Label(right_frame, textvariable=self.total_images_var,
              font=("times new roman", 12), bg="white").pack()

        self.progress = ttk.Progressbar(right_frame, orient=HORIZONTAL,
                                        length=300, mode='determinate')
        self.progress.pack(pady=12)

        self.train_btn = Button(right_frame, text="START TRAINING",
                                font=("times new roman", 14, "bold"),
                                bg="green", fg="white", width=18,
                                command=self.start_training_thread)
        self.train_btn.pack(pady=8)

        self.log_text = Text(right_frame, width=48, height=15, bg="#f7f7f7")
        self.log_text.pack(pady=8)

        # Start queue processor
        self.root.after(100, self.process_queue)

    # Put UI commands into queue from worker thread
    def ui_push(self, typ, msg=None, **kw):
        self.q.put((typ, msg, kw))

    # Main-thread UI updates
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
                    self.progress['value'] = kw.get("value", 0)

                elif typ == "preview":
                    # kw contains 'path' to image to preview
                    p = kw.get("path")
                    if p and os.path.exists(p):
                        try:
                            img_cv = cv2.imread(p)
                            if img_cv is not None:
                                img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                                pil_img = Image.fromarray(img_rgb).resize(PREVIEW_SIZE)
                            else:
                                pil_img = Image.new("RGB", PREVIEW_SIZE, (245, 245, 245))
                        except Exception:
                            pil_img = Image.new("RGB", PREVIEW_SIZE, (245, 245, 245))

                        self.left_photo = ImageTk.PhotoImage(pil_img)
                        self.left_img_label.config(image=self.left_photo)

                elif typ == "done":
                    messagebox.showinfo("Result", msg or "Done")
                    self.train_btn.config(state=NORMAL)

        except queue.Empty:
            pass

        self.root.after(100, self.process_queue)

    def start_training_thread(self):
        self.train_btn.config(state=DISABLED)
        threading.Thread(target=self.train_classifier, daemon=True).start()

    def train_classifier(self):
        # Validate dataset path
        if not os.path.exists(DATASET_PATH):
            self.ui_push("log", f"❌ Dataset folder not found: {DATASET_PATH}")
            self.ui_push("done", "Dataset folder missing.")
            return

        # Build student map: id -> list of image paths
        student_map = {}
        for entry in sorted(os.listdir(DATASET_PATH)):
            folder_path = os.path.join(DATASET_PATH, entry)
            if not os.path.isdir(folder_path):
                continue
            if not entry.isdigit():
                self.ui_push("log", f"Skipping non-numeric folder: {entry}")
                continue
            sid = int(entry)
            files = [os.path.join(folder_path, f) for f in sorted(os.listdir(folder_path))
                     if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            if files:
                student_map[sid] = files
                print(f"DEBUG: Found {len(files)} images for ID {sid}")

        if not student_map:
            self.ui_push("log", "⚠ No images found in dataset folders.")
            self.ui_push("done", "Training stopped.")
            return

        # Filter by MIN_IMAGES_PER_STUDENT
        filtered_students = []
        total_images = 0
        for sid, flist in sorted(student_map.items()):
            if len(flist) >= MIN_IMAGES_PER_STUDENT:
                filtered_students.append((sid, flist))
                total_images += len(flist)
            else:
                self.ui_push("log", f"Skipping student {sid}: only {len(flist)} image(s) (need >= {MIN_IMAGES_PER_STUDENT})")

        if total_images == 0:
            self.ui_push("log", "No students meet the minimum image requirement.")
            self.ui_push("done", "No valid data to train.")
            return

        self.ui_push("update", None, total=total_images)
        self.ui_push("log", f"Training on {len(filtered_students)} students, {total_images} total images.")

        faces = []
        ids = []
        processed = 0

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # iterate students and images
        for sid, flist in filtered_students:
            self.ui_push("update", None, student=sid)
            self.ui_push("log", f"Processing student {sid} with {len(flist)} images...")

            for img_path in flist:
                # send preview request to main thread
                self.ui_push("preview", None, path=img_path)

                try:
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        self.ui_push("log", f"Cannot read image: {img_path}")
                        continue

                    faces_rects = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4)
                    if len(faces_rects) > 0:
                        x, y, w, h = faces_rects[0]
                        face_img = img[y:y+h, x:x+w]
                    else:
                        face_img = img

                    face_resized = cv2.resize(face_img, FACE_SIZE)
                    faces.append(face_resized)
                    ids.append(sid)

                    processed += 1
                    percent = int((processed / total_images) * 100)
                    self.ui_push("update", None, loaded=processed)
                    self.ui_push("progress", None, value=percent)
                    self.ui_push("log", f"✓ Loaded {os.path.basename(img_path)} ({processed}/{total_images})")

                    # small delay so preview is visible
                    time.sleep(0.2)
                except Exception as e:
                    self.ui_push("log", f"Error processing {img_path}: {e}")

        if len(faces) == 0:
            self.ui_push("log", "No valid faces collected. Training aborted.")
            self.ui_push("done", "Training failed.")
            return

        self.ui_push("log", "Starting LBPH training...")
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, np.array(ids, dtype=np.int32))

            os.makedirs(MODEL_DIR, exist_ok=True)
            model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)
            recognizer.write(model_path)

            self.ui_push("log", f"Model saved to: {model_path}")
            self.ui_push("done", "Training Completed Successfully!")
        except Exception as e:
            self.ui_push("log", f"Training error: {e}")
            self.ui_push("done", "Training failed.")

if __name__ == "__main__":
    # quick dependency hint if needed:
    # pip install opencv-contrib-python pillow
    root = Tk()
    app = TrainApp(root)
    root.mainloop()
