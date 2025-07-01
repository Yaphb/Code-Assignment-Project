# Import necessary modules from Python's standard library.
import tkinter as tk
from tkinter import messagebox # Import messagebox for displaying alerts and notifications
import json # Import json for handling task data storage, a common format for storing structured data
import os # Import os for file path handling, checking existence, and directory management

# Define constants for timer settings and styling. This makes it easy to
# change the look and feel or the timer durations later.
POMODORO_MINS = 25
SHORT_BREAK_MINS = 5
LONG_BREAK_MINS = 15

# Color scheme inspired by popular Pomodoro websites for a modern look.
COLOR_BACKGROUND = "#1E1E1E"
COLOR_FOREGROUND = "#FFFFFF"
COLOR_ACCENT = "#FF6347"  # A shade of tomato/coral
COLOR_BUTTON = "#333333"
COLOR_BUTTON_ACTIVE = "#555555"
COLOR_START_ACTIVE = "#FF4500"  # A shade of orange-red for the start button

# File name for storing tasks.
TASKS_FILE = "pomodoro_tasks.json"


# --- Main Application Class ---
# This class encapsulates the entire Pomodoro Timer application.
# It inherits from tk.Tk, demonstrating the principle of Inheritance,
# a key concept in Object-Oriented Programming (OOP).
class PomodoroTimer(tk.Tk):
    """
    The main class for the Pomodoro Timer application.

    This class sets up the GUI, manages the timer's state and logic,
    and handles task management functionalities. Encapsulation is achieved
    by keeping all widgets and state variables within this class.
    """

    def __init__(self): # self is the instance of the class, which is a common practice in OOP.
        """
        Initializes the main application window and its components.
        """
        super().__init__()  # Call the constructor of the parent class (tk.Tk)

        # --- State Variables ---
        # These variables track the current state of the timer.
        self.current_mode = "Pomodoro"  # Can be 'Pomodoro', 'Short Break', or 'Long Break', defaulting to Pomodoro.
        self.time_left = POMODORO_MINS * 60
        self.is_running = False
        self.timer_id = None  # To store the ID of the 'after' job for the timer loop

        # --- Window Configuration ---
        self.title("Study Pomodoro Timer")
        self.geometry("400x600")  # Set a default size for the window
        self.config(bg=COLOR_BACKGROUND, padx=20, pady=20)

        # --- GUI Widgets ---
        # All widgets are created by calling helper methods for better organization.
        self.create_mode_buttons()
        self.create_timer_display()
        self.create_control_buttons()
        self.create_task_manager()

        # Load tasks from the file when the application starts.
        self.load_tasks()

    # --- GUI Creation Methods ---
    
    # These methods create the various components of the GUI.
    def create_mode_buttons(self):
        """Creates the buttons for switching between timer modes."""
        
        # tk.Frame is used to group the mode buttons together.
        mode_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        mode_frame.pack(pady=10)

        # Using a loop to create buttons demonstrates efficient code structure.
        modes = [("Pomodoro", POMODORO_MINS), ("Short Break", SHORT_BREAK_MINS), ("Long Break", LONG_BREAK_MINS)]
        for mode, _ in modes:
            # Create a button for each mode.
            # The lambda function captures the current mode to pass it to the switch_mode method.
            # tk.Button is used to create a button widget.
            btn = tk.Button(mode_frame, text=mode, bg=COLOR_BUTTON, fg=COLOR_FOREGROUND,
                            activebackground=COLOR_ACCENT, relief="flat", borderwidth=0, font=("Comic Sans MS", 12),
                            command=lambda m=mode: self.switch_mode(m))
            btn.pack(side="left", padx=5)

    def create_timer_display(self):
        """Creates the label that shows the time countdown."""
        
        # tk.Label is used to display the timer.
        self.timer_label = tk.Label(self, text=self.format_time(self.time_left),
                                    font=("Comic Sans MS", 60, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_FOREGROUND)
        self.timer_label.pack(pady=20)

    def create_control_buttons(self):
        """Creates the Start, Pause, and Reset buttons."""
        control_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        control_frame.pack(pady=10)

        self.start_button = tk.Button(control_frame, text="Start", bg=COLOR_ACCENT, fg=COLOR_FOREGROUND,
                                      activebackground=COLOR_START_ACTIVE, relief="flat", borderwidth=0, font=("Comic Sans MS", 16, "bold"),
                                      command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        self.pause_button = tk.Button(control_frame, text="Pause", bg=COLOR_BUTTON, fg=COLOR_FOREGROUND,
                                      activebackground=COLOR_BUTTON_ACTIVE, relief="flat", borderwidth=0, font=("Comic Sans MS", 16),
                                      command=self.pause_timer)
        self.pause_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(control_frame, text="Reset", bg=COLOR_BUTTON, fg=COLOR_FOREGROUND,
                                      activebackground=COLOR_BUTTON_ACTIVE, relief="flat", borderwidth=0, font=("Comic Sans MS", 16),
                                      command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10)

    def create_task_manager(self):
        """Creates the GUI components for managing tasks."""
        task_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        task_frame.pack(pady=20, fill="x")

        task_label = tk.Label(task_frame, text="Tasks", font=("Comic Sans MS", 14, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_FOREGROUND)
        task_label.pack()

        # Input field for new tasks
        self.task_entry = tk.Entry(task_frame, bg=COLOR_BUTTON, fg=COLOR_FOREGROUND, insertbackground=COLOR_FOREGROUND,
                                   relief="flat", font=("Comic Sans MS", 12))
        self.task_entry.pack(fill="x", pady=5)
        self.task_entry.insert(0, "Enter task here...")

        def on_entry_focus_in(event):
            if self.task_entry.get() == "Enter task here...":
                self.task_entry.delete(0, tk.END)
                self.task_entry.config(fg=COLOR_FOREGROUND)

        def on_entry_focus_out(event):
            if not self.task_entry.get():
                self.task_entry.insert(0, "Enter task here...")
                self.task_entry.config(fg=COLOR_FOREGROUND)

        self.task_entry.bind("<FocusIn>", on_entry_focus_in)
        self.task_entry.bind("<FocusOut>", on_entry_focus_out)
        self.task_entry.bind("<Return>", self.add_task) # Allow adding task by pressing Enter

        # Frame for task buttons
        task_button_frame = tk.Frame(task_frame, bg=COLOR_BACKGROUND)
        task_button_frame.pack(pady=5)
        
        add_task_btn = tk.Button(task_button_frame, text="Add Task", bg=COLOR_BUTTON, fg=COLOR_FOREGROUND,
                                 command=self.add_task, relief="flat", font=("Comic Sans MS", 10))
        add_task_btn.pack(side="left", padx=5, pady=5)
        
        delete_task_btn = tk.Button(task_button_frame, text="Delete Selected", bg=COLOR_BUTTON, fg=COLOR_FOREGROUND,
                                    command=self.delete_task, relief="flat", font=("Comic Sans MS", 10))
        delete_task_btn.pack(side="left", padx=5, pady=5)

        # tk.Listbox is used to display the list of tasks.
        self.task_listbox = tk.Listbox(task_frame, bg=COLOR_BUTTON, fg=COLOR_FOREGROUND, selectbackground=COLOR_ACCENT,
                                       relief="flat", borderwidth=0, font=("Comic Sans MS", 12), height=8)
        self.task_listbox.pack(fill="x", expand=True)

    # --- Timer Logic Methods ---

    # These methods control the timer's behavior and state, demonstrating control structures like loops and conditionals.
    def start_timer(self):
        """Starts or resumes the timer if it's not already running."""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(text="Start", state="disabled")
            self.pause_button.config(state="normal", text="Pause")
            self.countdown()

    def pause_timer(self):
        """Pauses the timer if running."""
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self.start_button.config(text="Resume", state="normal")
            self.pause_button.config(state="disabled")

    def reset_timer(self):
        """Resets the timer to the current mode's default time."""
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.is_running = False
        self.switch_mode(self.current_mode)
        self.start_button.config(text="Start", state="normal")
        self.pause_button.config(text="Pause", state="disabled")


    def countdown(self):
        """
        The main loop for the timer. Updates the display every second.
        This method calls itself using 'self.after', which simulates a loop.
        """
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
            self.timer_id = self.after(1000, self.countdown)  # Schedule next call
        elif self.time_left <= 0:
            self.is_running = False
            self.handle_timer_completion()

    def switch_mode(self, mode):
        """
        Switches the timer to a new mode (e.g., 'Pomodoro', 'Short Break').
        """
        self.current_mode = mode
        if mode == "Pomodoro":
            self.time_left = POMODORO_MINS * 60
        elif mode == "Short Break":
            self.time_left = SHORT_BREAK_MINS * 60
        elif mode == "Long Break":
            self.time_left = LONG_BREAK_MINS * 60
        
        # Always reset the visual state when switching modes
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.is_running = False
        self.update_timer_display()
        self.start_button.config(text="Start", state="normal")
        self.pause_button.config(text="Pause", state="disabled")

    def handle_timer_completion(self):
        """
        Handles what happens when the timer reaches zero.
        It shows a notification and suggests the next mode.
        """
        self.bell()  # Play a system sound
        messagebox.showinfo("Timer Finished!", f"{self.current_mode} session is complete!")
        
        # Suggest the next logical mode
        if self.current_mode == "Pomodoro":
            self.switch_mode("Short Break")
        else:
            self.switch_mode("Pomodoro")
        self.reset_timer() # Reset to the new mode's start time

    # --- Utility and Task Management Methods ---

    def format_time(self, seconds):
        """
        Formats the given time in seconds into a MM:SS string.
        This demonstrates string processing.
        """
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def update_timer_display(self):
        """Updates the timer label with the current time."""
        self.timer_label.config(text=self.format_time(self.time_left))

    def add_task(self, event=None):
        """
        Adds a new task from the entry field to the task list.
        'event=None' allows this method to be called by a button click or an Enter key press.
        """
        task = self.task_entry.get().strip() # Stripping whitespace ensures no empty tasks are added.
        # Using a collection (list) to store tasks.
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()

    def delete_task(self):
        """Deletes the currently selected task from the listbox."""
        # Exception handling for when no task is selected.
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_index)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete.")

    def save_tasks(self):
        """Save tasks to file with a simple while loop and exception handling."""
        attempts = 0
        while attempts < 3:
            try:
                # Open the file in write mode to save tasks.
                with open(TASKS_FILE, 'w') as f:
                    # Convert the listbox items to a list and write to the file.
                    # json.dump is used to arrange the list of tasks into JSON format.
                    json.dump(list(self.task_listbox.get(0, tk.END)), f) 
                break
            # If an exception occurs, increment the attempts counter.
            except Exception:
                attempts += 1

    def load_tasks(self):
        """Load tasks from file with a simple while loop and exception handling."""
        attempts = 0
        while attempts < 3:
            try:
                # Check if the tasks file exists before trying to read it.
                if os.path.exists(TASKS_FILE):
                    # Open the file in read mode to load tasks.
                    with open(TASKS_FILE, 'r') as f:
                        # Load tasks from the JSON file into the listbox.
                        for task in json.load(f):
                            # Ensure only valid strings are added to the listbox.
                            if isinstance(task, str) and task.strip():
                                self.task_listbox.insert(tk.END, task)
                break
            except Exception:
                attempts += 1


# --- Main Execution Block ---
if __name__ == "__main__":
    """
    This block ensures that the code inside it only runs when the script is
    executed directly (not when imported as a module).
    """
    app = PomodoroTimer() # Creates an instance of the PomodoroTimer class, initializing the GUI and its components.
    app.mainloop()  # Starts the tkinter event loop, making the GUI interactive.
