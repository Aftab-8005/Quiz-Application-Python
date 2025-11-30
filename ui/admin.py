from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import db
from ui.style import add_hover, fade_in


class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        fade_in(self.root)

        # Background
        try:
            bg = Image.open("assets/bg.jpg").resize((1000, 650))
            self.bg_img = ImageTk.PhotoImage(bg)
            Label(self.root, image=self.bg_img).place(x=0, y=0)
        except:
            self.root.configure(bg="#eef2f3")

        # Main Card
        main_card = Frame(self.root, bg="white")
        main_card.place(relx=0.5, rely=0.5, anchor="center", width=900, height=550)

        Label(main_card, text="ADMIN PANEL", font=("Arial", 26, "bold"),
              bg="white", fg="#222").pack(pady=10)

        tabs = ttk.Notebook(main_card)
        tabs.pack(expand=True, fill="both")

        # TAB 1: ADD QUESTION
        add_tab = Frame(tabs, bg="white")
        tabs.add(add_tab, text="Add Question")

        Label(add_tab, text="Add New Question", font=("Arial", 20, "bold"),
              bg="white").pack(pady=10)

        self.q_text = StringVar()
        Entry(add_tab, textvariable=self.q_text, font=("Arial", 14),
              width=60).pack(pady=5)

        self.op1 = StringVar()
        self.op2 = StringVar()
        self.op3 = StringVar()
        self.op4 = StringVar()

        Entry(add_tab, textvariable=self.op1, font=("Arial", 12),
              width=40).pack(pady=5)
        Entry(add_tab, textvariable=self.op2, font=("Arial", 12),
              width=40).pack(pady=5)
        Entry(add_tab, textvariable=self.op3, font=("Arial", 12),
              width=40).pack(pady=5)
        Entry(add_tab, textvariable=self.op4, font=("Arial", 12),
              width=40).pack(pady=5)

        Label(add_tab, text="Correct Option (0-3)", font=("Arial", 12),
              bg="white").pack()
        self.correct = StringVar()
        Entry(add_tab, textvariable=self.correct, width=10).pack()

        Label(add_tab, text="Difficulty", font=("Arial", 12),
              bg="white").pack(pady=5)

        self.diff = StringVar()
        difficulty_menu = ttk.Combobox(add_tab, textvariable=self.diff,
                                       values=["easy", "medium", "hard"],
                                       width=10, state="readonly")
        difficulty_menu.pack()

        btn_add = Button(add_tab, text="Add Question", bg="#28a745", fg="white",
                         font=("Arial", 14, "bold"), command=self.add_question)
        btn_add.pack(pady=20)
        add_hover(btn_add, "#28a745", "#1e7e34")

        # TAB 2: MANAGE QUESTIONS
        manage_tab = Frame(tabs, bg="white")
        tabs.add(manage_tab, text="Manage Questions")

        self.question_table = ttk.Treeview(
            manage_tab,
            columns=("ID", "Q", "O1", "O2", "O3", "O4", "Correct", "Diff"),
            show="headings"
        )
        self.question_table.pack(fill="both", expand=True)

        for col in self.question_table["columns"]:
            self.question_table.column(col, width=100)
            self.question_table.heading(col, text=col)

        self.load_questions()

        btn_del = Button(manage_tab, text="Delete Selected",
                         bg="#dc3545", fg="white",
                         font=("Arial", 14), command=self.delete_question)
        btn_del.pack(pady=10)
        add_hover(btn_del, "#dc3545", "#b52a37")

        # TAB 3: STUDENTS
        student_tab = Frame(tabs, bg="white")
        tabs.add(student_tab, text="Students")

        self.student_table = ttk.Treeview(
            student_tab,
            columns=("Roll", "Name", "Section", "Score"),
            show="headings"
        )
        self.student_table.pack(fill="both", expand=True)

        for col in self.student_table["columns"]:
            self.student_table.column(col, width=150)
            self.student_table.heading(col, text=col)

        self.load_students()

        btn_reset = Button(student_tab, text="Reset All Scores",
                           bg="#ffa500", fg="white",
                           font=("Arial", 14), command=self.reset_scores)
        btn_reset.pack(pady=10)
        add_hover(btn_reset, "#ffa500", "#e69500")

    # FUNCTIONS

    def add_question(self):
        q = self.q_text.get()
        o1, o2, o3, o4 = self.op1.get(), self.op2.get(), self.op3.get(), self.op4.get()
        correct = self.correct.get()
        diff = self.diff.get()

        if not q or not o1 or not o2 or not o3 or not o4 or not correct or not diff:
            messagebox.showerror("Error", "All fields required")
            return

        db.execute(
            "INSERT INTO questions (question, op1, op2, op3, op4, correct, difficulty) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (q, o1, o2, o3, o4, correct, diff)
        )

        messagebox.showinfo("Success", "Question Added Successfully!")
        self.question_table.delete(*self.question_table.get_children())
        self.load_questions()

    def load_questions(self):
        self.question_table.delete(*self.question_table.get_children())
        data = db.fetchall("SELECT * FROM questions")
        for row in data:
            self.question_table.insert("", END, values=row)

    def delete_question(self):
        selected = self.question_table.selection()
        if not selected:
            messagebox.showerror("Error", "Select a row first!")
            return

        q_id = self.question_table.item(selected)["values"][0]
        db.execute("DELETE FROM questions WHERE id=%s", (q_id,))
        messagebox.showinfo("Deleted", "Question deleted!")
        self.load_questions()

    def load_students(self):
        self.student_table.delete(*self.student_table.get_children())
        data = db.fetchall("SELECT rollno, name, section, score FROM students ORDER BY score DESC")
        for row in data:
            self.student_table.insert("", END, values=row)

    def reset_scores(self):
        db.execute("UPDATE students SET score=0")
        messagebox.showinfo("Success", "All scores reset!")
        self.load_students()
