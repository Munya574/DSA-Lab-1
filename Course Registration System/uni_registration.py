import csv
import os
from datetime import datetime, time

class Student:
    def __init__(self, student_id, name, password, email, major):
        self.student_id = student_id
        self.name = name
        self.password = password
        self.email = email
        self.major = major
        self.registered_courses = set()
    
    def get_total_credits(self, courses):
        """Calculate total credits a student is enrolled in"""
        total = 0
        for course_id in self.registered_courses:
            if course_id in courses:
                total += courses[course_id].credits
        return total
    
    def has_schedule_conflict(self, new_course, courses):
        """Check if a new course conflicts with existing schedule"""
        for enrolled_course_id in self.registered_courses:
            enrolled_course = courses.get(enrolled_course_id)
            if enrolled_course and new_course.has_time_conflict(enrolled_course):
                return True
        return False
    
    def to_csv_row(self):
        """Convert student data to a CSV row"""
        return [self.student_id, self.name, self.password, self.email, self.major, ','.join(self.registered_courses)]


class Course:
    def __init__(self, course_id, name, department, instructor, max_students=5, credits=2, days=None, start_time=None, end_time=None):
        self.course_id = course_id
        self.name = name
        self.department = department
        self.instructor = instructor
        self.enrolled_students = set()
        self.max_students = max_students
        self.credits = credits
        self.days = days or []  # List of days (e.g., ['Mon', 'Wed'])
        self.start_time = start_time  # datetime.time object
        self.end_time = end_time      # datetime.time object
    
    def is_full(self):
        """Check if course has reached maximum capacity"""
        return len(self.enrolled_students) >= self.max_students
    
    def has_time_conflict(self, other_course):
        """Check if this course has a time conflict with another course"""
        # Check if any days overlap
        days_overlap = any(day in other_course.days for day in self.days)
        if not days_overlap:
            return False
            
        # Check if times overlap on the common days
        if self.start_time <= other_course.end_time and self.end_time >= other_course.start_time:
            return True
            
        return False
    
    def to_csv_row(self):
        """Convert course data to CSV row format"""
        start_time_str = self.start_time.strftime('%H:%M') if self.start_time else ""
        end_time_str = self.end_time.strftime('%H:%M') if self.end_time else ""
        return [
            self.course_id, 
            self.name, 
            self.department,
            self.instructor, 
            str(self.max_students), 
            str(self.credits),
            ",".join(self.days),
            start_time_str,
            end_time_str,
            ",".join(self.enrolled_students)
        ]
    
    def __str__(self):
        """String representation of the course for display"""
        days_str = ", ".join(self.days)
        time_str = f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}" if self.start_time and self.end_time else "N/A"
        return f"{self.course_id}: {self.name} ({self.department})\n" \
               f"  Instructor: {self.instructor}\n" \
               f"  Schedule: {days_str} {time_str}\n" \
               f"  Credits: {self.credits}\n" \
               f"  Enrollment: {len(self.enrolled_students)}/{self.max_students}"


class EnrollmentSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}
        self.max_credits = 10  # Maximum credits a student can take
        self.data_dir = "data"
        self.ensure_data_directory()
        self.load_data()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_data(self):
        """Load student and course data from CSV files"""
        self._load_students()
        self._load_courses()
        self._load_enrollments()
    
    def _load_students(self):
        """Load student data from CSV file"""
        students_file = os.path.join(self.data_dir, "students.csv")
        if not os.path.exists(students_file):
            return
            
        with open(students_file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    student_id, name, password = row[0], row[1], row[2]
                    self.students[student_id] = Student(student_id, name, password)
    
    def _load_courses(self):
        """Load course data from CSV file"""
        courses_file = os.path.join(self.data_dir, "courses.csv")
        if not os.path.exists(courses_file):
            self._create_sample_courses()
            return
            
        with open(courses_file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 9:
                    course_id = row[0]
                    name = row[1]
                    department = row[2]
                    instructor = row[3]
                    max_students = int(row[4]) if row[4] else 30
                    credits = int(row[5]) if row[5] else 3
                    
                    days = row[6].split(',') if row[6] else []
                    
                    start_time = None
                    if row[7]:
                        h, m = map(int, row[7].split(':'))
                        start_time = time(h, m)
                    
                    end_time = None
                    if row[8]:
                        h, m = map(int, row[8].split(':'))
                        end_time = time(h, m)
                    
                    course = Course(
                        course_id, 
                        name, 
                        department,
                        instructor, 
                        max_students, 
                        credits,
                        days, 
                        start_time, 
                        end_time
                    )
                    
                    if len(row) >= 10 and row[9]:
                        course.enrolled_students = set(row[9].split(','))
                    
                    self.courses[course_id] = course
    
    def preload_students(self):
        """Preload sample students data"""
        students_data = [
            ("Z01234", "James Phiri", "password123", "jphiri@zed.edu", "Computer Science"),
            ("Z05678", "Dingiswayo Mukandawire", "password456", "dmukandawire@zed.edu", "Mathematics"),
            ("Z09123", "Nasilele Nakazwe", "password789", "nnakazwe@zed.edu", "Physics"),
        ]

        for student_id, name, password, email, major in students_data:
            self.students[student_id] = Student(student_id, name, password, email, major)
    
        # Save the preloaded students data
        self.save_students()

    def _create_sample_courses(self):
        """Create sample courses for Zed University"""
        # Computer Science Department
        cs_courses = [
            Course("CS101", "Introduction to Programming", "Computer Science", "Dr. Smith", 5, 2, 
                  ["Mon", "Wed"], time(9, 0), time(10, 30)),
            Course("CS201", "Data Structures", "Computer Science", "Dr. Johnson", 5, 2, 
                  ["Tue", "Thu"], time(11, 0), time(12, 30)),
            Course("CS301", "Algorithms", "Computer Science", "Dr. Lee", 5, 2, 
                  ["Mon", "Wed"], time(13, 0), time(14, 30)),
            Course("CS350", "Database Systems", "Computer Science", "Dr. Garcia", 5, 2, 
                  ["Tue", "Thu"], time(14, 0), time(15, 30)),
            Course("CS401", "Artificial Intelligence", "Computer Science", "Dr. Wong", 5, 2, 
                  ["Mon", "Wed"], time(15, 0), time(16, 30))
        ]
        
        # Mathematics Department
        math_courses = [
            Course("MATH101", "Calculus I", "Mathematics", "Dr. Brown", 5, 2, 
                  ["Mon", "Wed", "Fri"], time(10, 0), time(11, 0)),
            Course("MATH201", "Linear Algebra", "Mathematics", "Dr. Wilson", 5, 2, 
                  ["Tue", "Thu"], time(9, 0), time(10, 30)),
            Course("MATH301", "Differential Equations", "Mathematics", "Dr. Taylor", 5, 2, 
                  ["Mon", "Wed"], time(14, 0), time(15, 30)),
            Course("MATH350", "Probability Theory", "Mathematics", "Dr. Martinez", 5, 2, 
                  ["Tue", "Thu"], time(13, 0), time(14, 30)),
            Course("MATH401", "Real Analysis", "Mathematics", "Dr. Anderson", 5, 2, 
                  ["Mon", "Wed", "Fri"], time(13, 0), time(14, 0))
        ]
        
        # Physics Department
     #   physics_courses = [
      #      Course("PHYS101", "Physics I: Mechanics", "Physics", "Dr. Rodriguez", 30, 4, 
       #           ["Mon", "Wed"], time(11, 0), time(12, 30)),
        #    Course("PHYS201", "Physics II: Electromagnetism", "Physics", "Dr. Lewis", 25, 4, 
         #         ["Tue", "Thu"], time(10, 0), time(11, 30)),
          #  Course("PHYS301", "Quantum Mechanics", "Physics", "Dr. Clark", 20, 4, 
       #           ["Mon", "Wed"], time(14, 0), time(15, 30)),
        #    Course("PHYS350", "Thermodynamics", "Physics", "Dr. Walker", 25, 3, 
         #         ["Tue", "Thu"], time(15, 0), time(16, 30)),
          #  Course("PHYS401", "Nuclear Physics", "Physics", "Dr. Hall", 15, 4, 
           #       ["Mon", "Wed", "Fri"], time(9, 0), time(10, 0))
       # ]
        
        # Add all courses to the course dictionary
        for course in cs_courses + math_courses : # + physics_courses
            self.courses[course.course_id] = course
        
        # Save courses to CSV
        self.save_courses()
    
    def _load_enrollments(self):
        """Load enrollment relationships between students and courses"""
        enrollments_file = os.path.join(self.data_dir, "enrollments.csv")
        if not os.path.exists(enrollments_file):
            return
            
        with open(enrollments_file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    student_id, course_id = row[0], row[1]
                    if student_id in self.students and course_id in self.courses:
                        self.students[student_id].registered_courses.add(course_id)
                        self.courses[course_id].enrolled_students.add(student_id)
    
    def save_data(self):
        """Save all data to CSV files"""
        self.save_students()
        self.save_courses()
        self.save_enrollments()
    
    def save_students(self):
        """Save student data to CSV file"""
        students_file = os.path.join(self.data_dir, "students.csv")
        with open(students_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["StudentID", "Name", "Password", "Email", "Major", "RegisteredCourses"])
            for student in self.students.values():
                writer.writerow(student.to_csv_row())
    
    def save_courses(self):
        """Save course data to CSV file"""
        courses_file = os.path.join(self.data_dir, "courses.csv")
        with open(courses_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["CourseID", "Name", "Department", "Instructor", "MaxStudents", "Credits", 
                            "Days", "StartTime", "EndTime", "EnrolledStudents"])
            for course in self.courses.values():
                writer.writerow(course.to_csv_row())
    
    def save_enrollments(self):
        """Save enrollment relationships to CSV file"""
        enrollments_file = os.path.join(self.data_dir, "enrollments.csv")
        with open(enrollments_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["StudentID", "CourseID", "EnrollmentDate"])
            for student_id, student in self.students.items():
                for course_id in student.registered_courses:
                    writer.writerow([student_id, course_id, datetime.now().strftime("%Y-%m-%d")])
    
    def register_student(self, student_id, name, password):
        """Register a new student"""
        if student_id in self.students:
            return False, "Student ID already exists"
        
        self.students[student_id] = Student(student_id, name, password)
        self.save_students()
        return True, "Student registered successfully"
    
    def authenticate_student(self, student_id, password):
        """Authenticate a student by ID and password"""
        if student_id not in self.students:
            return False, "Student ID not found"
        
        if self.students[student_id].password != password:
            return False, "Incorrect password"
        
        return True, "Authentication successful"
    
    def enroll_student(self, student_id, course_id):
        """Enroll a student in a course"""
        # Validate student and course exist
        if student_id not in self.students:
            return False, "Student not found"
        
        if course_id not in self.courses:
            return False, "Course not found"
        
        student = self.students[student_id]
        course = self.courses[course_id]
        
        # Check if student is already enrolled
        if course_id in student.registered_courses:
            return False, "Already enrolled in this course"
        
        # Check if course is full
        if course.is_full():
            return False, "Course is full"
        
        # Check for schedule conflicts
        if student.has_schedule_conflict(course, self.courses):
            return False, "Schedule conflict with existing course"
        
        # Check credit limit
        new_total_credits = student.get_total_credits(self.courses) + course.credits
        if new_total_credits > self.max_credits:
            return False, f"Credit limit exceeded. Maximum: {self.max_credits}, Attempted: {new_total_credits}"
        
        # Enroll student
        student.registered_courses.add(course_id)
        course.enrolled_students.add(student_id)
        
        # Save changes
        self.save_data()
        
        return True, "Enrollment successful"
    
    def drop_course(self, student_id, course_id):
        """Drop a student from a course"""
        # Validate student and course exist
        if student_id not in self.students:
            return False, "Student not found"
        
        if course_id not in self.courses:
            return False, "Course not found"
        
        student = self.students[student_id]
        course = self.courses[course_id]
        
        # Check if student is enrolled in the course
        if course_id not in student.registered_courses:
            return False, "Not enrolled in this course"
        
        # Drop the course
        student.registered_courses.remove(course_id)
        course.enrolled_students.remove(student_id)
        
        # Save changes
        self.save_data()
        
        return True, "Course dropped successfully"
    
    def get_available_courses(self):
        """Get list of all courses"""
        return list(self.courses.values())
    
    def get_student_courses(self, student_id):
        """Get list of courses a student is enrolled in"""
        if student_id not in self.students:
            return []
        
        student = self.students[student_id]
        return [self.courses[course_id] for course_id in student.registered_courses if course_id in self.courses]


class UniversitySystem:
    def __init__(self):
        self.enrollment_system = EnrollmentSystem()
        self.enrollment_system.preload_students()
        self.current_student = None
    
    def main_menu(self):
        """Display the main menu"""
        self._clear_screen()
        print("=" * 50)
        print("    WELCOME TO ZED UNIVERSITY REGISTRATION SYSTEM    ")
        print("=" * 50)
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print("=" * 50)
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            self.login()
        elif choice == '2':
            self.register()
        elif choice == '3':
            print("Thank you for using the system. Goodbye!")
            exit()
        else:
            input("Invalid choice. Press Enter to continue...")
            self.main_menu()
    
    def login(self):
        """Handle student login"""
        self._clear_screen()
        print("=" * 50)
        print("                   STUDENT LOGIN                     ")
        print("=" * 50)
        
        student_id = input("Enter your Student ID: ")
        password = input("Enter your Password: ")
        
        success, message = self.enrollment_system.authenticate_student(student_id, password)
        
        if success:
            self.current_student = self.enrollment_system.students[student_id]
            print(f"Welcome, {self.current_student.name}!")
            input("Press Enter to continue...")
            self.student_menu()
        else:
            print(f"Login failed: {message}")
            input("Press Enter to continue...")
            self.main_menu()
    
    def register(self):
        """Handle student registration"""
        self._clear_screen()
        print("=" * 50)
        print("                STUDENT REGISTRATION                 ")
        print("=" * 50)
        
        student_id = input("Enter Student ID (e.g., S12345): ")
        name = input("Enter Full Name: ")
        password = input("Create Password: ")
        
        success, message = self.enrollment_system.register_student(student_id, name, password)
        
        if success:
            print("Registration successful!")
            self.current_student = self.enrollment_system.students[student_id]
            input("Press Enter to continue...")
            self.student_menu()
        else:
            print(f"Registration failed: {message}")
            input("Press Enter to continue...")
            self.main_menu()
    
    def student_menu(self):
        """Display the student menu"""
        while True:
            self._clear_screen()
            print("=" * 50)
            print(f"    STUDENT DASHBOARD - {self.current_student.name}    ")
            print("=" * 50)
            
            # Show current credits
            total_credits = self.current_student.get_total_credits(self.enrollment_system.courses)
            print(f"Current Credits: {total_credits}/{self.enrollment_system.max_credits}")
            print("=" * 50)
            
            print("1. View Available Courses")
            print("2. View My Schedule")
            print("3. Enroll in a Course")
            print("4. Drop a Course")
            print("5. Logout")
            print("=" * 50)
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == '1':
                self.view_available_courses()
            elif choice == '2':
                self.view_my_schedule()
            elif choice == '3':
                self.enroll_in_course()
            elif choice == '4':
                self.drop_a_course()
            elif choice == '5':
                self.current_student = None
                print("Logged out successfully.")
                input("Press Enter to continue...")
                self.main_menu()
                break
            else:
                input("Invalid choice. Press Enter to continue...")
    
    def view_available_courses(self):
        """Display all available courses"""
        self._clear_screen()
        print("=" * 80)
        print("                             AVAILABLE COURSES                               ")
        print("=" * 80)
        
        courses = self.enrollment_system.get_available_courses()
        
        # Group courses by department
        departments = {}
        for course in courses:
            if course.department not in departments:
                departments[course.department] = []
            departments[course.department].append(course)
        
        # Display courses by department
        for dept, dept_courses in departments.items():
            print(f"\n{dept} Department:")
            print("-" * 80)
            for course in dept_courses:
                # Check if student is already enrolled
                enrolled = course.course_id in self.current_student.registered_courses
                status = "Enrolled" if enrolled else "Available" if not course.is_full() else "Full"
                
                # Format course info
                print(f"{course.course_id}: {course.name}")
                print(f"  Instructor: {course.instructor}")
                days_str = ", ".join(course.days)
                time_str = f"{course.start_time.strftime('%H:%M')} - {course.end_time.strftime('%H:%M')}" if course.start_time and course.end_time else "N/A"
                print(f"  Schedule: {days_str} {time_str}")
                print(f"  Credits: {course.credits}")
                print(f"  Enrollment: {len(course.enrolled_students)}/{course.max_students}")
                print(f"  Status: {status}")
                print("-" * 80)
        
        input("Press Enter to continue...")
    
    def view_my_schedule(self):
        """Display the student's current schedule"""
        self._clear_screen()
        print("=" * 80)
        print(f"                    MY SCHEDULE - {self.current_student.name}                     ")
        print("=" * 80)
        
        courses = self.enrollment_system.get_student_courses(self.current_student.student_id)
        
        if not courses:
            print("You are not enrolled in any courses.")
        else:
            total_credits = self.current_student.get_total_credits(self.enrollment_system.courses)
            print(f"Total Credits: {total_credits}/{self.enrollment_system.max_credits}")
            print("-" * 80)
            
            # Sort courses by day and time
            courses.sort(key=lambda c: (
                # Sort by day of week (Monday first)
                min([["Mon", "Tue", "Wed", "Thu", "Fri"].index(day) if day in ["Mon", "Tue", "Wed", "Thu", "Fri"] else 6 for day in c.days], default=7),
                # Then by start time
                c.start_time if c.start_time else time(23, 59)
            ))
            
            for course in courses:
                print(f"{course.course_id}: {course.name}")
                print(f"  Department: {course.department}")
                print(f"  Instructor: {course.instructor}")
                days_str = ", ".join(course.days)
                time_str = f"{course.start_time.strftime('%H:%M')} - {course.end_time.strftime('%H:%M')}" if course.start_time and course.end_time else "N/A"
                print(f"  Schedule: {days_str} {time_str}")
                print(f"  Credits: {course.credits}")
                print("-" * 80)
        
        input("Press Enter to continue...")
    
    def enroll_in_course(self):
        """Enroll the student in a new course"""
        self._clear_screen()
        print("=" * 50)
        print("                COURSE ENROLLMENT                  ")
        print("=" * 50)
        
        # Show all available courses
        courses = self.enrollment_system.get_available_courses()
        
        # Filter out full courses and already enrolled courses
        available_courses = [c for c in courses if not c.is_full() and c.course_id not in self.current_student.registered_courses]
        
        if not available_courses:
            print("No available courses to enroll in.")
            input("Press Enter to continue...")
            return
        
        print("Available Courses:")
        print("-" * 50)
        for i, course in enumerate(available_courses):
            print(f"{i+1}. {course.course_id}: {course.name} ({course.department})")
            days_str = ", ".join(course.days)
            time_str = f"{course.start_time.strftime('%H:%M')} - {course.end_time.strftime('%H:%M')}" if course.start_time and course.end_time else "N/A"
            print(f"   Schedule: {days_str} {time_str}")
            print(f"   Credits: {course.credits}")
            print(f"   Instructor: {course.instructor}")
            print(f"   Enrollment: {len(course.enrolled_students)}/{course.max_students}")
            print("-" * 50)
        
        try:
            choice = int(input(f"Enter course number (1-{len(available_courses)}) or 0 to cancel: "))
            
            if choice == 0:
                return
                
            if 1 <= choice <= len(available_courses):
                selected_course = available_courses[choice - 1]
                
                # Confirm enrollment
                print(f"\nYou selected: {selected_course.course_id}: {selected_course.name}")
                confirm = input("Confirm enrollment? (y/n): ").lower()
                
                if confirm == 'y':
                    success, message = self.enrollment_system.enroll_student(
                        self.current_student.student_id, 
                        selected_course.course_id
                    )
                    
                    print(message)
                else:
                    print("Enrollment cancelled.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        
        input("Press Enter to continue...")
    
    def drop_a_course(self):
        """Allow the student to drop a course"""
        self._clear_screen()
        print("=" * 50)
        print("                  DROP COURSE                      ")
        print("=" * 50)
        
        # Get student's courses
        courses = self.enrollment_system.get_student_courses(self.current_student.student_id)
        
        if not courses:
            print("You are not enrolled in any courses.")
            input("Press Enter to continue...")
            return
        
        print("Your Courses:")
        print("-" * 50)
        for i, course in enumerate(courses):
            print(f"{i+1}. {course.course_id}: {course.name} ({course.department})")
            days_str = ", ".join(course.days)
            time_str = f"{course.start_time.strftime('%H:%M')} - {course.end_time.strftime('%H:%M')}" if course.start_time and course.end_time else "N/A"
            print(f"   Schedule: {days_str} {time_str}")
            print(f"   Credits: {course.credits}")
            print(f"   Instructor: {course.instructor}")
            print("-" * 50)
        
        try:
            choice = int(input(f"Enter course number to drop (1-{len(courses)}) or 0 to cancel: "))
            
            if choice == 0:
                return
                
            if 1 <= choice <= len(courses):
                selected_course = courses[choice - 1]
                
                # Confirm drop
                print(f"\nYou selected to drop: {selected_course.course_id}: {selected_course.name}")
                confirm = input("Confirm drop? (y/n): ").lower()
                
                if confirm == 'y':
                    success, message = self.enrollment_system.drop_course(
                        self.current_student.student_id, 
                        selected_course.course_id
                    )
                    
                    print(message)
                else:
                    print("Drop cancelled.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        
        input("Press Enter to continue...")
    
    def _clear_screen(self):
        """Clear the console screen"""
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For Unix/Linux/MacOS
        else:
            os.system('clear')


if __name__ == "__main__":
    university_system = UniversitySystem()
    university_system.main_menu()