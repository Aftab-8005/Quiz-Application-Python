from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import hashlib
import db

from ui.quiz import QuizWindow
from ui.admin import AdminPanel
from ui.leaderboard import LeaderboardWindow

# STYLE IMPORT
from ui.style import add_hover, fade_in, toggle_theme


class LoginWindow:
    def __init__(self, root):
        self.root = root
        root.title("Login")
        root.geometry("450x630")
        root.resizable(False, False)

        fade_in(root)

        # Background
        try:
            bg = Image.open("assets/bg.jpg").resize((450, 630))
            self.bg_img = ImageTk.PhotoImage(bg)
            bg_label = Label(root, image=self.bg_img, border=0)
            bg_label.place(x=0, y=0)
            bg_label.lower()   # keep image behind all widgets
   
        except:
            root.configure(bg="#dfdfdf")

        # Logo
        try:
            logo = Image.open("assets/logo.jpg").resize((130, 130))
            self.logo_img = ImageTk.PhotoImage(logo)
            Label(root, image=self.logo_img, bg="white").pack(pady=15)
        except:
            Label(root, text="QUIZ APP", font=("Arial", 30, "bold"), bg="white").pack(pady=20)

        Label(root, text="Login", font=("Arial", 26, "bold"), bg="white").pack(pady=10)

        # ROLL NUMBER
        Label(root, text="Roll Number", font=("Arial", 14), bg="white").pack()
        self.roll = StringVar()
        Entry(root, textvariable=self.roll, width=32, font=("Arial", 12), bd=3).pack(pady=8)

        # PASSWORD
        Label(root, text="Password", font=("Arial", 14), bg="white").pack()
        self.pwd = StringVar()
        Entry(root, textvariable=self.pwd, width=32, font=("Arial", 12), bd=3, show="*").pack(pady=8)

        # STUDENT LOGIN
        btn1 = Button(root, text="Login", width=20, bg="#4472c4", fg="white",
                      font=("Arial", 12, "bold"), command=self.student_login)
        btn1.pack(pady=10)
        add_hover(btn1, "#4472c4", "#3352a3")

        # ADMIN LOGIN
        btn2 = Button(root, text="Admin Login", width=20, bg="#6f42c1", fg="white",
                      font=("Arial", 12, "bold"), command=self.admin_login)
        btn2.pack(pady=10)
        add_hover(btn2, "#6f42c1", "#563199")

        # LEADERBOARD
        btn3 = Button(root, text="Leaderboard", width=20, bg="#28a745", fg="white",
                      font=("Arial", 12, "bold"), command=self.open_leaderboard)
        btn3.pack(pady=10)
        add_hover(btn3, "#28a745", "#1e7e34")

        # REGISTER
        btn4 = Button(root, text="Create New Account", width=20, fg="blue",
                      font=("Arial", 11), command=self.open_register)
        btn4.pack(pady=10)
        add_hover(btn4, "white", "#e0e0ff")

        # DARK MODE
        btn_dark = Button(root, text="Dark Mode", width=14, bg="#444", fg="white",
                          font=("Arial", 11, "bold"),
                          command=lambda: toggle_theme(root))
        btn_dark.pack(pady=10)
        add_hover(btn_dark, "#444", "#222")

    # STUDENT LOGIN
    def student_login(self):
        roll = self.roll.get()
        password = hashlib.sha256(self.pwd.get().encode()).hexdigest()

        user = db.fetchone("SELECT * FROM students WHERE rollno=%s AND password=%s",
                           (roll, password))

        if user:
            messagebox.showinfo("Success", "Login Successful!")
            self.root.destroy()
            new = Tk()
            QuizWindow(new, user)
        else:
            messagebox.showerror("Error", "Invalid Credentials!")

    # ADMIN LOGIN
    def admin_login(self):
        admin = db.fetchone("SELECT * FROM admins WHERE username=%s AND password=%s",
                            (self.roll.get(), self.pwd.get()))

        if admin:
            self.root.destroy()
            win = Tk()
            AdminPanel(win)
        else:
            messagebox.showerror("Error", "Invalid Admin Credentials!")

    # OPEN REGISTER
    def open_register(self):
        self.root.destroy()

        from ui.register import RegisterWindow  # safe import

        win = Tk()
        RegisterWindow(win)


    # OPEN LEADERBOARD
    def open_leaderboard(self):
        new = Tk()
        LeaderboardWindow(new)
