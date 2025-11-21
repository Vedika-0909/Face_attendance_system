# Part 1/6
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import cv2
import os

# ----------------- DB CONFIG -----------------
DB_URL = "postgresql://neondb_owner:npg_QbefUI5gLEq7@ep-quiet-union-a1c1sfqv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

BG_COLOR = "#0f1724"          
PANEL_BG = "#0b2545"         # panel background
ACCENT = "#1e90ff"          # buttons, accents (dodgerblue)
CARD = "#0f3b66"            # cards
TEXT_LIGHT = "#ffffff"
TEXT_MUTED = "#cbd5e1"

FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_SUB = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10)
FONT_BTN = ("Segoe UI", 10, "bold")

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management - Face Attendance")
        # allow window to be maximized by user (we'll use root.state in main)
        self.root.configure(bg=BG_COLOR)

        # Connect to Neon Cloud DB
        try:
            self.conn = psycopg2.connect(DB_URL)
            self.cursor = self.conn.cursor()
            print("✅ Cloud DB Connected Successfully")
        except Exception as e:
            messagebox.showerror("DB Connection Error", str(e))
            return

        # ensure DB table exists
        self.create_table_db()

        # UI layout
        # top header
        self.create_header()

        # main panels
        content = Frame(self.root, bg=BG_COLOR)
        content.place(x=20, y=100, relwidth=0.96, relheight=0.80)

        self.left_panel = Frame(content, bg=PANEL_BG)
        self.left_panel.place(x=0, y=0, relwidth=0.47, relheight=1)
        # left: form panel
        self.left_panel = Frame(content, bg=PANEL_BG, bd=0, relief=RIDGE)
        self.left_panel.place(x=0, y=0, width=560, height=580)

        # right: details panel
        self.right_panel = Frame(content, bg=BG_COLOR)
        self.right_panel.place(relx=0.48, y=0, relwidth=0.52, relheight=1)

        self.create_form(self.left_panel)
        self.create_table(self.right_panel)

    def create_header(self):
        header = Frame(self.root, bg=CARD)
        header.place(x=0, y=0, width=1200, height=90)

        title = Label(header, text="STUDENT DETAILS", bg=CARD, fg=TEXT_LIGHT,
                      font=FONT_TITLE)
        title.place(x=20, y=10)

        subtitle = Label(header, text="Face Recognition Attendance", bg=CARD, fg=TEXT_MUTED,
                         font=FONT_SUB)
        subtitle.place(x=22, y=52)

    def create_form(self, parent):
        # Form title
        form_title = Label(parent, text="Student Information", bg=PANEL_BG, fg=TEXT_LIGHT,
                           font=("Segoe UI", 14, "bold"))
        form_title.place(x=12, y=12)

        # Use internal frame for neat spacing
        frm = Frame(parent, bg=PANEL_BG)
        frm.place(x=12, y=50, relwidth=0.95, relheight=0.93)

        # Row 1: Department, Course, Year, Semester
        lbl_dept = Label(frm, text="Department", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_dept.place(x=0, y=0)
        self.cmb_dept = ttk.Combobox(frm, values=["Select", "Computer", "IT", "Mechanical"], state="readonly")
        self.cmb_dept.current(0)
        self.cmb_dept.place(x=0, y=22, width=160)

        lbl_course = Label(frm, text="Course", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_course.place(x=180, y=0)
        self.cmb_course = ttk.Combobox(frm, values=["Select", "BE", "BSc", "Diploma"], state="readonly")
        self.cmb_course.current(0)
        self.cmb_course.place(x=180, y=22, width=160)

        Label(frm, text="Year", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=360, y=0)
        self.cmb_year = ttk.Combobox(frm, values=["Select", "2023-24", "2024-25", "2025-26"], state="readonly")
        self.cmb_year.current(0); self.cmb_year.place(x=360, y=22, width=160)
        lbl_year = Label(frm, text="Year", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_year.place(x=360, y=0)
        self.cmb_year = ttk.Combobox(frm, values=["Select", "2020-21", "2021-22", "2022-23"], state="readonly")
        self.cmb_year.current(0)
        self.cmb_year.place(x=360, y=22, width=160)

        lbl_sem = Label(frm, text="Semester", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_sem.place(x=0, y=60)
        self.cmb_sem = ttk.Combobox(frm, values=["Select", "Semester-1", "Semester-2"], state="readonly")
        self.cmb_sem.current(0); self.cmb_sem.place(x=0, y=82, width=160)
# Part 2/6 (continue)
        # Student ID, Name, Division, Roll No
        Label(frm, text="Student ID", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=120)
        self.ent_id = Entry(frm); self.ent_id.place(x=0, y=142, width=160)
        self.cmb_sem.current(0)
        self.cmb_sem.place(x=0, y=82, width=160)

        # Row 2: Student ID, Name, Division, Roll No
        lbl_id = Label(frm, text="Student ID", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_id.place(x=0, y=120)
        self.ent_id = Entry(frm)
        self.ent_id.place(x=0, y=142, width=160)

        lbl_name = Label(frm, text="Student Name", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_name.place(x=180, y=120)
        self.ent_name = Entry(frm)
        self.ent_name.place(x=180, y=142, width=340)

        Label(frm, text="Class Div", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=180)
        self.cmb_div = ttk.Combobox(frm, values=["Select", "A", "B", "C"], state="readonly")
        self.cmb_div.current(0); self.cmb_div.place(x=0, y=202, width=160)
        lbl_div = Label(frm, text="Class Div", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_div.place(x=0, y=180)
        self.cmb_div = ttk.Combobox(frm, values=["Select", "A", "B", "C"], state="readonly")
        self.cmb_div.current(0)
        self.cmb_div.place(x=0, y=202, width=160)

        lbl_roll = Label(frm, text="Roll No", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_roll.place(x=180, y=180)
        self.ent_roll = Entry(frm)
        self.ent_roll.place(x=180, y=202, width=160)

        # Gender, DOB, Phone
        Label(frm, text="Gender", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=360, y=180)
        self.cmb_gender = ttk.Combobox(frm, values=["Male", "Female", "Other"], state="readonly")
        self.cmb_gender.set("Male")
        # Row 3: Gender, DOB, Phone
        lbl_gender = Label(frm, text="Gender", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_gender.place(x=360, y=180)
        self.cmb_gender = ttk.Combobox(frm, values=["Male", "Female", "Other"], state="readonly")
        self.cmb_gender.set("Male")
        self.cmb_gender.place(x=360, y=202, width=160)

        lbl_dob = Label(frm, text="DOB (DD-MM-YYYY)", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_dob.place(x=0, y=240)
        self.ent_dob = Entry(frm)
        self.ent_dob.place(x=0, y=262, width=160)

        lbl_phone = Label(frm, text="Phone No", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_phone.place(x=180, y=240)
        self.ent_phone = Entry(frm)
        self.ent_phone.place(x=180, y=262, width=160)

        # Row 4: Email, Address, Teacher Name
        lbl_email = Label(frm, text="Email", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_email.place(x=0, y=300)
        self.ent_email = Entry(frm)
        self.ent_email.place(x=0, y=322, width=340)

        Label(frm, text="Address", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=360)
        self.txt_addr = Text(frm, height=3, width=40)
        self.txt_addr.place(x=0, y=382)
        lbl_addr = Label(frm, text="Address", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_addr.place(x=0, y=360)
        self.txt_addr = Text(frm, height=3, width=40)
        self.txt_addr.place(x=0, y=382)

        Label(frm, text="Teacher Name", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=360, y=300)
        self.ent_teacher = Entry(frm)
        self.ent_teacher.place(x=360, y=322, width=160)

        # ---------------- RADIO BUTTONS ----------------
        self.photo_var = StringVar()
        self.photo_var.set("take")

        Radiobutton(frm, text="Take Photo Sample", variable=self.photo_var, value="take",
                    bg=PANEL_BG, fg=TEXT_LIGHT, selectcolor=PANEL_BG).place(x=0, y=440)

        Radiobutton(frm, text="No Photo Sample", variable=self.photo_var, value="no",
                    bg=PANEL_BG, fg=TEXT_LIGHT, selectcolor=PANEL_BG).place(x=180, y=440)
        lbl_teacher = Label(frm, text="Teacher Name", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL)
        lbl_teacher.place(x=360, y=300)
        self.ent_teacher = Entry(frm)
        self.ent_teacher.place(x=360, y=322, width=160)

        # Buttons
        Button(frm, text="SAVE", bg=ACCENT, fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#187bcd", command=self.save_student).place(x=10, y=480, width=100, height=36)

        Button(frm, text="UPDATE", bg="#16a085", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#11906f", command=self.update_student).place(x=120, y=480, width=100, height=36)

        Button(frm, text="DELETE", bg="#e74c3c", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#c0392b", command=self.delete_student).place(x=230, y=480, width=100, height=36)

        Button(frm, text="RESET", bg="#7f8c8d", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#6b7a7a", command=self.reset_form).place(x=340, y=480, width=100, height=36)
        # Buttons row
        btn_save = Button(frm, text="SAVE", bg=ACCENT, fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
                          activebackground="#187bcd", command=self.save_student)
        btn_save.place(x=10, y=470, width=100, height=36)

        btn_update = Button(frm, text="UPDATE", bg="#16a085", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
                            activebackground="#11906f", command=self.update_student)
        btn_update.place(x=120, y=470, width=100, height=36)

        btn_delete = Button(frm, text="DELETE", bg="#e74c3c", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
                            activebackground="#c0392b", command=self.delete_student)
        btn_delete.place(x=230, y=470, width=100, height=36)

        btn_reset = Button(frm, text="RESET", bg="#7f8c8d", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
                            activebackground="#6b7a7a", command=self.reset_form)
        btn_reset.place(x=340, y=470, width=100, height=36)

        # ---------------- PHOTO SAMPLE BUTTONS ----------------
        Button(frm, text="ADD PHOTO SAMPLE", bg="#1e5bd8", fg="white", font=FONT_BTN, bd=0,
               command=self.add_photo_sample).place(x=10, y=525, width=180, height=36)

        Button(frm, text="UPDATE PHOTO SAMPLE", bg="#9327c9", fg="white", font=FONT_BTN, bd=0,
               command=self.update_photo_sample).place(x=200, y=525, width=200, height=36)
# Part 3/6
    # ----------------- TABLE -----------------
       # ----------------- TABLE -----------------
    def create_table(self, parent):

        # search area
        search_frame = Frame(parent, bg=BG_COLOR)
        search_frame.place(x=0, y=0, width=580, height=100)

        Label(search_frame, text="Search By", bg=BG_COLOR, fg=TEXT_LIGHT, font=FONT_LABEL).place(x=10, y=10)
        self.cmb_search = ttk.Combobox(search_frame, values=["Select", "StudentID", "StudentName", "RollNo"], state="readonly")
        self.cmb_search.current(0)

        lbl_search = Label(search_frame, text="Search By", bg=BG_COLOR, fg=TEXT_LIGHT, font=FONT_LABEL)
        lbl_search.place(x=10, y=10)

        self.cmb_search = ttk.Combobox(search_frame, values=["Select", "StudentID", "StudentName", "RollNo"], state="readonly")
        self.cmb_search.current(0)
        self.cmb_search.place(x=80, y=12, width=160)

        self.ent_search = Entry(search_frame)
        self.ent_search.place(x=260, y=12, width=200)

        Button(search_frame, text="SEARCH", bg=ACCENT, fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               command=self.search_student).place(x=470, y=10, width=90)

        self.ent_search = Entry(search_frame)
        self.ent_search.place(x=260, y=12, width=200)

        btn_search = Button(search_frame, text="SEARCH", bg=ACCENT, fg=TEXT_LIGHT, font=FONT_BTN, bd=0, command=self.search_student)
        btn_search.place(x=470, y=10, width=90)

        # treeview frame
        table_frame = Frame(parent, bg=BG_COLOR)
        table_frame.place(x=0, y=100, width=780, height=480)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#f0f4f8", foreground="#111827", rowheight=28, fieldbackground="#f0f4f8")
        table_frame.place(x=0, y=100, width=580, height=480)

        # Treeview style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#f0f4f8",
                        foreground="#111827",
                        rowheight=28,
                        fieldbackground="#f0f4f8")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        cols = (
            "Department", "Course", "Year", "Semester",
            "StudentID", "StudentName", "Class Div", "Roll No",
            "Gender", "DOB", "Phone", "Email", "Address", "Teacher"
        )

        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)

            if c in ("Address", "Email"):
                self.tree.column(c, width=200, anchor=CENTER)
            elif c == "Teacher":
                self.tree.column(c, width=150, anchor=CENTER)
            else:
                self.tree.column(c, width=120, anchor=CENTER)

        # Scrollbars
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, anchor=CENTER)

    
        # vertical scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=RIGHT, fill=Y)
        hsb.pack(side=BOTTOM, fill=X)

        self.tree.pack(fill=BOTH, expand=1)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=1)

        # bind row select
        self.tree.bind("<ButtonRelease-1>", self.on_row_select)


    # ----------------- DB OPERATIONS -----------------
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

    # ----------------- CRUD: SAVE & LOAD -----------------
    # ---------- Button callbacks (placeholders) ----------
    def save_student(self):
        # Replace with actual save to DB logic
        sid = self.ent_id.get().strip()
        name = self.ent_name.get().strip()

        if not sid or not name:
            messagebox.showwarning("Warning", "Student ID and Name are required!")
            return

        try:
            self.cursor.execute("""
                INSERT INTO students(student_id,name,department,course,year,semester,class_div,roll_no,
                gender,dob,phone,email,address,teacher)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                sid, name, self.cmb_dept.get(), self.cmb_course.get(), self.cmb_year.get(), self.cmb_sem.get(),
                self.cmb_div.get(), self.ent_roll.get(), self.cmb_gender.get(), self.ent_dob.get(),
                self.ent_phone.get(), self.ent_email.get(), self.txt_addr.get("1.0",END).strip(), self.ent_teacher.get()
            ))
            self.conn.commit()

            # Photo Logic
            if self.photo_var.get() == "take":
                self.generate_dataset(sid)
            else:
                messagebox.showinfo("Saved", "Saved without photo sample.")

            self.load_students()
            self.reset_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_students(self):
        # clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # fetch all columns in same order as cols
        self.cursor.execute("""
            SELECT department, course, year, semester, student_id, name, class_div, roll_no,
                   gender, dob, phone, email, address, teacher
            FROM students
            ORDER BY student_id
        """)
        rows = self.cursor.fetchall()
        for row in rows:
            # insert row tuple directly (Treeview expects a sequence)
            self.tree.insert("", END, values=row)
# Part 4/6
        # add to treeview as example
        data = (self.cmb_dept.get(), self.cmb_course.get(), self.cmb_year.get(), self.cmb_sem.get(),
        sid, name, self.cmb_div.get(), self.ent_roll.get())
        self.tree.insert("", END, values=data)
        messagebox.showinfo("Saved", "Student saved locally (sample).")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row to update.")
            return
        sid = self.ent_id.get().strip()

        try:
            self.cursor.execute("""
                UPDATE students SET name=%s, department=%s, course=%s, year=%s, semester=%s,
                class_div=%s, roll_no=%s, gender=%s, dob=%s, phone=%s, email=%s, address=%s, teacher=%s
                WHERE student_id=%s
            """, (
                self.ent_name.get(), self.cmb_dept.get(), self.cmb_course.get(), self.cmb_year.get(), self.cmb_sem.get(),
                self.cmb_div.get(), self.ent_roll.get(), self.cmb_gender.get(), self.ent_dob.get(), self.ent_phone.get(),
                self.ent_email.get(), self.txt_addr.get("1.0", END).strip(), self.ent_teacher.get(), sid
            ))
            self.conn.commit()
            messagebox.showinfo("Updated", "Student updated successfully.")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        if not selected:
            messagebox.showwarning("Warning", "Select a row to update.")
            return
        # Example: update selected with current form values
        for item in selected:
            self.tree.item(item, values=(self.cmb_dept.get(), self.cmb_course.get(), self.cmb_year.get(), self.cmb_sem.get(),
                                         self.ent_id.get(), self.ent_name.get(), self.cmb_div.get(), self.ent_roll.get()))
        messagebox.showinfo("Updated", "Selected row updated (sample).")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row to delete.")
            return

        # student_id is at index 4 in the tree values (as per our cols)
        sid = self.tree.item(selected[0])["values"][4]

        try:
            self.cursor.execute("DELETE FROM students WHERE student_id=%s", (sid,))
            self.conn.commit()

            # Delete photo folder data safely
            if os.path.exists("data"):
                for file in os.listdir("data"):
                    if file.startswith(f"user.{sid}."):
                        try:
                            os.remove(os.path.join("data", file))
                        except:
                            pass

            messagebox.showinfo("Deleted", "Student deleted successfully.")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        if not selected:
            messagebox.showwarning("Warning", "Select a row to delete.")
            return
        for item in selected:
            self.tree.delete(item)
        messagebox.showinfo("Deleted", "Selected record(s) removed (sample).")

    def reset_form(self):
        self.ent_id.delete(0, END)
        self.ent_name.delete(0, END)
        self.ent_roll.delete(0, END)
        self.ent_dob.delete(0, END)
        self.ent_phone.delete(0, END)
        self.ent_email.delete(0, END)
        self.txt_addr.delete("1.0", END)
        self.ent_teacher.delete(0, END)
        self.cmb_dept.current(0)
        self.cmb_course.current(0)
        self.cmb_year.current(0)
        self.cmb_sem.current(0)
        self.cmb_div.current(0)

    def search_student(self):
        key = self.cmb_search.get()
        txt = self.ent_search.get().strip().lower()

        if key=="Select" or not txt:
            messagebox.showwarning("Warning", "Select type and enter text.")
            return

        # map field names to tree index (based on cols)
        field_map = {"StudentID":4, "StudentName":5, "RollNo":7}
        idx = field_map.get(key, None)
        if idx is None:
            messagebox.showwarning("Warning", "Invalid search type.")
            return

        key = self.cmb_search.get()
        txt = self.ent_search.get().strip().lower()
        if key == "Select" or not txt:
            messagebox.showwarning("Warning", "Select search type and enter text.")
            return
        # simple filter on treeview items (sample)
        for item in self.tree.get_children():
            vals = self.tree.item(item)["values"]
            if txt in str(vals[idx]).lower():
                self.tree.selection_set(item)
                self.tree.see(item)
                return

            field_map = {"StudentID": 4, "StudentName": 5, "RollNo": 7}
            idx = field_map.get(key, None)
            if idx is not None:
                if txt in str(vals[idx]).lower():
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    return
        messagebox.showinfo("Not Found", "No matching records found.")

    def on_row_select(self, event):
        sel = self.tree.focus()
        if not sel:
            return

        vals = self.tree.item(sel,"values")

        if not sel:
            return
        vals = self.tree.item(sel, "values")
        # populate form with selected
        try:
            # populate form fields (indexes based on cols order)
            self.cmb_dept.set(vals[0]); self.cmb_course.set(vals[1]); self.cmb_year.set(vals[2])
            self.cmb_sem.set(vals[3]); self.ent_id.delete(0,END); self.ent_id.insert(0,vals[4])
            self.ent_name.delete(0,END); self.ent_name.insert(0,vals[5]); self.cmb_div.set(vals[6])
            self.ent_roll.delete(0,END); self.ent_roll.insert(0,vals[7])
            # additional fields
            try: self.cmb_gender.set(vals[8])
            except: pass
            try: self.ent_dob.delete(0,END); self.ent_dob.insert(0, vals[9])
            except: pass
            try: self.ent_phone.delete(0,END); self.ent_phone.insert(0, vals[10])
            except: pass
            try: self.ent_email.delete(0,END); self.ent_email.insert(0, vals[11])
            except: pass
            try:
                self.txt_addr.delete("1.0", END)
                self.txt_addr.insert("1.0", vals[12])
            except: pass
            try: self.ent_teacher.delete(0,END); self.ent_teacher.insert(0, vals[13])
            except: pass
        except Exception as e:
            # ignore populate errors but print in console
            print("Row select error:", e)
# Part 5/6
    # ---------------------- CAMERA & PHOTO FUNCTIONS ----------------------
    def generate_dataset(self, student_id):
        if not os.path.exists("data"):
            os.makedirs("data")

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            messagebox.showerror("Camera Error", "Cannot access webcam. Make sure camera is connected and not used by another app.")
            return

        count = 0
        messagebox.showinfo("INFO", "Capturing photos... Look at the camera. Press Enter to stop early.")

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            count += 1
            file_name = f"data/user.{student_id}.{count}.jpg"
            cv2.imwrite(file_name, frame)

            cv2.imshow("Capturing", frame)

            # stop on Enter (13) or when 50 images captured
            if cv2.waitKey(1) == 13 or count >= 50:
                break

        cam.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", f"Photo samples captured successfully ({count} images).")

    def add_photo_sample(self):
        sid = self.ent_id.get().strip()
        if sid == "":
            messagebox.showwarning("Warning", "Enter Student ID first!")
            return

        self.generate_dataset(sid)

    def update_photo_sample(self):
        sid = self.ent_id.get().strip()
        if sid == "":
            messagebox.showwarning("Warning", "Enter Student ID first!")
            return

        # Delete old images if any
        if os.path.exists("data"):
            for file in os.listdir("data"):
                if file.startswith(f"user.{sid}."):
                    try:
                        os.remove(os.path.join("data", file))
                    except:
                        pass

        messagebox.showinfo("INFO", "Old samples deleted (if existed). Capturing new photos...")
        self.generate_dataset(sid)
# ----------------- RUN APP -----------------
        self.cmb_dept.set(vals[0])
        self.cmb_course.set(vals[1])
        self.cmb_year.set(vals[2])
        self.cmb_sem.set(vals[3])
        self.ent_id.delete(0, END); self.ent_id.insert(0, vals[4])
        self.ent_name.delete(0, END); self.ent_name.insert(0, vals[5])
        self.cmb_div.set(vals[6])
        self.ent_roll.delete(0, END); self.ent_roll.insert(0, vals[7])
except Exception:
pass

if __name__ == "__main__":
    root = Tk()
    # start maximized so frames get full area
    try:
        root.state('zoomed')
    except:
        # fallback: set large geometry
        root.geometry("1600x900+0+0")
    root.resizable(True, True)
    app = StudentApp(root)
    root.mainloop()
