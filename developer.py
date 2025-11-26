from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

devs = [
   
    {"name": "Vedika Mohite", "role": "Project Manager & Lead Developer", "email": "vedikamohite.@google.com", "phone": "+91 91234 56789"},
     {"name": "Rani Pukale", "role": "Backend Developer", "email": "ranipukale.@google.com", "phone": "+91 98765 43210"},
    {"name": "Samruddhi Nangre-Patil", "role": "Frontend Develope", "email": "samruddhipatil.@google.com", "phone": "+91 99876 54321"},
    {"name": "Shreya Jadhav", "role": "Frontend Develope", "email": "shreya.jadhav@google.com", "phone": "+91 99876 54321"}
]

class HelpUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1530x790+0+0")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        # ===== Title Bar =====
        title_lbl = Label(self.root, text="Developer", font=("Times New Roman", 35, "bold"), 
                          bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=60)

        # ===== Main Layout =====
        LEFT_W = 600        
        RIGHT_W = 930       

        # ===== LEFT SIDE IMAGE =====
        left_frame = Frame(self.root, width=LEFT_W, height=790, bg="black")
        left_frame.place(x=0, y=0)

        try:
            img = Image.open("images\dev.avif")
            img = img.resize((LEFT_W, 790), Image.LANCZOS)
            self.left_photo = ImageTk.PhotoImage(img)
            lbl_img = Label(left_frame, image=self.left_photo, bd=0)
            lbl_img.place(x=0, y=0, width=LEFT_W, height=790)
        except:
            Label(left_frame, text="Image Not Found\n images/D1Image.jpg", fg="white", bg="black",
                  font=("Arial", 14)).place(relx=0.5, rely=0.5, anchor="center")

        # ===== RIGHT SECTION =====
        right_frame = Frame(self.root, width=RIGHT_W, height=790, bg="#f7fafc")
        right_frame.place(x=LEFT_W, y=0)

        heading = Label(right_frame, text="Developer Team", font=("Segoe UI", 26, "bold"), 
                        bg="#f7fafc", fg="#0b5ed7")
        heading.place(x=40, y=80)


        # ===== Cards Grid =====
        cards_frame = Frame(right_frame, bg="#f7fafc")
        cards_frame.place(x=40, y=180, width=RIGHT_W-80, height=560)

        card_w = (RIGHT_W - 120) // 2
        card_h = 250

        idx = 0
        for r in range(2):
            for c in range(2):
                if idx >= len(devs): break
                d = devs[idx]

                x = c * (card_w + 40)
                y = r * (card_h + 40)

                card = Frame(cards_frame, bg="white", bd=2, relief=RIDGE)
                card.place(x=x, y=y, width=card_w, height=card_h)

                Label(card, text=d["name"], font=("Segoe UI", 13, "bold"), bg="white", fg="#0b2545").place(x=110, y=25)
                Label(card, text=d["role"], font=("Segoe UI", 11), bg="white", fg="#6b7280").place(x=110, y=55)

                def show_info(txt):
                    return lambda: messagebox.showinfo("Contact Info", txt)

                Button(card, text=d["email"], font=("Segoe UI", 10), bg="white", fg="#0b5ed7", bd=0,
                       cursor="hand2", command=show_info(d["email"])).place(x=20, y=120)

                Button(card, text=d["phone"], font=("Segoe UI", 10), bg="white", fg="#0b5ed7", bd=0,
                       cursor="hand2", command=show_info(d["phone"])).place(x=20, y=150)

                idx += 1


if __name__ == "__main__":
    root = Tk()
    app = HelpUI(root)
    root.mainloop()
