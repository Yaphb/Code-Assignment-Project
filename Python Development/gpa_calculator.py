# GPA Calculator Program (Custom Grade Points)

GRADE_POINTS = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.67,
    'B+': 3.33, 'B': 3.0, 'B-': 2.67,
    'C+': 2.33, 'C': 2.0, 'F': 0.0
}

def calculate_gpa():
    total_credits = 0
    total_points = 0

    print("GPA Calculator (type 'done' when finished)\n")
    
    while True:
        course = input("Enter course name (or 'done' to finish): ")
        if course.lower() == 'done':
            break
        try:
            credits = float(input(f"Enter credit hours for {course}: "))
            grade = input(f"Enter grade for {course} (e.g., A, B+, C-): ").strip().upper()

            if grade not in GRADE_POINTS:
                print("Invalid grade entered. Please try again.\n")
                continue

            total_credits += credits
            total_points += GRADE_POINTS[grade] * credits

        except ValueError:
            print("Invalid input. Please enter numeric values for credit hours.\n")

    if total_credits == 0:
        print("No valid courses entered.")
    else:
        gpa = total_points / total_credits
        print(f"\nYour GPA is: {gpa:.2f}")

# Run the GPA calculator
calculate_gpa()

