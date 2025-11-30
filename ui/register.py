from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import hashlib
import db
from ui.style import add_hover, fade_in



class RegisterWindow:
    def __init__(self, root):
        self.root = root
        root.title("Register")
        root.geometry("500x650")
        root.resizable(False, False)

        fade_in(root)

        # Background
        try:
            bg = Image.open("assets/bg.jpg").resize((500, 650))
            self.bg_img = ImageTk.PhotoImage(bg)
            Label(root, image=self.bg_img).place(x=0, y=0)
        except:
            root.configure(bg="#dce5ff")

        # Card Frame
        card = Frame(root, bg="white", bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=520)

        Label(card, text="Create Account", font=("Arial", 22, "bold"),
              bg="white").pack(pady=15)

        # Name
        Label(card, text="Name", font=("Arial", 13), bg="white").pack()
        self.name = StringVar()
        Entry(card, textvariable=self.name, width=34, font=("Arial", 12), bd=3).pack(pady=5)

        # Roll Number
        Label(card, text="Roll Number", font=("Arial", 13), bg="white").pack()
        self.roll = StringVar()
        Entry(card, textvariable=self.roll, width=34, font=("Arial", 12), bd=3).pack(pady=5)

        # Section
        Label(card, text="Section", font=("Arial", 13), bg="white").pack()
        self.section = StringVar()
        Entry(card, textvariable=self.section, width=34, font=("Arial", 12), bd=3).pack(pady=5)

        # Password
        Label(card, text="Password", font=("Arial", 13), bg="white").pack()
        self.pwd = StringVar()
        Entry(card, textvariable=self.pwd, width=34, font=("Arial", 12),
              bd=3, show="*").pack(pady=5)

        # Register Button
        btn_reg = Button(card, text="Register", width=18, bg="#28a745", fg="white",
                         font=("Arial", 12, "bold"), command=self.register_user)
        btn_reg.pack(pady=15)
        add_hover(btn_reg, "#28a745", "#1e7e34")

        # Back Button
        btn_back = Button(card, text="Back to Login", width=18, bg="#6c757d", fg="white",
                          font=("Arial", 11, "bold"), command=self.go_back)
        btn_back.pack()
        add_hover(btn_back, "#6c757d", "#555")

    def register_user(self):
        name = self.name.get()
        roll = self.roll.get()
        sec = self.section.get()
        pwd = self.pwd.get()

        if name == "" or roll == "" or sec == "" or pwd == "":
            messagebox.showerror("Error", "All fields are required!")
            return

        hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()

        try:
            db.execute(
                "INSERT INTO students(name, rollno, section, password, score) VALUES(%s,%s,%s,%s,%s)",
                (name, roll, sec, hashed_pwd, 0)
            )
            messagebox.showinfo("Success", "Account created successfully!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def go_back(self):
        self.root.destroy()

        from ui.login import LoginWindow  # SAFE lazy import

        root = Tk()
        LoginWindow(root)


