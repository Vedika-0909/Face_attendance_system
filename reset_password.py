import tkinter as tk
from tkinter import messagebox
import psycopg2
import hashlib
import subprocess

# ============= DATABASE ===============
DB_URL = "postgresql://neondb_owner:npg_QbefUI5gLEq7@ep-quiet-union-a1c1sfqv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def connect_db():
    return psycopg2.connect(DB_URL)
# ======================================


# -------------------------
# HASH PASSWORD FUNCTION
# -------------------------
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()


# -------------------------
# UPDATE PASSWORD FUNCTION
# -------------------------
def reset_password():
    username = entry_user.get()
    new_pass = entry_new.get()
    confirm_pass = entry_confirm.get()

    if username == "" or new_pass == "" or confirm_pass == "":
        messagebox.showwarning("Error", "All fields are required")
        return

    if new_pass != confirm_pass:
        messagebox.showerror("Error", "New Password & Confirm Password do not match")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()

        # Check user exists
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if user is None:
            messagebox.showerror("Error", "No user found with this username")
        else:
            hashed = hash_password(new_pass)

            cur.execute(
                "UPDATE users SET password=%s WHERE username=%s",
                (hashed, username)
            )
            conn.commit()
            messagebox.showinfo("Success", "Password reset successfully!\nPlease login again")
            back_to_login()

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("DB Error", str(e))


# -------------------------
# BACK TO LOGIN FUNCTION
# -------------------------
def back_to_login():
    root.destroy()
    subprocess.Popen(["python", "login.py"])


# ---------------------------------------------------
# TKINTER WINDOW (BIG SCREEN)
# ---------------------------------------------------
root = tk.Tk()
root.title("Reset Password")
root.geometry("1000x600")
root.configure(bg="#e6e6e6")

title = tk.Label(
    root,
    text="RESET PASSWORD",
    font=("Arial", 28, "bold"),
    bg="#e6e6e6"
)
title.pack(pady=40)

# FRAME
frame = tk.Frame(root, bg="white", padx=40, pady=40)
frame.pack()

# Username
tk.Label(frame, text="Username", font=("Arial", 14), bg="white").grid(row=0, column=0, sticky="w", pady=10)
entry_user = tk.Entry(frame, font=("Arial", 14), width=40)
entry_user.grid(row=0, column=1)

# New Password
tk.Label(frame, text="New Password", font=("Arial", 14), bg="white").grid(row=1, column=0, sticky="w", pady=10)
entry_new = tk.Entry(frame, show="*", font=("Arial", 14), width=40)
entry_new.grid(row=1, column=1)

# Confirm Password
tk.Label(frame, text="Confirm Password", font=("Arial", 14), bg="white").grid(row=2, column=0, sticky="w", pady=10)
entry_confirm = tk.Entry(frame, show="*", font=("Arial", 14), width=40)
entry_confirm.grid(row=2, column=1)

# RESET BUTTON
tk.Button(
    frame, text="RESET", font=("Arial", 14, "bold"),
    bg="#4CAF50", fg="white", padx=20, pady=8,
    command=reset_password
).grid(row=3, column=1, pady=30)

# BACK BUTTON
tk.Button(
    frame, text="Back to Login", font=("Arial", 12),
    bg="white", fg="#0d6efd", bd=0,
    cursor="hand2",
    command=back_to_login
).grid(row=4, column=1)

root.mainloop()
