from tkinter import *
from tkinter import messagebox

# Developer data
devs = [
    {"name": "Vedika Mohite", "role": "Project Manager & Lead Developer", "email": "vedikamohite.@google.com", "phone": "+91 91234 56789"},
    {"name": "Rani Pukale", "role": "Backend Developer", "email": "ranipukale.@google.com", "phone": "+91 98765 43210"},
    {"name": "Samruddhi Nangre-Patil", "role": "Frontend Developer", "email": "samruddhipatil.@google.com", "phone": "+91 99876 54321"},
    {"name": "Shreya Jadhav", "role": "Frontend Developer", "email": "shreya.jadhav@google.com", "phone": "+91 99876 54321"}
]

class DeveloperUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System - Developers")
        self.root.geometry("1530x790+0+0")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")

        LEFT_W = 600
        RIGHT_W = 930

        # ===== LEFT PANEL (Gradient style simulated) =====
        left_frame = Frame(self.root, width=LEFT_W, height=790, bg="#1e40af")  # Dark blue
        left_frame.place(x=0, y=0)

        Label(left_frame, text="Face Recognition\nAttendance System", font=("Helvetica", 26, "bold"),
              fg="white", bg="#1e40af", justify=CENTER).place(relx=0.5, rely=0.35, anchor="center")

        Label(left_frame, text="Effortless Attendance Management", font=("Helvetica", 16),
              fg="#cbd5e1", bg="#1e40af").place(relx=0.5, rely=0.50, anchor="center")

        # ===== RIGHT PANEL =====
        right_frame = Frame(self.root, width=RIGHT_W, height=790, bg="#f0f2f5")
        right_frame.place(x=LEFT_W, y=0)

        Label(right_frame, text="Developer Team", font=("Segoe UI", 28, "bold"),
              bg="#f0f2f5", fg="#1e40af").place(x=40, y=40)

        # Container for cards
        cards_frame = Frame(right_frame, bg="#f0f2f5")
        cards_frame.place(x=40, y=120, width=RIGHT_W-80, height=630)

        card_w = (RIGHT_W - 120) // 2
        card_h = 250

        idx = 0
        for r in range(2):
            for c in range(2):
                if idx >= len(devs):
                    break
                d = devs[idx]

                x = c * (card_w + 40)
                y = r * (card_h + 40)

                # Shadow effect
                shadow = Frame(cards_frame, bg="#cbd5e1")
                shadow.place(x=x+4, y=y+4, width=card_w, height=card_h)

                # Card frame
                card = Frame(cards_frame, bg="white", bd=0)
                card.place(x=x, y=y, width=card_w, height=card_h)

                # Top colored bar for card
                top_bar = Frame(card, bg="#1e40af", height=40)
                top_bar.pack(fill=X, side=TOP)

                Label(top_bar, text=d["name"], font=("Segoe UI", 12, "bold"),
                      bg="#1e40af", fg="white").pack(padx=10, pady=5, anchor=W)

                Label(card, text=d["role"], font=("Segoe UI", 11),
                      bg="white", fg="#6b7280").place(x=20, y=60)

                # Email button
                def show_info(txt):
                    return lambda: messagebox.showinfo("Contact Info", txt)

                Button(card, text="📧 "+d["email"], font=("Segoe UI", 10), bg="white",
                       fg="#1e40af", bd=0, cursor="hand2", anchor="w",
                       command=show_info(d["email"])).place(x=20, y=120, width=card_w-40)

                # Phone button
                Button(card, text="📞 "+d["phone"], font=("Segoe UI", 10), bg="white",
                       fg="#1e40af", bd=0, cursor="hand2", anchor="w",
                       command=show_info(d["phone"])).place(x=20, y=155, width=card_w-40)

                idx += 1

if __name__ == "__main__":
    root = Tk()
    DeveloperUI(root)
    root.mainloop()
