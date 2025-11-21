class StudentSGrades:
    def __init__(self):
        self.students = []
        self.average = []


    def check_student(self, name):
        clean_name = name.strip().lower()
        if len(clean_name) < 1:
            return False
        for student in self.students:
            if student["name"].strip().lower() == clean_name:
                return True
        return False


    @staticmethod
    def check_correct_name(name):
        if not name or not name.strip():
            print("The name can't be empty!")
            return None

        name_parts = name.strip().split()

        for name in name_parts:
            if any(char.isdigit() for char in name):
                print("The name must not contain numbers!")
                return None

        correct_name = " ".join(word.capitalize() for word in name_parts)
        return correct_name


    def add_to_dictionary(self, name):
        correct_name = self.check_correct_name(name)
        if correct_name is None:
            return

        exists = self.check_student(correct_name)
        print("exists", exists)

        if exists:
            print(f"Student {correct_name} already exist!")
            return
        else:
            new_student = {"name": correct_name, "grades": []}
            self.students.append(new_student)
            print(f"Student {correct_name} added!")
            print("List of students:", self.students)


    def add_grade_to_student(self, name):
        exists = self.check_student(name)
        if not exists:
            print(f"Student {name} not exist!")
            return False
        else:
            while True:
                new_grades = input("Enter the score (or 'done' to exit): ")
                if new_grades == "done":
                    print("The input of ratings is completed")
                    break
                try:
                    grade = round(float(new_grades), 2)
                    for student in self.students:
                        if student["name"] == name:
                            student["grades"].append(grade)
                            self.average.append(grade)
                            print(f"Grade {grade} added for {name}")
                            print("Dictionary", self.students)
                            break
                except ValueError:
                    print("Mistake! Enter a number or 'done'")
            return True


    def get_all_students(self):
        """Get a list of all students with an average score."""

        if not self.students:
            print("There is no list of students")

        for student in self.students:
            try:
                student_average = sum(student["grades"]) / len(student["grades"])
                print(f"{student['name']}`s average grade is {student_average:.1f}")
            except ZeroDivisionError:
                print(f"Average score {student['name']}: N/A")

        if len(self.average) == 0:
            print("The list of student grades is incomplete!")
            return

        print(f"Max average: {max(self.average):.1f}")
        print(f"Min average: {min(self.average):.1f}")
        print(f"Overall average: {sum(self.average) / len(self.average):.1f}")


    def find_the_best_student(self):
        """Find the best student """
        if not self.students:
            print("Student not found!")
            return

        students_with_grades = [s for s in self.students if s["grades"]]

        if not students_with_grades:
            print("There are no grades in the list of students!")
            return

        best_student = max(students_with_grades,
                           key=lambda student: sum(student["grades"]) / len(student["grades"]))

        best_average = sum(best_student["grades"]) / len(best_student["grades"])
        print(f"The student with the highest average is {best_student['name']}"
              f"with a grade of {best_average:.2f}")


    def mainloop(self):
        while True:
            print("-" * 28)
            print("---Student Grade Analyzer---")
            print("1. Add a new student")
            print("2. Add grades for a student")
            print("3. Generate full report")
            print("4. Find the best student")
            print("5. Exit")
            print("-" * 28)

            choice = input("Enter your choice: ")
            print("- " * 11)

            if choice == "1":
                name = input("Input the name of the new student: ")
                self.add_to_dictionary(name)
            elif choice == "2":
                grades = input("Add grades for a student: ")
                self.add_grade_to_student(grades)
            elif choice == "3":
                self.get_all_students()
            elif choice == "4":
                self.find_the_best_student()
            elif choice == "5":
                break
            else:
                print("Invalid option!")


if __name__ == "__main__":
    StudentsObj = StudentSGrades()
    StudentsObj.mainloop()
