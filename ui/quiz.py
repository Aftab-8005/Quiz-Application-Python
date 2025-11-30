from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import db
from ui.style import add_hover, fade_in


class QuizWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Python Quiz")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        fade_in(self.root)

        # Background Image
        try:
            bg = Image.open("assets/bg.jpg").resize((900, 600))
            self.bg_img = ImageTk.PhotoImage(bg)
            Label(self.root, image=self.bg_img).place(x=0, y=0)
        except:
            self.root.configure(bg="#ecf0f1")

        # Load 10 random questions
        self.questions = db.fetchall("SELECT * FROM questions ORDER BY RAND() LIMIT 10")
        self.index = 0
        self.score = 0
        self.time_left = 30
        self.timer_running = False

        # Main quiz card
        self.card = Frame(self.root, bg="white", bd=0, highlightthickness=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=450)

        # Timer Label
        self.timer_label = Label(self.card, text="⏳ 30s",
                                 font=("Arial", 16, "bold"),
                                 bg="white", fg="green")
        self.timer_label.place(x=550, y=20)

        # Progress Label
        self.progress = Label(self.card, text="Question 1 of 10",
                              font=("Arial", 14, "bold"), bg="white")
        self.progress.place(x=20, y=20)

        # Question Label
        self.question_text = Label(self.card, text="Loading...",
                                   wraplength=600, justify="left",
                                   font=("Arial", 18, "bold"),
                                   bg="white")
        self.question_text.place(x=20, y=70)

        # Selected option
        self.selected = IntVar()
        self.selected.set(-1)

        # Options (radio buttons)
        self.opts = []
        y_pos = 150
        for i in range(4):
            rb = Radiobutton(self.card, text="", font=("Arial", 16),
                             bg="white", activebackground="white",
                             variable=self.selected, value=i)
            rb.place(x=40, y=y_pos)
            self.opts.append(rb)
            y_pos += 60

        # Next Button
        self.next_btn = Button(self.card, text="Next →", font=("Arial", 14, "bold"),
                               bg="#4472c4", fg="white",
                               activebackground="#3352a3",
                               width=12, command=self.next_question)
        self.next_btn.place(x=550, y=380)
        add_hover(self.next_btn, "#4472c4", "#3352a3")

        # Load first question
        self.load_question()

    # Load Question
    def load_question(self):
        q = self.questions[self.index]

        self.progress.config(text=f"Question {self.index + 1} of 10")
        self.question_text.config(text=q[1])

        options = [q[2], q[3], q[4], q[5]]
        for i in range(4):
            self.opts[i].config(text=options[i])

        self.selected.set(-1)

        # Reset Timer
        self.time_left = 30
        self.timer_label.config(text="⏳ 30s", fg="green")

        # Start Timer
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    # Timer Function
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"⏳ {self.time_left}s")

            # Warning color
            if self.time_left <= 5:
                self.timer_label.config(fg="red")

            self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.auto_next()

    # Auto move when time ends
    def auto_next(self):
        messagebox.showinfo("Time Up!", "Time is over! Moving to next question.")
        self.evaluate()
        self.next_or_finish()

    # Manual NEXT clicked
    def next_question(self):
        self.timer_running = False
        self.evaluate()
        self.next_or_finish()

    # Evaluate user answer
    def evaluate(self):
        chosen = self.selected.get()
        correct = self.questions[self.index][6]
        if chosen == correct:
            self.score += 1

    # Load next or finish quiz
    def next_or_finish(self):
        self.index += 1

        if self.index >= 10:
            self.finish_quiz()
        else:
            self.load_question()

    # Modern Final Result Screen
    def finish_quiz(self):
        self.timer_running = False
        self.card.destroy()

        # Update score in database if higher
        roll = self.user[2]
        prev_score = self.user[5]
        if self.score > prev_score:
            db.execute("UPDATE students SET score=%s WHERE rollno=%s",
                       (self.score, roll))

        result_card = Frame(self.root, bg="white", bd=0, highlightthickness=0)
        result_card.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # Title
        Label(result_card, text="🎉 Quiz Completed!", font=("Arial", 28, "bold"),
              bg="white", fg="#222").pack(pady=10)

        # Badge
        if self.score >= 8:
            badge = "🏅 Gold Medal"
            color = "#28a745"
            msg = "Excellent performance!"
        elif self.score >= 5:
            badge = "🥈 Silver Medal"
            color = "#007bff"
            msg = "Good job!"
        else:
            badge = "🥉 Bronze Medal"
            color = "#ff6600"
            msg = "Keep improving!"

        Label(result_card, text=badge, font=("Arial", 22, "bold"),
              bg="white", fg=color).pack(pady=10)

        # Score
        Label(result_card, text=f"Your Score: {self.score}/10",
              font=("Arial", 30, "bold"),
              bg="white", fg="#222").pack(pady=10)

        Label(result_card, text=msg, font=("Arial", 18),
              bg="white", fg="#666").pack(pady=5)

        def go_home():
            self.root.destroy()

        def retry():
            self.root.destroy()
            new = Tk()
            QuizWindow(new, self.user)

        btn_retry = Button(result_card, text="Try Again",
                           font=("Arial", 16, "bold"),
                           bg="#4472c4", fg="white",
                           width=12, activebackground="#3352a3",
                           command=retry)
        btn_retry.pack(pady=15)
        add_hover(btn_retry, "#4472c4", "#3352a3")

        btn_home = Button(result_card, text="Home",
                          font=("Arial", 16, "bold"),
                          bg="#6c757d", fg="white",
                          width=12, activebackground="#555",
                          command=go_home)
        btn_home.pack()
        add_hover(btn_home, "#6c757d", "#555")
