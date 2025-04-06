import csv

class Student:
    def __init__(self, student_id, name, major, email, password):
        self.student_id = student_id
        self.name = name
        self.major = major
        self.email = email
        self.password = password
        self.registered_courses = set()

class Course:
    def __init__(self, course_code, name, instructor, day, time, credit_hours, max_students=30):
        self.course_code = course_code
        self.name = name
        self.instructor = instructor
        self.day = day
        self.time = time
        self.credit_hours = credit_hours
        self.max_students = max_students
        self.enrolled_students = set()

class EnrollmentSystem:
    def __init__(self):
        self.students = {}   # student_id -> Student
        self.courses = {}    # course_code -> Course
        self.departments = {
            "Computer Science": [],
            "English": []
        }
        self.load_data()

    def load_data(self):
        # Load students
        try:
            with open("students.csv", mode="r", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    student = Student(
                        student_id=row["student_id"],
                        name=row["name"],
                        major=row["major"],
                        email=row["email"],
                        password=row["password"]
                    )
                    student.registered_courses = set(row["registered_courses"].split(";")) if row["registered_courses"] else set()
                    self.students[student.student_id] = student
        except FileNotFoundError:
            print("students.csv not found.")

        # Load courses
        try:
            with open("courses.csv", mode="r", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    course = Course(
                        course_code=row["course_code"],
                        name=row["name"],
                        instructor=row["instructor"],
                        day=row["day"],
                        time=row["time"],
                        credit_hours=int(row["credit_hours"]),
                        max_students=int(row["max_students"])
                    )
                    course.enrolled_students = set(row["enrolled_students"].split(";")) if row["enrolled_students"] else set()
                    self.courses[course.course_code] = course

                    # Assign courses to departments (based on prefix for now)
                    if course.course_code.startswith("CS"):
                        self.departments["Computer Science"].append(course)
                    elif course.course_code.startswith("EN"):
                        self.departments["English"].append(course)
        except FileNotFoundError:
            print("courses.csv not found.")

    def login(self):
        print("\n--- Student Login ---")
        attempts = 3
        while attempts > 0:
            student_id = input("Enter Student ID (e.g., Z0123): ").strip()
            password = input("Enter Password: ").strip()

            student = self.students.get(student_id)
            if student and student.password == password:
                print(f"\n Welcome, {student.name}!")
                return student
            else:
                attempts -= 1
                print(f"Invalid credentials. Attempts left: {attempts}")

        print("Too many failed attempts. Exiting.")
        return None

    def view_schedule(self, student: Student):
        print("\n--- Your Schedule ---")
        total_credits = 0
        if not student.registered_courses:
            print("You have not registered for any courses yet.")
        else:
            for code in student.registered_courses:
                course = self.courses[code]
                print(f"{course.course_code} | {course.name} | {course.instructor} | {course.day} {course.time} | {course.credit_hours} credits")
                total_credits += course.credit_hours
        print(f"\nTotal Credits: {total_credits}/10")

    def main_menu(self):
        student = self.login()
        if not student:
            return

        while True:
            print("\n--- Main Menu ---")
            print("1. View/Register for Courses")
            print("2. View My Schedule")
            print("3. Logout")

            choice = input("Choose an option (1-3): ").strip()

            if choice == "1":
                self.select_courses(student)
            elif choice == "2":
                self.view_schedule(student)
            elif choice == "3":
                print("👋 Logged out.")
                break
            else:
                print("Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    system = EnrollmentSystem()
    system.main_menu()