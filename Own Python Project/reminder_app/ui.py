import tkinter as tk
from tkinter import messagebox, simpledialog
from .reminder import Reminder, ReminderManager
from datetime import datetime

class ReminderApp:
    """GUI for the Simple Reminder App."""
    def __init__(self, root):
        self.root = root
        self.root.geometry("520x420")
        self.root.configure(bg="#23272e")
        self.manager = ReminderManager()

        # --- Frames ---
        input_frame = tk.Frame(root, padx=12, pady=12, bg="#23272e")
        input_frame.pack(fill=tk.X)

        list_frame = tk.Frame(root, padx=12, pady=12, bg="#23272e")
        list_frame.pack(expand=True, fill=tk.BOTH)

        label_font = ("Segoe UI", 11, "bold")
        entry_font = ("Segoe UI", 11)
        button_font = ("Segoe UI", 11, "bold")

        # --- Input Widgets ---
        tk.Label(input_frame, text="Message:", font=label_font, fg="#f5f6fa", bg="#23272e").pack(side=tk.LEFT)
        self.message_entry = tk.Entry(input_frame, width=30, font=entry_font, bg="#181a1b", fg="#f5f6fa", insertbackground="#f5f6fa", relief=tk.FLAT)
        self.message_entry.pack(side=tk.LEFT, padx=8)

        add_button = tk.Button(input_frame, text="Add Reminder", command=self.add_reminder,
                               font=button_font, bg="#4f8cff", fg="#fff", activebackground="#357ae8", activeforeground="#fff", relief=tk.FLAT, bd=0, height=1)
        add_button.pack(side=tk.LEFT, padx=8)

        # --- List Widgets ---
        self.reminder_listbox = tk.Listbox(list_frame, font=entry_font, bg="#181a1b", fg="#f5f6fa", selectbackground="#4f8cff", selectforeground="#fff", relief=tk.FLAT)
        self.reminder_listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.reminder_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.reminder_listbox.config(yscrollcommand=scrollbar.set)

        delete_button = tk.Button(root, text="Delete Selected Reminder", command=self.delete_reminder,
                                  font=button_font, bg="#ff4f4f", fg="#fff", activebackground="#e83535", activeforeground="#fff", relief=tk.FLAT, bd=0, height=2)
        delete_button.pack(pady=12)

        self.refresh_list()
        self.check_reminders()

    def add_reminder(self):
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Input Error", "Message cannot be empty.")
            return

        # Ask for date and time using a simple dialog
        time_str = simpledialog.askstring("Reminder Time", 
                                          "Enter time (YYYY-MM-DD HH:MM):",
                                          parent=self.root)
        if not time_str:
            return

        try:
            reminder = Reminder(message, time_str)
            self.manager.add_reminder(reminder)
            self.refresh_list()
            self.message_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def delete_reminder(self):
        selected_indices = self.reminder_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a reminder to delete.")
            return

        selected_reminder_obj = self.manager.reminders[selected_indices[0]]
        self.manager.delete_reminder(selected_reminder_obj)
        self.refresh_list()

    def refresh_list(self):
        self.reminder_listbox.delete(0, tk.END)
        for reminder in self.manager.reminders:
            self.reminder_listbox.insert(tk.END, f"{reminder.time.strftime('%Y-%m-%d %H:%M')} - {reminder.message}")

    def check_reminders(self):
        """Periodically check for due reminders."""
        now = datetime.now()
        due_reminders = [r for r in self.manager.reminders if r.time <= now]

        for r in due_reminders:
            messagebox.showinfo("Reminder!", f"It's time for:\n\n{r.message}")
            self.manager.delete_reminder(r) # Remove after showing
        
        if due_reminders:
            self.refresh_list()

        # Check again in 30 seconds
        self.root.after(30000, self.check_reminders)