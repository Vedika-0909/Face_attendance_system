import psycopg2
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# ============= DATABASE ===============
DB_URL = "postgresql://neondb_owner:npg_QbefUI5gLEq7@ep-quiet-union-a1c1sfqv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def connect_db():
    return psycopg2.connect(DB_URL)
# ======================================


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition - Login")
        self.root.state("zoomed")

        # ---------------- BACKGROUND ----------------
        bg = Image.open("images/login_bg..jpeg")
        bg = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.bg_img = ImageTk.PhotoImage(bg)

        Label(self.root, image=self.bg_img).place(x=0, y=0)

        # ---------------- LOGIN FRAME ----------------
        self.frame = Frame(self.root, bg="white", bd=2, relief="flat")
        self.frame.place(relx=0.75, rely=0.5, anchor=CENTER, width=500, height=500)

        title = Label(
            self.frame,
            text="Login to Continue",
            font=("Arial Rounded MT Bold", 26),
            bg="white",
            fg="#0064dd"
        )
        title.pack(pady=30)

        # ------------- Username ----------------
        Label(self.frame, text="Username",
              font=("Arial", 13), bg="white", fg="#333").pack(anchor="w", padx=70)

        self.username = Entry(
            self.frame, font=("Arial", 14), bd=1, relief=SOLID
        )
        self.username.pack(fill="x", padx=70, pady=(0, 15), ipady=6)

        # ------------- Password ----------------
        Label(self.frame, text="Password",
              font=("Arial", 13), bg="white", fg="#333").pack(anchor="w", padx=70)

        self.password = Entry(
            self.frame, font=("Arial", 14), bd=1, relief=SOLID, show="*"
        )
        self.password.pack(fill="x", padx=70, pady=(0, 5), ipady=6)

        # Show Password
        self.show_pass = BooleanVar()
        Checkbutton(
            self.frame,
            text="Show Password",
            variable=self.show_pass,
            command=self.toggle_password,
            bg="white",
            fg="#333",
            activebackground="white",
            selectcolor="white",
            font=("Arial", 10)
        ).pack(anchor="w", padx=70)

        # ------------- Login Button -------------
        self.login_btn = Button(
            self.frame,
            text="LOGIN",
            font=("Arial Rounded MT Bold", 15),
            bg="#0077ff",
            fg="white",
            bd=0,
            cursor="hand2",
            activebackground="#005fd4",
            command=self.login
        )
        self.login_btn.pack(pady=30, ipadx=20, ipady=6)

        # Hover effect
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#005fd4"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#0077ff"))

        # ------------- Forgot Password -------------
        Button(
            self.frame,
            text="Forgot Password?",
            font=("Arial", 11),
            bd=0,
            bg="white",
            fg="#0064dd",
            cursor="hand2",
            activebackground="white",
            command=self.forgot_password
        ).pack()

    # Toggle password
    def toggle_password(self):
        if self.show_pass.get():
            self.password.config(show="")
        else:
            self.password.config(show="*")

    # Login Function
        # Login Function
    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user == "" or pwd == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (user, pwd)
            )
            row = cur.fetchone()
            conn.close()

            if row:
                messagebox.showinfo("Success", "Login Successful!")
                
                # Close login window
                self.root.destroy()

                # Open main dashboard
                import subprocess
                subprocess.Popen(["python", "main.py"])

            else:
                messagebox.showerror("Error", "Invalid Username or Password")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))


    # Forgot password action
    def forgot_password(self):
    
        import subprocess
        import os

        reset_file = "reset_password.py"   # reset screen ka file

        if os.path.exists(reset_file):
            subprocess.Popen(["python", reset_file])
        else:
            messagebox.showerror("Error", "reset_password.py file not found!")



# MAIN
if __name__ == "__main__":
    root = Tk()
    LoginWindow(root)
    root.mainloop()
