students = []
grades = []
category = []

Max_students = 10

while len(students) < Max_students:
    s = input('Enter name(input "cancel" to quit): ')
    if s == "cancel":
        break
    if not s:
        print("Name cannot be empty.")
        continue
    
    try:
        g = int(input('Enter grade: '))
        if 0 <= g <= 100:
            students.append(s)
            grades.append(g)
        else:
            print("Grade must be between 0 and 100.")
    except ValueError:
        print(" Invalid input")

for i in range(len(grades)):
    if grades[i] >= 90:
        category.append('Excellent')
    elif grades[i] >= 80:
        category.append('Good')
    elif grades[i] >= 70:
        category.append('Avergae')
    else:
        category.append('Needs Improvement')

data = [["Name", "Grade", "Category"]]
for i in range(len(students)):
    data.append([students[i], grades[i], category[i]])

col_widths = [max(len(str(row[i])) for row in data) for i in range(len(data[0]))]

for row in data:
    print("  ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
