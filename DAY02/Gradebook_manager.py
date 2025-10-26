def view():
    print("Function: View all students and their grades. \n")
    for name, subjects in gradebook.items():
        print(f"Name: {name}")
        subject_list = ', '.join(subjects.keys())  # Extract subjects and join with comma
        print(f"Subjects: {subject_list}\n")
        input()

    print("\n")

def addstudent():
    try:
        name = str(input("Enter the name of the student: "))
        gradebook[name]={}
        print("Name added successfully")
        input()

    except ValueError:
        print("Error: Please enter a valid number for marks.")

def updategrade():
    print("Function: Update the grade or marks of a student. \n")
    name = input("Enter the name of the student: ")
    subject = input("New subject of the student: ")
    marks = int(input("Marks of the student: "))
    gradebook[name][subject]=marks
    print("  Grade updated successfully")
    input()



def Remove():
    print("Function: Remove a student from the records.")
    name = input("Enter name of student to be deleted: \n")
    del gradebook[name]
    print("  Student removed successfully")
    input()


def Avg():
    print("Function: Calculate and display the average marks of all students.")
    name=input("enter the name of student to retrieve marks")
    if name in gradebook:
        subjects = gradebook[name]
        total = sum(subjects.values())
        count = len(subjects)
        average = total / count
        print(f"{name}'s average marks: {average:.2f}")
    else:
        print("Student not found in the gradebook.")
    input()
flag = 0 
gradebook = {}   
#menu
while flag == 0:
    try:    
        print("1.View all records")
        print("2.Add a new student")
        print("3.Add/Update subject grade")
        print("4.Remove a student")
        print("5.calculate Average grade")
        print("6.Exit \n")
        e = int(input("Enter option number : " ))
        print ("\n")
        if e == 1:
            view()
        elif e == 2:
            addstudent()
        elif e == 3:
            updategrade()
        elif e == 4:
            Remove()
        elif e == 5:
            Avg()
        elif e==6:
            flag = 1
    except ValueError:
        print("Enter correct option only")
print("program has ended")
#Add a new student function
        

