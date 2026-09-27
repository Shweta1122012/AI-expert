import json

FILE_NAME = "students.json"


def load_students():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


def add_student(students):
    name = input("Enter student name: ")
    marks = []

    for i in range(3):
        mark = float(input(f"Enter marks for subject {i + 1}: "))
        marks.append(mark)

    students[name] = marks
    save_students(students)

    print(f"\n{ name } has been added successfully!")


def show_students(students):
    if not students:
        print("\nNo students found.")
        return

    print("\n--- Student Records ---")

    for name, marks in students.items():
        average = sum(marks) / len(marks)

        if average >= 90:
            grade = "A"
        elif average >= 75:
            grade = "B"
        elif average >= 60:
            grade = "C"
        elif average >= 40:
            grade = "D"
        else:
            grade = "F"

        print(f"\nName: {name}")
        print(f"Marks: {marks}")
        print(f"Average: {average:.2f}")
        print(f"Grade: {grade}")


def search_student(students):
    name = input("Enter student name to search: ")

    if name in students:
        marks = students[name]
        average = sum(marks) / len(marks)

        print("\nStudent Found!")
        print("Name:", name)
        print("Marks:", marks)
        print(f"Average: {average:.2f}")
    else:
        print("Student not found.")


def main():
    students = load_students()

    while True:
        print("\n====== STUDENT GRADE MANAGER ======")
        print("1. Add Student")
        print("2. Show Students")
        print("3. Search Student")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_student(students)

        elif choice == "2":
            show_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


main()