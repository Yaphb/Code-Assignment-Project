import json
import os

class Course:
    """Represents a single course with name, credit hours, and grade."""
    def __init__(self, name, credits, grade):
        # Basic input validation
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Course name must be a non-empty string.")
        if not isinstance(credits, (int, float)) or credits <= 0:
            raise ValueError("Credits must be a positive number.")
        if not isinstance(grade, str) or not grade.strip():
            raise ValueError("Grade must be a non-empty string.")

        self.name = name
        self.credits = float(credits)
        self.grade = grade.upper()

    def to_dict(self):
        """Converts the Course object to a dictionary."""
        return {"name": self.name, "credits": self.credits, "grade": self.grade}

class GPACalculator:
    """Manages courses and calculates GPA."""
    GRADE_POINTS = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.67,
        'B+': 3.33, 'B': 3.0, 'B-': 2.67,
        'C+': 2.33, 'C': 2.0, 'F': 0.0
    }

    def __init__(self, data_file='data/gpa_data.json'):
        self.courses = []
        self.data_file = data_file
        self._ensure_data_dir_exists()
        self.load_courses()

    def _ensure_data_dir_exists(self):
        """Ensures the data directory exists."""
        dir_name = os.path.dirname(self.data_file)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def add_course(self, course):
        """Adds a course to the list."""
        if not isinstance(course, Course):
            raise TypeError("Only Course objects can be added.")
        self.courses.append(course)
        self.save_courses()

    def calculate_gpa(self):
        """Calculates the GPA based on the list of courses."""
        total_points = 0
        total_credits = 0

        if not self.courses:
            return 0.0, 0.0

        for course in self.courses:
            if course.grade in self.GRADE_POINTS:
                total_points += self.GRADE_POINTS[course.grade] * course.credits
                total_credits += course.credits
        
        if total_credits == 0:
            return 0.0, 0.0

        gpa = total_points / total_credits
        return gpa, total_credits

    def save_courses(self):
        """Saves the list of courses to a JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                # Convert list of Course objects to list of dictionaries
                json.dump([course.to_dict() for course in self.courses], f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def load_courses(self):
        """Loads courses from a JSON file."""
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.courses = [Course(c['name'], c['credits'], c['grade']) for c in data]
        except (IOError, json.JSONDecodeError, KeyError) as e:
            # Handle file not found, corrupted file, or bad data
            print(f"Error loading data: {e}")
            self.courses = [] # Reset to empty list on error

    def clear_courses(self):
        """Clears all courses and deletes the data file."""
        self.courses = []
        if os.path.exists(self.data_file):
            os.remove(self.data_file)