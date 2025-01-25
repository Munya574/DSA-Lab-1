students = []
grades = []
category = []

Max_students = 10

from tabulate import tabulate

while len(students) < Max_students:
    s = input('Enter name(input "cancel" to quit): ')
    if s == "cancel":
        break
    if not s:
        print("Name cannot be empty.")
        continue
    
    try:
        g = eval(input('Enter grade: '))
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

data = [students, grades, category]
header = ['Name', 'Grade', 'Category']
print(tabulate(data, headers=headers, tablefmt="pretty"))
