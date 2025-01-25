students = []
grades = []
category = []

Max_students = 10

from tabulate import tabulate

count = 0 
while count < 10:
    s = input('Enter name(Enter "cancel" to stop): ')
    if s == "cancel":
        break
    g = eval(input('Enter grade: '))
    students.append(s)
    grades.append(g)
    count += 1

for i in range(len(grades)):
    if grades[i] >= 90:
        category.append('Excellent')
    elif grades[i] >= 80:
        category.append('Good')
    elif grades[i] >= 70:
        category.append('Avergae')
    else:
        category.append('Needs Improvement')
print(category)

data = [students, grades, category]
header = ['Name', 'Grade', 'Category']
print(tabulate(data, headers=header, tablefmt="pretty"))
