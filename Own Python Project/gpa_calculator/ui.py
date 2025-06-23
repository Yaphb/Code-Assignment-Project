import tkinter as tk
from tkinter import ttk, messagebox
from .calculator import Course, GPACalculator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GPACalculatorApp:
    """GUI for the GPA Calculator application."""
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Calculator")
        self.root.geometry("750x520")
        self.root.configure(bg="#23272e")  # Dark background
        self.calculator = GPACalculator()

        # --- Main Frames ---
        control_frame = tk.Frame(self.root, padx=18, pady=18, bg="#2c313a")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        display_frame = tk.Frame(self.root, padx=18, pady=18, bg="#23272e")
        display_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        label_font = ("Segoe UI", 11, "bold")
        entry_font = ("Segoe UI", 11)
        button_font = ("Segoe UI", 11, "bold")

        # --- Control Frame Widgets (Input) ---
        tk.Label(control_frame, text="Course Name:", font=label_font, fg="#f5f6fa", bg="#2c313a").grid(row=0, column=0, sticky='w', pady=4)
        self.course_name_entry = tk.Entry(control_frame, font=entry_font, bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa", relief=tk.FLAT)
        self.course_name_entry.grid(row=0, column=1, pady=4, padx=4)

        tk.Label(control_frame, text="Credits:", font=label_font, fg="#f5f6fa", bg="#2c313a").grid(row=1, column=0, sticky='w', pady=4)
        self.credits_entry = tk.Entry(control_frame, font=entry_font, bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa", relief=tk.FLAT)
        self.credits_entry.grid(row=1, column=1, pady=4, padx=4)

        tk.Label(control_frame, text="Grade:", font=label_font, fg="#f5f6fa", bg="#2c313a").grid(row=2, column=0, sticky='w', pady=4)
        self.grade_entry = ttk.Combobox(control_frame, values=list(self.calculator.GRADE_POINTS.keys()), font=entry_font, state="readonly")
        self.grade_entry.grid(row=2, column=1, pady=4, padx=4)
        self.grade_entry.configure(background="#23272e", foreground="#23272e")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="#23272e", background="#23272e", foreground="#23272e", selectbackground="#23272e", selectforeground="#f5f6fa")

        add_button = tk.Button(control_frame, text="Add Course", command=self.add_course,
                               font=button_font, bg="#4f8cff", fg="#fff", activebackground="#357ae8", activeforeground="#fff", relief=tk.FLAT, bd=0, height=2)
        add_button.grid(row=3, column=0, columnspan=2, pady=14, sticky='ew')

        clear_button = tk.Button(control_frame, text="Clear All Data", command=self.clear_data,
                                 font=button_font, bg="#ff4f4f", fg="#fff", activebackground="#e83535", activeforeground="#fff", relief=tk.FLAT, bd=0, height=2)
        clear_button.grid(row=4, column=0, columnspan=2, pady=6, sticky='ew')

        # --- Display Frame Widgets (Output) ---
        tree_style = ttk.Style()
        tree_style.theme_use('clam')
        tree_style.configure("Treeview",
                             background="#2c313a",
                             foreground="#f5f6fa",
                             rowheight=28,
                             fieldbackground="#2c313a",
                             font=("Segoe UI", 11))
        tree_style.configure("Treeview.Heading",
                             background="#23272e",
                             foreground="#4f8cff",
                             font=("Segoe UI", 11, "bold"))

        self.tree = ttk.Treeview(display_frame, columns=("Course", "Credits", "Grade"), show='headings', style="Treeview")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Credits", text="Credits")
        self.tree.heading("Grade", text="Grade")
        self.tree.pack(expand=True, fill=tk.BOTH, pady=(0, 10))

        self.gpa_label = tk.Label(display_frame, text="GPA: 0.00 | Total Credits: 0.0",
                                 font=("Segoe UI", 14, "bold"), fg="#4f8cff", bg="#23272e")
        self.gpa_label.pack(pady=8)

        self.refresh_course_list()
        self.update_gpa_display()

    def add_course(self):
        """Handles adding a new course from user input."""
        try:
            name = self.course_name_entry.get()
            credits = float(self.credits_entry.get())
            grade = self.grade_entry.get()

            course = Course(name, credits, grade)
            self.calculator.add_course(course)

            self.refresh_course_list()
            self.update_gpa_display()
            self.clear_input_fields()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("An Error Occurred", f"An unexpected error occurred: {e}")

    def refresh_course_list(self):
        """Clears and re-populates the course list view."""
        # Clear existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Add courses to the treeview
        for course in self.calculator.courses:
            self.tree.insert('', tk.END, values=(course.name, course.credits, course.grade))

    def update_gpa_display(self):
        """Recalculates and updates the GPA label."""
        gpa, total_credits = self.calculator.calculate_gpa()
        self.gpa_label.config(text=f"GPA: {gpa:.2f} | Total Credits: {total_credits:.1f}")
        self.update_chart()

    def clear_input_fields(self):
        """Clears the input fields after adding a course."""
        self.course_name_entry.delete(0, tk.END)
        self.credits_entry.delete(0, tk.END)
        self.grade_entry.set('')

    def clear_data(self):
        """Clears all course data after confirmation."""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all course data?"):
            self.calculator.clear_courses()
            self.refresh_course_list()
            self.update_gpa_display()

    def update_chart(self):
        """Creates or updates the grade distribution chart."""
        # Clear previous chart if it exists
        for widget in self.root.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        if not self.calculator.courses:
            return

        grades = [course.grade for course in self.calculator.courses]
        grade_counts = {grade: grades.count(grade) for grade in set(grades)}

        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.bar(grade_counts.keys(), grade_counts.values(), color='skyblue')
        ax.set_title('Grade Distribution')
        ax.set_ylabel('Number of Courses')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.gpa_label.master) # Embed in the same frame as the label
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.X, pady=5)