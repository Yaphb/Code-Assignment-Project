import tkinter as tk
from tkinter import messagebox
from .timer import PomodoroTimer

class PomodoroTimerApp:
    """GUI for the Pomodoro Timer application with enhanced flow and customization."""
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x540")
        self.root.configure(bg="#23272e")

        self.timer_logic = PomodoroTimer()
        self.timer_id = None
        self.remaining_time = None  # Track remaining time for pause/resume

        # --- UI Elements ---
        self.title_label = tk.Label(
            root, text="Pomodoro Timer", font=("Segoe UI", 22, "bold"),
            fg="#4f8cff", bg="#23272e"
        )
        self.title_label.pack(pady=16)

        # --- Customization Controls ---
        control_frame = tk.Frame(root, bg="#23272e")
        control_frame.pack(pady=(0, 10))

        label_font = ("Segoe UI", 11, "bold")
        entry_font = ("Segoe UI", 11)

        tk.Label(control_frame, text="Work (min):", font=label_font, fg="#f5f6fa", bg="#23272e").grid(row=0, column=0, padx=4, pady=2)
        self.work_entry = tk.Entry(control_frame, width=4, font=entry_font, bg="#181a1b", fg="#f5f6fa", insertbackground="#f5f6fa", relief=tk.FLAT)
        self.work_entry.insert(0, "25")
        self.work_entry.grid(row=0, column=1, padx=4, pady=2)

        tk.Label(control_frame, text="Short Break (min):", font=label_font, fg="#f5f6fa", bg="#23272e").grid(row=0, column=2, padx=4, pady=2)
        self.short_break_entry = tk.Entry(control_frame, width=4, font=entry_font, bg="#181a1b", fg="#f5f6fa", insertbackground="#f5f6fa", relief=tk.FLAT)
        self.short_break_entry.insert(0, "5")
        self.short_break_entry.grid(row=0, column=3, padx=4, pady=2)

        tk.Label(control_frame, text="Long Break (min):", font=label_font, fg="#f5f6fa", bg="#23272e").grid(row=1, column=0, padx=4, pady=2)
        self.long_break_entry = tk.Entry(control_frame, width=4, font=entry_font, bg="#181a1b", fg="#f5f6fa", insertbackground="#f5f6fa", relief=tk.FLAT)
        self.long_break_entry.insert(0, "15")
        self.long_break_entry.grid(row=1, column=1, padx=4, pady=2)

        tk.Label(control_frame, text="Sessions:", font=label_font, fg="#f5f6fa", bg="#23272e").grid(row=1, column=2, padx=4, pady=2)
        self.sessions_entry = tk.Entry(control_frame, width=4, font=entry_font, bg="#181a1b", fg="#f5f6fa", insertbackground="#f5f6fa", relief=tk.FLAT)
        self.sessions_entry.insert(0, "4")
        self.sessions_entry.grid(row=1, column=3, padx=4, pady=2)

        # --- Timer Display ---
        self.canvas = tk.Canvas(root, width=240, height=240, bg="#181a1b", highlightthickness=0)
        self.timer_text = self.canvas.create_text(120, 130, text="25:00", fill="#f5f6fa", font=("Segoe UI", 44, "bold"))
        self.canvas.pack(pady=10)

        # --- Buttons ---
        button_style = {
            "font": ("Segoe UI", 12, "bold"),
            "bg": "#4f8cff",
            "fg": "#fff",
            "activebackground": "#357ae8",
            "activeforeground": "#fff",
            "relief": tk.FLAT,
            "bd": 0,
            "height": 2,
            "width": 10,
            "cursor": "hand2"
        }

        btn_frame = tk.Frame(root, bg="#23272e")
        btn_frame.pack(pady=6)

        self.start_button = tk.Button(btn_frame, text="Start", command=self.start_timer, **button_style)
        self.start_button.grid(row=0, column=0, padx=8)

        self.stop_button = tk.Button(btn_frame, text="Stop", command=self.stop_timer, **button_style)
        self.stop_button.configure(bg="#ffb84f", activebackground="#e8a835")
        self.stop_button.grid(row=0, column=1, padx=8)

        self.reset_button = tk.Button(btn_frame, text="Reset", command=self.reset_timer, **button_style)
        self.reset_button.configure(bg="#ff4f4f", activebackground="#e83535")
        self.reset_button.grid(row=0, column=2, padx=8)

        # --- Progress and Status ---
        self.session_label = tk.Label(root, text="Session: 0/4", fg="#b0b8c1", bg="#23272e", font=("Segoe UI", 12, "bold"))
        self.session_label.pack(pady=(10, 0))

        self.check_marks = tk.Label(root, text="", fg="#4f8cff", bg="#23272e", font=("Segoe UI", 18, "bold"))
        self.check_marks.pack(pady=8)

        self.is_running = False
        self.current_session = 0
        self.total_sessions = 4
        self.session_type = "Work"
        self.session_times = {"Work": 25*60, "Short Break": 5*60, "Long Break": 15*60}

        # Store all entry widgets for easy enable/disable
        self.entries = [
            self.work_entry,
            self.short_break_entry,
            self.long_break_entry,
            self.sessions_entry
        ]

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def apply_settings(self):
        """Apply user settings for timer durations and sessions."""
        try:
            work = int(self.work_entry.get())
            short_break = int(self.short_break_entry.get())
            long_break = int(self.long_break_entry.get())
            sessions = int(self.sessions_entry.get())
            if work <= 0 or short_break <= 0 or long_break <= 0 or sessions <= 0:
                raise ValueError
            self.session_times = {
                "Work": work * 60,
                "Short Break": short_break * 60,
                "Long Break": long_break * 60
            }
            self.total_sessions = sessions
        except Exception:
            messagebox.showerror("Input Error", "Please enter valid positive integers for all timer settings.")

    def set_entries_state(self, state):
        """Enable or disable the time/session entry widgets."""
        for entry in self.entries:
            entry.config(state=state)

    def start_timer(self):
        """Starts or resumes the countdown timer."""
        if self.is_running:
            return
        self.apply_settings()
        self.is_running = True
        self.set_entries_state("disabled")  # Disable editing while running
        if self.current_session == 0:
            self.current_session = 1
            self.session_type = "Work"
            self.remaining_time = None  # New session, reset remaining_time
        self.run_session(resume=True)

    def run_session(self, resume=False):
        """Run the current session."""
        if self.current_session > self.total_sessions:
            self.canvas.itemconfig(self.timer_text, text="Done!")
            self.title_label.config(text="Pomodoro Complete!", fg="#4f8cff")
            self.is_running = False
            self.remaining_time = None
            return
        if self.session_type == "Work":
            self.title_label.config(text="Work", fg="#e7305b")
            duration = self.session_times["Work"]
        elif self.session_type == "Short Break":
            self.title_label.config(text="Short Break", fg="#9bdeac")
            duration = self.session_times["Short Break"]
        else:
            self.title_label.config(text="Long Break", fg="#4f8cff")
            duration = self.session_times["Long Break"]

        # Use remaining_time if resuming from pause
        if resume and self.remaining_time is not None:
            self.countdown(self.remaining_time)
        else:
            self.remaining_time = duration
            self.countdown(duration)

    def stop_timer(self):
        """Stops/pauses the timer."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.is_running = False
        # Allow editing again when paused
        self.set_entries_state("normal")

    def reset_timer(self):
        """Resets the timer to its initial state."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.is_running = False
        self.current_session = 0
        self.session_type = "Work"
        self.session_label.config(text=f"Session: 0/{self.total_sessions}")
        self.title_label.config(text="Pomodoro Timer", fg="#4f8cff")
        self.canvas.itemconfig(self.timer_text, text=f"{int(self.work_entry.get()):02d}:00")
        self.check_marks.config(text="")
        self.remaining_time = None
        self.set_entries_state("normal")  # Allow editing after reset

    def countdown(self, count):
        """The recursive countdown mechanism."""
        self.remaining_time = count  # Always update remaining_time
        mins = count // 60
        secs = count % 60
        self.canvas.itemconfig(self.timer_text, text=f"{mins:02d}:{secs:02d}")
        if count > 0 and self.is_running:
            self.timer_id = self.root.after(1000, self.countdown, count - 1)
        elif self.is_running:
            self.remaining_time = None
            self.after_session()

    def after_session(self):
        """Handle logic after a session ends."""
        if self.session_type == "Work":
            marks = "✔" * self.current_session
            self.check_marks.config(text=marks)
            if self.current_session % self.total_sessions == 0:
                self.session_type = "Long Break"
            else:
                self.session_type = "Short Break"
        else:
            if self.session_type == "Long Break":
                self.current_session = 0
                self.session_type = "Work"
                self.session_label.config(text=f"Session: 0/{self.total_sessions}")
                self.title_label.config(text="Pomodoro Complete!", fg="#4f8cff")
                self.is_running = False
                return
            else:
                self.current_session += 1
                self.session_type = "Work"
        self.session_label.config(text=f"Session: {self.current_session}/{self.total_sessions}")
        self.run_session()

    def on_closing(self):
        """Handle the window closing event to stop the timer."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.root.destroy()