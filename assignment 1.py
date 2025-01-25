from tabulate import tabulate

while len(students) < max_students:
    s = input('Enter name(input "cancel" to break): ')
    if s == "cancel":
        break
    if not name:
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
        


data = [students, grades, category]
header = ['Name', 'Grade', 'Category']
print(tabulate(data, headers=headers, tablefmt="pretty"))
