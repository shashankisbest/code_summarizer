import json

def load_students(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_students(filename, students):
    with open(filename, "w") as file:
        json.dump(students, file, indent=4)

def add_student(students, name, age, marks):
    student = {
        "name": name,
        "age": age,
        "marks": marks
    }
    students.append(student)
    return students

def calculate_average(marks):
    total = 0
    for mark in marks:
        total += mark
    if len(marks) == 0:
        return 0
    return total / len(marks)

def find_top_student(students):
    top_student = None
    highest_average = 0

    for student in students:
        avg = calculate_average(student["marks"])
        if avg > highest_average:
            highest_average = avg
            top_student = student

    return top_student

def filter_passed_students(students, passing_marks=40):
    passed = []

    for student in students:
        avg = calculate_average(student["marks"])
        if avg >= passing_marks:
            passed.append(student)

    return passed

class StudentManager:

    def __init__(self, filename):
        self.filename = filename
        self.students = load_students(filename)

    def add(self, name, age, marks):
        self.students = add_student(self.students, name, age, marks)
        save_students(self.filename, self.students)

    def get_topper(self):
        return find_top_student(self.students)

    def get_passed(self):
        return filter_passed_students(self.students)

    def display_all(self):
        for student in self.students:
            print("Name:", student["name"])
            print("Age:", student["age"])
            print("Marks:", student["marks"])
            print("Average:", calculate_average(student["marks"]))
            print("------------------------")


def main():
    manager = StudentManager("students.json")

    manager.add("Alice", 20, [85, 90, 88])
    manager.add("Bob", 22, [40, 42, 38])
    manager.add("Charlie", 19, [95, 92, 93])

    print("All Students:")
    manager.display_all()

    print("Top Student:")
    print(manager.get_topper())

    print("Passed Students:")
    print(manager.get_passed())


if __name__ == "__main__":
    main()