from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import psycopg2, subprocess, os, csv
from datetime import datetime, date
import threading

try:
    import pandas as pd
except:
    pd = None

DB_URL = "postgresql://neondb_owner:npg_QbefUI5gLEq7@ep-quiet-union-a1c1sfqv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
MODEL_SCRIPT = "Face_recognition.py"

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Manager")
        try:
            self.root.state('zoomed')
        except:
            self.root.geometry("1400x820")

        self.conn = None
        self.connect_db()

        # ---------------- TOP ----------------
        top = Frame(self.root, bg="#0f1724", height=120)
        top.pack(side=TOP, fill=X)

        Label(top, text="Attendance Dashboard", bg="#0f1724", fg="white",
              font=("Segoe UI", 24, "bold")).place(x=20, y=30)

        self.total_lbl = Label(top, text="Total: --", bg="#0f1724", fg="white", font=("Segoe UI", 12))
        self.total_lbl.place(x=500, y=40)

        self.present_lbl = Label(top, text="Present Today: --", bg="#0f1724", fg="#7efc91", font=("Segoe UI", 12))
        self.present_lbl.place(x=650, y=40)

        self.absent_lbl = Label(top, text="Absent Today: --", bg="#0f1724", fg="#ffa4a4", font=("Segoe UI", 12))
        self.absent_lbl.place(x=850, y=40)

        Button(top, text="Start Face Recognition", bg="#1e90ff", fg="white",
               font=("Segoe UI", 12, "bold"), command=self.start_face_recognition)\
            .place(x=1100, y=35, width=220, height=36)

        # ---------------- BODY ----------------
        body = Frame(self.root, bg="#f6f6f6")
        body.pack(fill=BOTH, expand=True)

        left = Frame(body, bg="white", width=420)
        left.pack(side=LEFT, fill=Y, padx=10, pady=10)

        right = Frame(body, bg="white")
        right.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # ---------------- LEFT PANEL ----------------
        lf = LabelFrame(left, text="Quick Mark / Lookup", bg="white",
                        font=("Segoe UI", 10, "bold"))
        lf.pack(fill=X, padx=10, pady=10)

        Label(lf, text="Student ID", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.sid_entry = Entry(lf, font=("Segoe UI", 11))
        self.sid_entry.grid(row=0, column=1, padx=5, pady=5)
        self.sid_entry.bind("<Return>", lambda e: self.lookup_student())

        Button(lf, text="Lookup", bg="#16a085", fg="white",
               command=self.lookup_student).grid(row=0, column=2, padx=5)

        self.name_var = StringVar()
        self.course_var = StringVar()
        self.roll_var = StringVar()

        Label(lf, text="Name", bg="white").grid(row=1, column=0, padx=5)
        Label(lf, textvariable=self.name_var, bg="white").grid(row=1, column=1, columnspan=2, sticky=W)

        Label(lf, text="Course", bg="white").grid(row=2, column=0, padx=5)
        Label(lf, textvariable=self.course_var, bg="white").grid(row=2, column=1, columnspan=2, sticky=W)

        Label(lf, text="Roll No", bg="white").grid(row=3, column=0, padx=5)
        Label(lf, textvariable=self.roll_var, bg="white").grid(row=3, column=1, columnspan=2, sticky=W)

        Button(lf, text="Mark Present", bg="#1e90ff", fg="white",
               command=self.quick_mark).grid(row=4, column=0, columnspan=3, sticky=EW, padx=5, pady=10)

        # ---------------- ACTION BUTTONS ----------------
        actions = LabelFrame(left, text="Actions", bg="white", font=("Segoe UI", 10, "bold"))
        actions.pack(fill=X, padx=10, pady=10)

        Button(actions, text="Export CSV", bg="#1e90ff", fg="white",
               command=self.export_csv).grid(row=0, column=0, padx=5, pady=5, sticky=EW)

        Button(actions, text="Export Excel", bg="#634ea0", fg="white",
               command=self.export_excel).grid(row=0, column=1, padx=5, pady=5, sticky=EW)

        Button(actions, text="Delete Record", bg="#e74c3c", fg="white",
               command=self.delete_record).grid(row=1, column=0, padx=5, pady=5, sticky=EW)

        Button(actions, text="Update Record", bg="#f1c40f", fg="white",
               command=self.open_update_popup).grid(row=1, column=1, padx=5, pady=5, sticky=EW)

        Button(actions, text="Reset Filters", bg="#16a085", fg="white",
               command=self.reset_filters).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=EW)

        # ---------------- FILTERS ----------------
        ff = LabelFrame(left, text="Filters", bg="white", font=("Segoe UI", 10, "bold"))
        ff.pack(fill=X, padx=10, pady=10)

        self.filter_var = StringVar(value="today")

        Radiobutton(ff, text="Today", variable=self.filter_var, value="today", bg="white").grid(row=0, column=0, sticky=W)
        Radiobutton(ff, text="Single Date", variable=self.filter_var, value="single", bg="white").grid(row=1, column=0, sticky=W)
        Radiobutton(ff, text="Date Range", variable=self.filter_var, value="range", bg="white").grid(row=2, column=0, sticky=W)

        self.single_entry = Entry(ff); self.single_entry.grid(row=1, column=1, padx=5)
        self.from_entry = Entry(ff); self.from_entry.grid(row=2, column=1, padx=5)
        self.to_entry = Entry(ff); self.to_entry.grid(row=2, column=2, padx=5)

        Button(ff, text="Apply Filter", bg="#16a085", fg="white",
               command=self.apply_filter).grid(row=3, column=0, columnspan=3, sticky=EW, padx=5, pady=10)

        # ---------------- RIGHT TABLE ----------------
        cols = ("att_id","student_id","name","course","department","year","semester",
                "class_div","date","time","status")

        self.tree = ttk.Treeview(right, columns=cols, show="headings", selectmode='browse')
        for c in cols:
            self.tree.heading(c, text=c.replace("_"," ").title())
            self.tree.column(c, width=120)
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Load data
        self.apply_filter()
        self.refresh_dashboard()

    # ---------------- DB CONNECT ----------------
    def connect_db(self):
        try:
            self.conn = psycopg2.connect(DB_URL)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    # ---------------- LOOKUP STUDENT ----------------
    def lookup_student(self):
        sid = self.sid_entry.get().strip()
        if not sid:
            return messagebox.showwarning("Missing", "Enter student ID")

        try:
            con = psycopg2.connect(DB_URL); cur = con.cursor()
            cur.execute("SELECT name, course, roll_no FROM students WHERE student_id=%s", (str(sid),))
            r = cur.fetchone()
            cur.close(); con.close()

            if not r:
                messagebox.showinfo("Not Found", "No student found")
                self.name_var.set(""); self.course_var.set(""); self.roll_var.set("")
                return

            self.name_var.set(r[0])
            self.course_var.set(r[1])
            self.roll_var.set(r[2])

        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    # ---------------- QUICK MARK ----------------
    def quick_mark(self):
        sid = self.sid_entry.get().strip()
        if not sid:
            return messagebox.showwarning("Missing", "Enter Student ID")

        try:
            con = psycopg2.connect(DB_URL); cur = con.cursor()

            # check already marked today
            cur.execute("SELECT att_id FROM attendance WHERE student_id=%s AND date=%s",
                        (str(sid), date.today()))
            if cur.fetchone():
                messagebox.showinfo("Already", "Already marked today")
                cur.close(); con.close()
                return

            now = datetime.now().strftime("%H:%M:%S")
            cur.execute(
                "INSERT INTO attendance(student_id, date, time, status) VALUES(%s,%s,%s,%s)",
                (str(sid), date.today(), now, "Present")
            )

            con.commit()
            cur.close(); con.close()

            messagebox.showinfo("Done", "Marked Present")
            self.apply_filter()
            self.refresh_dashboard()

        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    # ---------------- FILTER ----------------
    def apply_filter(self):
        try:
            con = psycopg2.connect(DB_URL); cur = con.cursor()

            q = """
                SELECT 
                    a.att_id,
                    a.student_id,
                    s.name,
                    s.course,
                    s.department,
                    s.year,
                    s.semester,
                    s.class_div,
                    a.date,
                    a.time,
                    a.status
                FROM attendance a
                LEFT JOIN students s
                    ON a.student_id = s.student_id
            """

            params = []
            mode = self.filter_var.get()

            if mode == "today":
                q += " WHERE a.date=%s"
                params = [date.today()]

            elif mode == "single":
                dt = self.single_entry.get().strip()
                if not dt:
                    messagebox.showwarning("Input", "Enter a date (YYYY-MM-DD)")
                    cur.close(); con.close()
                    return
                q += " WHERE a.date=%s"
                params = [dt]

            elif mode == "range":
                d1 = self.from_entry.get().strip(); d2 = self.to_entry.get().strip()
                if not d1 or not d2:
                    messagebox.showwarning("Input", "Enter start and end dates (YYYY-MM-DD)")
                    cur.close(); con.close()
                    return
                q += " WHERE a.date BETWEEN %s AND %s"
                params = [d1, d2]

            q += " ORDER BY a.date DESC, a.time DESC"

            cur.execute(q, tuple(params))
            rows = cur.fetchall()
            cur.close(); con.close()

            for x in self.tree.get_children():
                self.tree.delete(x)

            for r in rows:
                # format date/time values for safety
                r_list = list(r)
                if isinstance(r_list[8], (date, datetime)):
                    r_list[8] = r_list[8].isoformat()
                r_list[9] = str(r_list[9])
                self.tree.insert("", END, values=tuple(r_list))

        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    # ---------------- DASHBOARD ----------------
    def refresh_dashboard(self):
        try:
            con = psycopg2.connect(DB_URL); cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM students")
            total = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM attendance WHERE date=%s AND status='Present'", (date.today(),))
            present = cur.fetchone()[0]

            cur.close(); con.close()

            self.total_lbl.config(text=f"Total: {total}")
            self.present_lbl.config(text=f"Present Today: {present}")
            self.absent_lbl.config(text=f"Absent Today: {total - present}")

        except:
            pass

    # ---------------- ROW SELECT ----------------
    def on_row_select(self, evt):
        # optional: populate quick panel when selecting a row
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        # att_id, student_id, name, course, department, year, semester, class_div, date, time, status
        try:
            self.sid_entry.delete(0, END); self.sid_entry.insert(0, vals[1])
            self.name_var.set(vals[2] or "")
            self.course_var.set(vals[3] or "")
            self.roll_var.set("")  # roll not returned in JOIN query, unless you add it
        except Exception:
            pass

    # ---------------- DELETE ----------------
    def delete_record(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Select", "Select a record to delete")
        vals = self.tree.item(sel[0], "values")
        att_id = vals[0]
        if not messagebox.askyesno("Confirm", "Delete this attendance record?"):
            return
        try:
            con = psycopg2.connect(DB_URL); cur = con.cursor()
            cur.execute("DELETE FROM attendance WHERE att_id=%s", (att_id,))
            con.commit()
            cur.close(); con.close()
            messagebox.showinfo("Deleted", "Record deleted")
            self.apply_filter()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    # ---------------- UPDATE POPUP ----------------
    def open_update_popup(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Select", "Select a record to update")
        vals = self.tree.item(sel[0], "values")
        att_id = vals[0]

        popup = Toplevel(self.root)
        popup.title("Update Record")
        popup.geometry("420x300")
        popup.resizable(False, False)

        Label(popup, text="Student ID").grid(row=0, column=0, padx=8, pady=8, sticky=W)
        e_sid = Entry(popup); e_sid.grid(row=0, column=1, padx=8, pady=8)
        e_sid.insert(0, vals[1])

        Label(popup, text="Name").grid(row=1, column=0, padx=8, pady=8, sticky=W)
        e_name = Entry(popup); e_name.grid(row=1, column=1, padx=8, pady=8)
        e_name.insert(0, vals[2] or "")

        Label(popup, text="Date (YYYY-MM-DD)").grid(row=2, column=0, padx=8, pady=8, sticky=W)
        e_date = Entry(popup); e_date.grid(row=2, column=1, padx=8, pady=8)
        e_date.insert(0, vals[8])

        Label(popup, text="Time (HH:MM:SS)").grid(row=3, column=0, padx=8, pady=8, sticky=W)
        e_time = Entry(popup); e_time.grid(row=3, column=1, padx=8, pady=8)
        e_time.insert(0, vals[9])

        Label(popup, text="Status").grid(row=4, column=0, padx=8, pady=8, sticky=W)
        status_cb = ttk.Combobox(popup, values=["Present", "Absent", "Late"], state="readonly")
        status_cb.grid(row=4, column=1, padx=8, pady=8)
        status_cb.set(vals[10] or "Present")

        def do_update():
            nsid = e_sid.get().strip()
            nname = e_name.get().strip()
            nd = e_date.get().strip()
            nt = e_time.get().strip()
            nstat = status_cb.get().strip()
            if not (nsid and nd and nt):
                return messagebox.showwarning("Input", "Student ID, date and time required")
            try:
                con = psycopg2.connect(DB_URL); cur = con.cursor()
                cur.execute("UPDATE attendance SET student_id=%s, date=%s, time=%s, status=%s WHERE att_id=%s",
                            (str(nsid), nd, nt, nstat, att_id))
                con.commit()
                cur.close(); con.close()
                messagebox.showinfo("Updated", "Record updated")
                popup.destroy()
                self.apply_filter()
                self.refresh_dashboard()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

        Button(popup, text="Save", bg="#1e90ff", fg="white", command=do_update).grid(row=5, column=0, columnspan=2, pady=12, ipadx=10)

    # ---------------- RESET FILTERS ----------------
    def reset_filters(self):
        self.filter_var.set("today")
        self.single_entry.delete(0, END)
        self.from_entry.delete(0, END)
        self.to_entry.delete(0, END)
        self.apply_filter()
        self.refresh_dashboard()

    # ---------------- EXPORT CSV ----------------
    def export_csv(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
            if not path:
                return
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.tree["columns"])
                for r in self.tree.get_children():
                    writer.writerow(self.tree.item(r)["values"])
            messagebox.showinfo("Saved", f"CSV saved: {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- EXPORT EXCEL ----------------
    def export_excel(self):
        if pd is None:
            return messagebox.showerror("Missing", "pandas required for Excel export")
        try:
            path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files","*.xlsx")])
            if not path:
                return
            rows = [self.tree.item(r)["values"] for r in self.tree.get_children()]
            df = pd.DataFrame(rows, columns=self.tree["columns"])
            df.to_excel(path, index=False)
            messagebox.showinfo("Saved", f"Excel saved: {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- FACE ----------------
    def start_face_recognition(self):
        if not os.path.exists(MODEL_SCRIPT):
            return messagebox.showerror("Missing", "Face_recognition.py not found")

        def run():
            try:
                subprocess.run(["python", MODEL_SCRIPT], check=True)
                self.apply_filter()
                self.refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        threading.Thread(target=run, daemon=True).start()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = Tk()
    app = AttendanceApp(root)
    root.mainloop()
