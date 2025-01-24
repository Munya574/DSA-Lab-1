from tabulate import tabulate

count = 0 
while count < 10:
    s = input('Enter name(input "cancel" to break): ')
    if s == "cancel":
        break
    g = input('Enter grade: ')
    students.append(s)
    grades.append(g)
    count += 1


data = [students, grades, category]
header = ['Name', 'Grade', 'Category']
print(tabulate(data, headers=headers, tablefmt="pretty"))
