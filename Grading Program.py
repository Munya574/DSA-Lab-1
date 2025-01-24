category = []
for i in range(len(grades)):
    if grades[i] >= 90:
        category.append('Excellent')
    elif grades[i] >= 80:
        category.append('Good')
    elif grades[i] >= 70:
        category.append('Avergae')
    else:
        category.append('Needs Improvement')