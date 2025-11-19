from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

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
FONT_LABEL = ("Segoe UI", 10)
FONT_BTN = ("Segoe UI", 10, "bold")

# ----------------- STUDENT APP -----------------
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management - Face Attendance")
        self.root.geometry("1200x720")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Connect to Neon Cloud DB
        try:
            self.conn = psycopg2.connect(DB_URL)
            self.cursor = self.conn.cursor()
            print("✅ Cloud DB Connected Successfully")
        except Exception as e:
            messagebox.showerror("DB Connection Error", str(e))
            return

        self.create_table_db()

        # UI
        self.create_header()
        content = Frame(self.root, bg=BG_COLOR)
        content.place(x=20, y=100, width=1160, height=580)

        self.left_panel = Frame(content, bg=PANEL_BG)
        self.left_panel.place(x=0, y=0, width=560, height=580)
        self.right_panel = Frame(content, bg=BG_COLOR)
        self.right_panel.place(x=580, y=0, width=580, height=580)

        self.create_form(self.left_panel)
        self.create_table(self.right_panel)
        self.load_students()

    # ----------------- HEADER -----------------
    def create_header(self):
        header = Frame(self.root, bg=CARD)
        header.place(x=0, y=0, width=1200, height=90)
        Label(header, text="STUDENT DETAILS", bg=CARD, fg=TEXT_LIGHT, font=FONT_TITLE).place(x=20, y=10)
        Label(header, text="Face Recognition Attendance", bg=CARD, fg=TEXT_MUTED, font=FONT_SUB).place(x=22, y=52)

    # ----------------- FORM -----------------
    def create_form(self, parent):
        form_title = Label(parent, text="Student Information", bg=PANEL_BG, fg=TEXT_LIGHT, font=("Segoe UI", 14, "bold"))
        form_title.place(x=12, y=12)

        frm = Frame(parent, bg=PANEL_BG)
        frm.place(x=12, y=50, width=536, height=500)

        # Department, Course, Year, Semester
        Label(frm, text="Department", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=0)
        self.cmb_dept = ttk.Combobox(frm, values=["Select", "Computer", "IT", "Mechanical"], state="readonly")
        self.cmb_dept.current(0); self.cmb_dept.place(x=0, y=22, width=160)

        Label(frm, text="Course", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=180, y=0)
        self.cmb_course = ttk.Combobox(frm, values=["Select", "BE", "BSc", "Diploma"], state="readonly")
        self.cmb_course.current(0); self.cmb_course.place(x=180, y=22, width=160)

        Label(frm, text="Year", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=360, y=0)
        self.cmb_year = ttk.Combobox(frm, values=["Select", "2020-21", "2021-22", "2022-23"], state="readonly")
        self.cmb_year.current(0); self.cmb_year.place(x=360, y=22, width=160)

        Label(frm, text="Semester", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=60)
        self.cmb_sem = ttk.Combobox(frm, values=["Select", "Semester-1", "Semester-2"], state="readonly")
        self.cmb_sem.current(0); self.cmb_sem.place(x=0, y=82, width=160)

        # Student ID, Name, Division, Roll No
        Label(frm, text="Student ID", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=120)
        self.ent_id = Entry(frm); self.ent_id.place(x=0, y=142, width=160)

        Label(frm, text="Student Name", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=180, y=120)
        self.ent_name = Entry(frm); self.ent_name.place(x=180, y=142, width=340)

        Label(frm, text="Class Div", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=180)
        self.cmb_div = ttk.Combobox(frm, values=["Select", "A", "B", "C"], state="readonly"); self.cmb_div.current(0)
        self.cmb_div.place(x=0, y=202, width=160)

        Label(frm, text="Roll No", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=180, y=180)
        self.ent_roll = Entry(frm); self.ent_roll.place(x=180, y=202, width=160)

        # Gender, DOB, Phone
        Label(frm, text="Gender", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=360, y=180)
        self.cmb_gender = ttk.Combobox(frm, values=["Male", "Female", "Other"], state="readonly"); self.cmb_gender.set("Male")
        self.cmb_gender.place(x=360, y=202, width=160)

        Label(frm, text="DOB (DD-MM-YYYY)", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=240)
        self.ent_dob = Entry(frm); self.ent_dob.place(x=0, y=262, width=160)

        Label(frm, text="Phone No", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=180, y=240)
        self.ent_phone = Entry(frm); self.ent_phone.place(x=180, y=262, width=160)

        # Email, Address, Teacher
        Label(frm, text="Email", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=300)
        self.ent_email = Entry(frm); self.ent_email.place(x=0, y=322, width=340)

        Label(frm, text="Address", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=0, y=360)
        self.txt_addr = Text(frm, height=3, width=40); self.txt_addr.place(x=0, y=382)

        Label(frm, text="Teacher Name", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL).place(x=360, y=300)
        self.ent_teacher = Entry(frm); self.ent_teacher.place(x=360, y=322, width=160)

        # Buttons
        Button(frm, text="SAVE", bg=ACCENT, fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#187bcd", command=self.save_student).place(x=10, y=470, width=100, height=36)
        Button(frm, text="UPDATE", bg="#16a085", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#11906f", command=self.update_student).place(x=120, y=470, width=100, height=36)
        Button(frm, text="DELETE", bg="#e74c3c", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#c0392b", command=self.delete_student).place(x=230, y=470, width=100, height=36)
        Button(frm, text="RESET", bg="#7f8c8d", fg=TEXT_LIGHT, font=FONT_BTN, bd=0,
               activebackground="#6b7a7a", command=self.reset_form).place(x=340, y=470, width=100, height=36)

    # ----------------- TABLE -----------------
    def create_table(self, parent):
        search_frame = Frame(parent, bg=BG_COLOR)
        search_frame.place(x=0, y=0, width=580, height=100)
        Label(search_frame, text="Search By", bg=BG_COLOR, fg=TEXT_LIGHT, font=FONT_LABEL).place(x=10, y=10)
        self.cmb_search = ttk.Combobox(search_frame, values=["Select", "StudentID", "StudentName", "RollNo"], state="readonly"); self.cmb_search.current(0)
        self.cmb_search.place(x=80, y=12, width=160)
        self.ent_search = Entry(search_frame); self.ent_search.place(x=260, y=12, width=200)
        Button(search_frame, text="SEARCH", bg=ACCENT, fg=TEXT_LIGHT, font=FONT_BTN, bd=0, command=self.search_student).place(x=470, y=10, width=90)

        table_frame = Frame(parent, bg=BG_COLOR)
        table_frame.place(x=0, y=100, width=580, height=480)
        style = ttk.Style(); style.theme_use("clam")
        style.configure("Treeview", background="#f0f4f8", foreground="#111827", rowheight=28, fieldbackground="#f0f4f8")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        cols = ("Department", "Course", "Year", "Semester", "StudentID", "StudentName", "Class Div", "Roll No")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=100, anchor=CENTER)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set); vsb.pack(side=RIGHT, fill=Y); self.tree.pack(fill=BOTH, expand=1)
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

    # ----------------- CRUD -----------------
    def save_student(self):
        sid = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        if not sid or not name:
            messagebox.showwarning("Warning", "Student ID and Name required!")
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
            messagebox.showinfo("Saved", "Student saved successfully.")
            self.load_students()
            self.reset_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_students(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.cursor.execute("SELECT department, course, year, semester, student_id, name, class_div, roll_no FROM students")
        for row in self.cursor.fetchall(): self.tree.insert("", END, values=row)

    def update_student(self):
        selected = self.tree.selection()
        if not selected: messagebox.showwarning("Warning", "Select a row to update."); return
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

    def delete_student(self):
        selected = self.tree.selection()
        if not selected: messagebox.showwarning("Warning", "Select a row to delete."); return
        sid = self.tree.item(selected[0])["values"][4]
        try:
            self.cursor.execute("DELETE FROM students WHERE student_id=%s", (sid,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Student deleted successfully.")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_form(self):
        self.ent_id.delete(0, END); self.ent_name.delete(0, END); self.ent_roll.delete(0, END)
        self.ent_dob.delete(0, END); self.ent_phone.delete(0, END); self.ent_email.delete(0, END)
        self.txt_addr.delete("1.0", END); self.ent_teacher.delete(0, END)
        self.cmb_dept.current(0); self.cmb_course.current(0); self.cmb_year.current(0)
        self.cmb_sem.current(0); self.cmb_div.current(0); self.cmb_gender.set("Male")

    def search_student(self):
        key = self.cmb_search.get(); txt = self.ent_search.get().strip().lower()
        if key=="Select" or not txt: messagebox.showwarning("Warning", "Select type and enter text."); return
        for item in self.tree.get_children():
            vals = self.tree.item(item)["values"]
            field_map = {"StudentID":4, "StudentName":5, "RollNo":7}
            idx = field_map.get(key, None)
            if idx is not None:
                if txt in str(vals[idx]).lower():
                    self.tree.selection_set(item); self.tree.see(item)
                    return
        messagebox.showinfo("Not Found", "No matching records found.")

    def on_row_select(self, event):
        sel = self.tree.focus()
        if not sel: return
        vals = self.tree.item(sel,"values")
        try:
            self.cmb_dept.set(vals[0]); self.cmb_course.set(vals[1]); self.cmb_year.set(vals[2])
            self.cmb_sem.set(vals[3]); self.ent_id.delete(0,END); self.ent_id.insert(0,vals[4])
            self.ent_name.delete(0,END); self.ent_name.insert(0,vals[5]); self.cmb_div.set(vals[6])
            self.ent_roll.delete(0,END); self.ent_roll.insert(0,vals[7])
        except: pass

if __name__ == "__main__":
    root = Tk()
    app = StudentApp(root)
    root.mainloop()
