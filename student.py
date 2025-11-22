from tkinter import *
from tkinter import ttk, messagebox
import psycopg2
import cv2
import os

# ----------------- DB CONFIG -----------------
DB_URL = "postgresql://neondb_owner:npg_QbefUI5gLEq7@ep-quiet-union-a1c1sfqv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# ----------------- COLORS & FONTS -----------------
BG_COLOR = "#0f1724"
PANEL_BG = "#0b2545"
ACCENT = "#1e90ff"
CARD = "#0f3b66"
TEXT_LIGHT = "#ffffff"
TEXT_MUTED = "#cbd5e1"

FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_SUB = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10)          # Form fields bada
FONT_ENTRY = ("Segoe UI", 11)          # Entry box bada
FONT_BTN = ("Segoe UI", 10, "bold")    # Buttons

import tkinter.font as tkfont

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management - Face Attendance")
        self.root.configure(bg=BG_COLOR)
        self.root.state('zoomed')

        # DB Connection
        try:
            self.conn = psycopg2.connect(DB_URL)
            self.cursor = self.conn.cursor()
            print("✅ Cloud DB Connected Successfully")
        except Exception as e:
            messagebox.showerror("DB Connection Error", str(e))
            return

        self.create_table_db()
        self.create_header()
        self.create_main_content()
        self.load_students()

    # ----------------- HEADER -----------------
    def create_header(self):
        header = Frame(self.root, bg=CARD, height=90)
        header.pack(side=TOP, fill=X)
        Label(header, text="STUDENT DETAILS", bg=CARD, fg=TEXT_LIGHT, font=FONT_TITLE).place(x=20, y=10)
        Label(header, text="Face Recognition Attendance", bg=CARD, fg=TEXT_MUTED, font=FONT_SUB).place(x=22, y=52)

    # ----------------- MAIN CONTENT -----------------
    def create_main_content(self):
        content = Frame(self.root, bg=BG_COLOR)
        content.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        # Left Panel (Form) Scrollable
        self.left_canvas = Canvas(content, bg=PANEL_BG, width=600)
        self.left_canvas.pack(side=LEFT, fill=Y)

        vsb_left = Scrollbar(content, orient=VERTICAL, command=self.left_canvas.yview)
        vsb_left.pack(side=LEFT, fill=Y)
        self.left_canvas.configure(yscrollcommand=vsb_left.set)

        self.left_frame = Frame(self.left_canvas, bg=PANEL_BG)
        self.left_canvas.create_window((0, 0), window=self.left_frame, anchor="nw")
        self.left_frame.bind("<Configure>", lambda e: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))

        # Right Panel (Table)
        self.right_frame = Frame(content, bg=BG_COLOR)
        self.right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(10,0))
        
        self.create_form(self.left_frame)
        self.create_table(self.right_frame)

    # ----------------- FORM -----------------
    def create_form(self, parent):
        Label(parent, text="Student Information", bg=PANEL_BG, fg=TEXT_LIGHT, font=("Segoe UI", 16, "bold")).pack(pady=10)

        frm = Frame(parent, bg=PANEL_BG)
        frm.pack(padx=10, pady=5)

        # Department, Course, Year, Semester
        Label(frm, text="Department", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=0, column=0, sticky=W)
        self.cmb_dept = ttk.Combobox(frm, values=["Select", "Computer", "IT", "Mechanical"], state="readonly", font=FONT_ENTRY)
        self.cmb_dept.current(0); self.cmb_dept.grid(row=1, column=0, padx=5, pady=5)

        Label(frm, text="Course", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=0, column=1, sticky=W)
        self.cmb_course = ttk.Combobox(frm, values=["Select", "BE", "BSc", "Diploma"], state="readonly", font=FONT_ENTRY)
        self.cmb_course.current(0); self.cmb_course.grid(row=1, column=1, padx=5, pady=5)

        Label(frm, text="Year", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=0, column=2, sticky=W)
        self.cmb_year = ttk.Combobox(frm, values=["Select", "2023-24", "2024-25", "2025-26"], state="readonly", font=FONT_ENTRY)
        self.cmb_year.current(0); self.cmb_year.grid(row=1, column=2, padx=5, pady=5)

        Label(frm, text="Semester", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=2, column=0, sticky=W, pady=(10,0))
        self.cmb_sem = ttk.Combobox(frm, values=["Select", "Semester-1", "Semester-2"], state="readonly", font=FONT_ENTRY)
        self.cmb_sem.current(0); self.cmb_sem.grid(row=3, column=0, padx=5, pady=5)

        # Student ID, Name, Division, Roll
        Label(frm, text="Student ID", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=4, column=0, sticky=W, pady=(10,0))
        self.ent_id = Entry(frm, font=FONT_ENTRY); self.ent_id.grid(row=5, column=0, padx=5, pady=5)
        Label(frm, text="Student Name", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=4, column=1, sticky=W, pady=(10,0))
        self.ent_name = Entry(frm, font=FONT_ENTRY); self.ent_name.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky=EW)

        Label(frm, text="Class Div", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=6, column=0, sticky=W, pady=(10,0))
        self.cmb_div = ttk.Combobox(frm, values=["Select", "A", "B", "C"], state="readonly", font=FONT_ENTRY)
        self.cmb_div.current(0); self.cmb_div.grid(row=7, column=0, padx=5, pady=5)
        Label(frm, text="Roll No", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=6, column=1, sticky=W, pady=(10,0))
        self.ent_roll = Entry(frm, font=FONT_ENTRY); self.ent_roll.grid(row=7, column=1, padx=5, pady=5)

        # Gender, DOB, Phone
        Label(frm, text="Gender", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=8, column=0, sticky=W, pady=(10,0))
        self.cmb_gender = ttk.Combobox(frm, values=["Male", "Female", "Other"], state="readonly", font=FONT_ENTRY)
        self.cmb_gender.set("Male"); self.cmb_gender.grid(row=9, column=0, padx=5, pady=5)
        Label(frm, text="DOB (DD-MM-YYYY)", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=8, column=1, sticky=W, pady=(10,0))
        self.ent_dob = Entry(frm, font=FONT_ENTRY); self.ent_dob.grid(row=9, column=1, padx=5, pady=5)
        Label(frm, text="Phone No", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=8, column=2, sticky=W, pady=(10,0))
        self.ent_phone = Entry(frm, font=FONT_ENTRY); self.ent_phone.grid(row=9, column=2, padx=5, pady=5)

        # Email, Address, Teacher
        Label(frm, text="Email", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=10, column=0, sticky=W, pady=(10,0))
        self.ent_email = Entry(frm, font=FONT_ENTRY); self.ent_email.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky=EW)
        Label(frm, text="Address", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=12, column=0, sticky=W, pady=(10,0))
        self.txt_addr = Text(frm, height=3, width=35, font=FONT_ENTRY); self.txt_addr.grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky=EW)
        Label(frm, text="Teacher Name", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=10, column=2, sticky=W, pady=(10,0))
        self.ent_teacher = Entry(frm, font=FONT_ENTRY); self.ent_teacher.grid(row=11, column=2, padx=5, pady=5)

        # Photo Radio Buttons
        self.photo_var = StringVar(); self.photo_var.set("take")
        Radiobutton(frm, text="Take Photo Sample", variable=self.photo_var, value="take",
                    bg=PANEL_BG, fg=TEXT_LIGHT, selectcolor=PANEL_BG, font=FONT_LABEL).grid(row=14, column=0, pady=10, sticky=W)
        Radiobutton(frm, text="No Photo Sample", variable=self.photo_var, value="no",
                    bg=PANEL_BG, fg=TEXT_LIGHT, selectcolor=PANEL_BG, font=FONT_LABEL).grid(row=14, column=1, pady=10, sticky=W)

        # Buttons
        Button(frm, text="SAVE", bg=ACCENT, fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#187bcd", command=self.save_student).grid(row=15, column=0, pady=5, sticky=EW)
        Button(frm, text="UPDATE", bg="#16a085", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#11906f", command=self.update_student).grid(row=15, column=1, pady=5, sticky=EW)
        Button(frm, text="DELETE", bg="#e74c3c", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#c0392b", command=self.delete_student).grid(row=15, column=2, pady=5, sticky=EW)
        Button(frm, text="RESET", bg="#7f8c8d", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#6b7a7a", command=self.reset_form).grid(row=16, column=0, pady=5, sticky=EW)
        Button(frm, text="ADD PHOTO SAMPLE", bg="#1e5bd8", fg="white", font=FONT_BTN, bd=0,
               command=self.add_photo_sample).grid(row=16, column=1, pady=5, sticky=EW)
        Button(frm, text="UPDATE PHOTO SAMPLE", bg="#9327c9", fg="white", font=FONT_BTN, bd=0,
               command=self.update_photo_sample).grid(row=16, column=2, pady=5, sticky=EW)

    # ----------------- TABLE -----------------
    def create_table(self, parent):
        search_frame = Frame(parent, bg=BG_COLOR, height=50, width=900)
        search_frame.pack(fill=X, padx=5, pady=5)

        Label(search_frame, text="Search By", bg=BG_COLOR, fg=TEXT_LIGHT, font=FONT_LABEL).pack(side=LEFT, padx=5)
        self.cmb_search = ttk.Combobox(search_frame, values=["Select", "StudentID", "StudentName", "RollNo"], state="readonly", font=FONT_ENTRY)
        self.cmb_search.current(0); self.cmb_search.pack(side=LEFT, padx=5)
        self.ent_search = Entry(search_frame, font=FONT_ENTRY); self.ent_search.pack(side=LEFT, padx=5)
        Button(search_frame, text="SEARCH", bg=ACCENT, fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               command=self.search_student).pack(side=LEFT, padx=5)

        table_frame = Frame(parent)
        table_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        style = ttk.Style()
        style.theme_use("clam")

        bold_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")  # headings
        row_font = tkfont.Font(family="Segoe UI", size=4)                    # rows

        style.configure("Treeview.Heading", font=bold_font)
        style.configure("Treeview", font=row_font, rowheight=20, background="#f0f4f8", foreground="#111827", fieldbackground="#f0f4f8")

        cols = ("Department", "Course", "Year", "Semester",
                "StudentID", "StudentName", "Class Div", "Roll No",
                "Gender", "DOB", "Phone", "Email", "Address", "Teacher")

        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            if c in ("Address", "Email"):
                self.tree.column(c, width=200, anchor=CENTER)
            elif c=="Teacher":
                self.tree.column(c, width=180, anchor=CENTER)
            else:
                self.tree.column(c, width=150, anchor=CENTER)

        vsb = Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        hsb = Scrollbar(table_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

    # ----------------- DB -----------------
    def create_table_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students(
                student_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(50),
                course VARCHAR(50),
                year VARCHAR(20),
                semester VARCHAR(20),
                class_div VARCHAR(10),
                roll_no VARCHAR(10),
                gender VARCHAR(10),
                dob VARCHAR(20),
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT,
                teacher VARCHAR(100)
            )
        """)
        self.conn.commit()

    # ----------------- CRUD & Photo -----------------
    def save_student(self):
        sid = self.ent_id.get().strip(); name = self.ent_name.get().strip()
        if not sid or not name:
            messagebox.showwarning("Warning", "Student ID and Name required!"); return
        try:
            self.cursor.execute("""
                INSERT INTO students(student_id,name,department,course,year,semester,class_div,roll_no,
                gender,dob,phone,email,address,teacher)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (sid, name, self.cmb_dept.get(), self.cmb_course.get(), self.cmb_year.get(), self.cmb_sem.get(),
                  self.cmb_div.get(), self.ent_roll.get(), self.cmb_gender.get(), self.ent_dob.get(),
                  self.ent_phone.get(), self.ent_email.get(), self.txt_addr.get("1.0",END).strip(), self.ent_teacher.get()))
            self.conn.commit()
            if self.photo_var.get()=="take": self.generate_dataset(sid)
            else: messagebox.showinfo("Saved", "Saved without photo sample.")
            self.load_students(); self.reset_form()
        except Exception as e: messagebox.showerror("Error", str(e))

    def load_students(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.cursor.execute("SELECT department, course, year, semester, student_id, name, class_div, roll_no, gender, dob, phone, email, address, teacher FROM students ORDER BY student_id")
        for row in self.cursor.fetchall(): self.tree.insert("", END, values=row)

    def update_student(self):
        selected = self.tree.selection(); sid = self.ent_id.get().strip()
        if not selected: messagebox.showwarning("Warning", "Select a row to update."); return
        try:
            self.cursor.execute("""
                UPDATE students SET name=%s, department=%s, course=%s, year=%s, semester=%s,
                class_div=%s, roll_no=%s, gender=%s, dob=%s, phone=%s, email=%s, address=%s, teacher=%s
                WHERE student_id=%s
            """, (self.ent_name.get(), self.cmb_dept.get(), self.cmb_course.get(), self.cmb_year.get(), self.cmb_sem.get(),
                  self.cmb_div.get(), self.ent_roll.get(), self.cmb_gender.get(), self.ent_dob.get(), self.ent_phone.get(),
                  self.ent_email.get(), self.txt_addr.get("1.0", END).strip(), self.ent_teacher.get(), sid))
            self.conn.commit(); messagebox.showinfo("Updated","Student updated successfully."); self.load_students()
        except Exception as e: messagebox.showerror("Error", str(e))

    def delete_student(self):
        sid = self.ent_id.get().strip()
        if not sid: messagebox.showwarning("Warning", "Select a student to delete."); return
        delete = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if delete:
            try:
                self.cursor.execute("DELETE FROM students WHERE student_id=%s", (sid,))
                self.conn.commit()
                folder = "data"
                if os.path.exists(folder):
                    for file in os.listdir(folder):
                        if file.startswith(f"user.{sid}."): os.remove(os.path.join(folder,file))
                messagebox.showinfo("Deleted","Student deleted successfully."); self.load_students(); self.reset_form()
            except Exception as e: messagebox.showerror("Error", str(e))

    def reset_form(self):
        self.ent_id.delete(0, END); self.ent_name.delete(0, END); self.ent_roll.delete(0, END)
        self.ent_dob.delete(0, END); self.ent_phone.delete(0, END); self.ent_email.delete(0, END)
        self.txt_addr.delete("1.0", END); self.ent_teacher.delete(0, END)
        self.cmb_dept.current(0); self.cmb_course.current(0); self.cmb_year.current(0); self.cmb_sem.current(0)
        self.cmb_div.current(0); self.cmb_gender.set("Male"); self.photo_var.set("take")

    def on_row_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.cmb_dept.set(values[0]); self.cmb_course.set(values[1]); self.cmb_year.set(values[2])
            self.cmb_sem.set(values[3]); self.ent_id.delete(0, END); self.ent_id.insert(0, values[4])
            self.ent_name.delete(0, END); self.ent_name.insert(0, values[5]); self.cmb_div.set(values[6])
            self.ent_roll.delete(0, END); self.ent_roll.insert(0, values[7]); self.cmb_gender.set(values[8])
            self.ent_dob.delete(0, END); self.ent_dob.insert(0, values[9]); self.ent_phone.delete(0, END)
            self.ent_phone.insert(0, values[10]); self.ent_email.delete(0, END); self.ent_email.insert(0, values[11])
            self.txt_addr.delete("1.0", END); self.txt_addr.insert(END, values[12]); self.ent_teacher.delete(0, END)
            self.ent_teacher.insert(0, values[13])

    def generate_dataset(self, student_id):
        folder = "data"; os.makedirs(folder, exist_ok=True)
        cam = cv2.VideoCapture(0); count=0
        while True:
            ret, img = cam.read()
            if not ret: break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Capture Photo Sample", gray)
            count+=1; cv2.imwrite(os.path.join(folder,f"user.{student_id}.{count}.jpg"), gray)
            if cv2.waitKey(1)==27 or count>=10: break
        cam.release(); cv2.destroyAllWindows()
        messagebox.showinfo("Saved", "Photo sample captured successfully!")

    def add_photo_sample(self): self.generate_dataset(self.ent_id.get().strip())
    def update_photo_sample(self): self.generate_dataset(self.ent_id.get().strip())
    
    def search_student(self):
        keyword = self.ent_search.get().strip(); field = self.cmb_search.get()
        if field=="Select" or not keyword: self.load_students(); return
        query = f"SELECT department, course, year, semester, student_id, name, class_div, roll_no, gender, dob, phone, email, address, teacher FROM students WHERE {field.lower()} LIKE %s"
        self.cursor.execute(query, (f"%{keyword}%",))
        rows = self.cursor.fetchall()
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in rows: self.tree.insert("", END, values=row)

if __name__=="__main__":
    root = Tk()
    app = StudentApp(root)
    root.mainloop()
