import tkinter as tk
from tkinter import messagebox

from gpa_calculator.ui import GPACalculatorApp
from pomodoro_timer.ui import PomodoroTimerApp
from reminder_app.ui import ReminderApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TAR UMT Student Assistant")
        self.root.geometry("480x560")
        self.root.configure(bg="#181a1b")

        # Gradient accent bar (simulate with two frames)
        accent_top = tk.Frame(self.root, bg="#4f8cff", height=10)
        accent_top.pack(fill=tk.X, side=tk.TOP)
        accent_grad = tk.Frame(self.root, bg="#8f94fb", height=6)
        accent_grad.pack(fill=tk.X, side=tk.TOP)

        # Shadow effect for card
        shadow = tk.Frame(self.root, bg="#101217")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=390, height=600)

        # Main card frame (rounded effect with padding)
        card_outer = tk.Frame(self.root, bg="#23272e", bd=0, highlightthickness=0)
        card_outer.place(relx=0.5, rely=0.5, anchor="center", width=380, height=590)

        # Logo/Title area
        logo_frame = tk.Frame(card_outer, bg="#23272e")
        logo_frame.pack(pady=(38, 0))
        logo_label = tk.Label(
            logo_frame,
            text="🎓",
            font=("Segoe UI Emoji", 54),
            bg="#23272e"
        )
        logo_label.pack(side=tk.LEFT, padx=(0, 18))
        title_label = tk.Label(
            logo_frame,
            text="TAR UMT\nStudent Assistant",
            font=("Segoe UI", 18, "bold"),
            fg="#f5f6fa",
            bg="#23272e",
            justify="left"
        )
        title_label.pack(side=tk.LEFT)

        # Subtitle
        subtitle = tk.Label(
            card_outer,
            text="Your all-in-one study companion",
            font=("Segoe UI", 13, "italic"),
            fg="#b0b8c1",
            bg="#23272e"
        )
        subtitle.pack(pady=(10, 28))

        # Button style options
        button_opts = {
            "font": ("Segoe UI", 14, "bold"),
            "bg": "#23272e",
            "fg": "#f5f6fa",
            "activebackground": "#4f8cff",
            "activeforeground": "#fff",
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
            "height": 2,
            "width": 26
        }

        # Animated hover effect
        def on_enter(e):
            e.widget['bg'] = "#4f8cff"
            e.widget['fg'] = "#fff"
            e.widget['font'] = ("Segoe UI", 15, "bold")
        def on_leave(e):
            e.widget['bg'] = "#23272e"
            e.widget['fg'] = "#f5f6fa"
            e.widget['font'] = ("Segoe UI", 14, "bold")
        def on_exit_enter(e):
            e.widget['bg'] = "#ff4f4f"
            e.widget['fg'] = "#fff"
            e.widget['font'] = ("Segoe UI", 15, "bold")
        def on_exit_leave(e):
            e.widget['bg'] = "#23272e"
            e.widget['fg'] = "#f5f6fa"
            e.widget['font'] = ("Segoe UI", 14, "bold")

        # Buttons for each application
        gpa_button = tk.Button(
            card_outer, text="GPA Calculator",
            command=self.open_gpa_calculator, **button_opts
        )
        gpa_button.pack(pady=(16, 12))
        gpa_button.bind("<Enter>", on_enter)
        gpa_button.bind("<Leave>", on_leave)

        pomodoro_button = tk.Button(
            card_outer, text="Study Pomodoro Timer",
            command=self.open_pomodoro_timer, **button_opts
        )
        pomodoro_button.pack(pady=12)
        pomodoro_button.bind("<Enter>", on_enter)
        pomodoro_button.bind("<Leave>", on_leave)

        reminder_button = tk.Button(
            card_outer, text="Simple Reminder App",
            command=self.open_reminder_app, **button_opts
        )
        reminder_button.pack(pady=12)
        reminder_button.bind("<Enter>", on_enter)
        reminder_button.bind("<Leave>", on_leave)

        # Exit button with red color on hover
        exit_button = tk.Button(
            card_outer, text="Exit",
            command=self.root.quit,
            bg="#23272e",
            fg="#f5f6fa",
            font=("Segoe UI", 14, "bold"),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            height=2,
            width=26
        )
        exit_button.pack(pady=(18, 0))
        exit_button.bind("<Enter>", on_exit_enter)
        exit_button.bind("<Leave>", on_exit_leave)

        # Footer
        footer = tk.Label(
            card_outer,
            text="© 2025 TAR UMT",
            font=("Segoe UI", 10),
            fg="#6c7a89",
            bg="#23272e"
        )
        footer.pack(side=tk.BOTTOM, pady=(32, 12))

    def open_gpa_calculator(self):
        self.open_new_window("GPA Calculator", GPACalculatorApp)

    def open_pomodoro_timer(self):
        self.open_new_window("Study Pomodoro Timer", PomodoroTimerApp)

    def open_reminder_app(self):
        self.open_new_window("Simple Reminder App", ReminderApp)

    def open_new_window(self, title, app_class):
        try:
            new_window = tk.Toplevel(self.root)
            new_window.title(title)
            new_window.configure(bg="#181a1b")
            app = app_class(new_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open application: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()