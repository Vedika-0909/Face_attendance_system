from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import psycopg2
import os
from datetime import datetime

# ---------------- DATABASE CONFIG ----------------
DB_URL = "postgresql://neondb_owner:npg_QbefUI5gLEq7@ep-quiet-union-a1c1sfqv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# ---------------- MODEL + CASCADE PATH ----------------
MODEL_PATH = r"models/classifier.xml"
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# ------------------ MAIN CLASS ---------------------
class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition - Attendance System")
        self.root.geometry("1530x790+0+0")
        self.root.config(bg="white")

        # ---------- UI TITLE ----------
        title = Label(self.root, text="FACE RECOGNITION",
                      font=("times new roman", 35, "bold"),
                      bg="white", fg="green")
        title.place(x=0, y=0, width=1530, height=45)

        # ---------- BG IMAGE ----------
        try:
            img_top = Image.open(r"images\facial-recognition.avif")
            img_top = img_top.resize((650, 700))
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            f_lbl = Label(self.root, image=self.photoimg_top)
            f_lbl.place(x=0, y=55, width=650, height=700)
        except Exception:
            pass

        # ---------- BUTTON ----------
        btn = Button(self.root, text="Start Face Recognition",
                     command=self.face_recog,
                     font=("times new roman", 18, "bold"),
                     bg="green", fg="white")
        btn.place(x=800, y=300, width=300, height=60)

        # small info label
        self.info_lbl = Label(self.root, text="Press 'q' to stop recognition", bg="white", fg="black", font=("Segoe UI",10))
        self.info_lbl.place(x=800, y=370)

    # ---------------- DB HELPERS ----------------
    def _connect(self):
        return psycopg2.connect(DB_URL)

    def fetch_student_by_id(self, pred_id):
        """
        Fetch student from DB using predicted id from LBPH recognizer
        Handles int/zero-padding/string mismatches
        """
        try:
            sid_int = int(pred_id)
            candidates = [str(sid_int), str(sid_int).zfill(4)]
            conn = self._connect()
            cur = conn.cursor()
            for cand in candidates:
                cur.execute("""
                    SELECT student_id, name, course, roll_no, department
                    FROM students WHERE student_id = %s
                """, (cand,))
                row = cur.fetchone()
                if row:
                    cur.close()
                    conn.close()
                    return row
            cur.close()
            conn.close()
            return None
        except Exception as e:
            print("DB Fetch Error:", e)
            return None

    def mark_attendance(self, student_id):
        """
        Insert attendance for given student_id (string). Avoid duplicate for same date.
        """
        try:
            conn = self._connect()
            cur = conn.cursor()
            today = datetime.now().date()

            # check duplicate (same day)
            cur.execute("SELECT att_id FROM attendance WHERE student_id = %s AND date = %s", (student_id, today))
            if cur.fetchone():
                cur.close()
                conn.close()
                print(f"✔ Already marked today for {student_id}")
                return True

            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")

            cur.execute("""
                INSERT INTO attendance (student_id, date, time, status)
                VALUES (%s, %s, %s, %s)
            """, (student_id, today, time_str, "Present"))
            conn.commit()
            cur.close()
            conn.close()
            print(f"✔ Attendance saved for ID: {student_id}")
            return True
        except Exception as e:
            print("Attendance Save Error:", e)
            return False

    # ---------------- FACE RECOGNITION ----------------
    def face_recog(self):
        # check model
        if not os.path.exists(MODEL_PATH):
            messagebox.showerror("Model missing", f"Model file not found at: {MODEL_PATH}\nRun training first.")
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read(MODEL_PATH)
        except Exception as e:
            messagebox.showerror("OpenCV error", f"Failed to load recognizer/model.\n{e}")
            return

        if not os.path.exists(CASCADE_PATH):
            messagebox.showerror("Cascade missing", f"Haarcascade not found at: {CASCADE_PATH}")
            return

        faceCascade = cv2.CascadeClassifier(CASCADE_PATH)

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            messagebox.showerror("Camera Error", "Cannot open webcam. Close other camera apps and retry.")
            return

        cam.set(3, 640)
        cam.set(4, 480)

        recognized_once = set()

        while True:
            ret, img = cam.read()
            if not ret:
                print("Camera frame not received. Exiting.")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80,80))

            for (x, y, w, h) in faces:
                try:
                    face_img = gray[y:y+h, x:x+w]
                    if face_img is None or face_img.size == 0:
                        continue

                    pred_id, confidence = recognizer.predict(face_img)
                    print("Detected → ID:", pred_id, "| Confidence:", confidence)

                    student = self.fetch_student_by_id(pred_id)

                    if confidence < 110 and student:
                        sid_db, name, course, roll_no, dept = student
                        label_text = f"ID:{sid_db} | {name} | {course} | {roll_no}"
                        color = (0, 255, 0)
                        if sid_db not in recognized_once:
                            self.mark_attendance(sid_db)
                            recognized_once.add(sid_db)
                    elif confidence < 110:
                        label_text = f"ID:{pred_id} (Not in DB)"
                        color = (0, 165, 255)
                    else:
                        label_text = "Unknown"
                        color = (0, 0, 255)

                except Exception as e:
                    print("Prediction error:", e)
                    label_text = "Error"
                    color = (0, 0, 255)

                # Draw rectangle and label
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                cv2.putText(img, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            cv2.imshow("Face Recognition", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break

        cam.release()
        cv2.destroyAllWindows()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition(root)
    root.mainloop()
