from tkinter import *
from tkinter import messagebox
import random
import threading
import time

class HelpUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition - Attendance System")
        self.root.state("zoomed")  # maximize window
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        # ===== BACKGROUND CANVAS WITH GRADIENT & BUBBLES =====
        self.bg_canvas = Canvas(root, width=self.width, height=self.height, highlightthickness=0)
        self.bg_canvas.pack(fill=BOTH, expand=True)
        self.draw_gradient(self.bg_canvas, "#dbeafe", "#bfdbfe")  # subtle light blue gradient

        # Animated bubbles
        self.bubbles = []
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            r = random.randint(10, 30)
            speed = random.uniform(0.5, 1.5)
            bubble = {"oval": self.bg_canvas.create_oval(x-r, y-r, x+r, y+r, fill="#93c5fd", outline="", stipple="gray50"),
                      "x": x, "y": y, "r": r, "speed": speed}
            self.bubbles.append(bubble)

        threading.Thread(target=self.animate_bubbles, daemon=True).start()

        # ===== HEADER FRAME =====
        self.header_frame = Frame(root, bg="#3b82f6", height=120)
        self.header_frame.place(x=0, y=0, width=self.width)

        self.header_label = Label(self.header_frame, text="HELP DESK", font=("Helvetica", 36, "bold"),
                                  fg="white", bg="#3b82f6")
        self.header_label.place(relx=0.5, y=30, anchor=CENTER)

        self.sub_label = Label(self.header_frame, text="Face Recognition Attendance System",
                               font=("Helvetica", 18), fg="#f0f9ff", bg="#3b82f6")
        self.sub_label.place(relx=0.5, y=80, anchor=CENTER)

        # ===== FLOATING CARD WITH SHADOW =====
        self.card_width = 700
        self.card_height = 350

        self.shadow = Canvas(root, width=self.card_width, height=self.card_height, bg="#94a3b8", highlightthickness=0)
        self.shadow.place(relx=0.5, rely=0.5, anchor=CENTER, y=20)

        self.card = Canvas(root, width=self.card_width, height=self.card_height, bg="white", highlightthickness=0)
        self.card.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.round_rectangle(self.card, 10, 10, self.card_width-10, self.card_height-10, radius=20, fill="white")

        self.card.create_text(self.card_width//2, 60, text="For any help, Connect with Us",
                              font=("Helvetica", 26, "bold"), fill="#16a34a")

        # ===== EMAIL & PHONE BUTTONS =====
        self.email_btn = Button(root, text="📧 Email: developerteam4@gmail.com", font=("Helvetica", 18),
                                fg="#1e40af", bg="white", bd=0, cursor="hand2",
                                command=lambda: messagebox.showinfo("Email", "developerteam4@gmail.com"))
        self.email_btn.place(relx=0.5, rely=0.5, anchor=CENTER, y=-10)

        self.phone_btn = Button(root, text="📞 Mobile: 9876543210", font=("Helvetica", 18),
                                fg="#1e40af", bg="white", bd=0, cursor="hand2",
                                command=lambda: messagebox.showinfo("Phone", "9876543210"))
        self.phone_btn.place(relx=0.5, rely=0.5, anchor=CENTER, y=60)

        # ===== FOOTER =====
        self.footer = Label(root, text="© 2025 Face Recognition Attendance System", font=("Helvetica", 12),
                            fg="#6b7280", bg="#dbeafe")
        self.footer.place(relx=0.5, rely=0.95, anchor=CENTER)

        # Hover effect
        self.add_hover(self.email_btn)
        self.add_hover(self.phone_btn)

        # Animate card
        threading.Thread(target=self.animate_card, daemon=True).start()

    # Hover effect
    def add_hover(self, widget):
        def on_enter(e):
            widget.config(fg="#2563eb")
        def on_leave(e):
            widget.config(fg="#1e40af")
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    # Rounded rectangle
    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    # Gradient background
    def draw_gradient(self, canvas, color1, color2):
        width = self.width
        height = canvas.winfo_height()
        (r1,g1,b1) = canvas.winfo_rgb(color1)
        (r2,g2,b2) = canvas.winfo_rgb(color2)
        r_ratio = float(r2 - r1) / height
        g_ratio = float(g2 - g1) / height
        b_ratio = float(b2 - b1) / height
        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr>>8:02x}{ng>>8:02x}{nb>>8:02x}'
            canvas.create_line(0,i,width,i,fill=color)

    # Animate card floating
    def animate_card(self):
        y = 0
        direction = 1
        while True:
            self.card.place_configure(relx=0.5, rely=0.5, anchor=CENTER, y=y)
            self.shadow.place_configure(relx=0.5, rely=0.5, anchor=CENTER, y=y+20)
            y += direction
            if y > 10 or y < -10:
                direction *= -1
            time.sleep(0.05)

    # Animate bubbles
    def animate_bubbles(self):
        while True:
            for bubble in self.bubbles:
                bubble["y"] -= bubble["speed"]
                if bubble["y"] + bubble["r"] < 0:
                    bubble["y"] = self.height + bubble["r"]
                    bubble["x"] = random.randint(0, self.width)
                self.bg_canvas.coords(bubble["oval"], bubble["x"]-bubble["r"], bubble["y"]-bubble["r"], bubble["x"]+bubble["r"], bubble["y"]+bubble["r"])
            time.sleep(0.03)

if __name__ == "__main__":
    root = Tk()
    app = HelpUI(root)
    root.mainloop()
