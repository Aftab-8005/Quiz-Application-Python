from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import db
from ui.style import add_hover, fade_in


class LeaderboardWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Leaderboard")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        fade_in(self.root)

        # Background
        try:
            bg = Image.open("assets/bg.jpg").resize((900, 600))
            self.bg_img = ImageTk.PhotoImage(bg)
            Label(self.root, image=self.bg_img).place(x=0, y=0)
        except:
            self.root.configure(bg="#ecf0f1")

        # Main Card
        card = Frame(self.root, bg="white", bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=750, height=450)

        Label(card, text="🏆 Leaderboard", font=("Arial", 28, "bold"),
              bg="white", fg="#222").pack(pady=20)

        table_frame = Frame(card, bg="white")
        table_frame.pack()

        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(
            table_frame,
            columns=("Rank", "Roll", "Name", "Section", "Score"),
            show="headings",
            height=12,
            yscrollcommand=scrollbar.set
        )

        self.table.column("Rank", width=70, anchor=CENTER)
        self.table.column("Roll", width=120, anchor=CENTER)
        self.table.column("Name", width=200, anchor=W)
        self.table.column("Section", width=120, anchor=CENTER)
        self.table.column("Score", width=80, anchor=CENTER)

        self.table.heading("Rank", text="Rank")
        self.table.heading("Roll", text="Roll No.")
        self.table.heading("Name", text="Name")
        self.table.heading("Section", text="Section")
        self.table.heading("Score", text="Score")

        self.table.pack()
        scrollbar.config(command=self.table.yview)

        self.load_data()

        btn_close = Button(card, text="Close", font=("Arial", 14, "bold"),
                           bg="#6c757d", fg="white", width=10,
                           command=self.root.destroy)
        btn_close.pack(pady=15)
        add_hover(btn_close, "#6c757d", "#555")

    def load_data(self):
        data = db.fetchall("SELECT rollno, name, section, score FROM students ORDER BY score DESC LIMIT 10")
        rank = 1
        for row in data:
            self.table.insert("", END,
                              values=(rank, row[0], row[1], row[2], row[3]))
            rank += 1
