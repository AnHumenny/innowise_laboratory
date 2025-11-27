class StudentSGrades:
    def __init__(self):
        """Initialize a class to manage student grades.

        Creates empty data structures to store information about students
        and their academic performance.
        """
        self.students = []

    @staticmethod
    def check_correct_name(name: str):
        """Verifies the correctness of the student's name and normalizes it.

        Checks:
        - Not empty
        - Contains no digits
        - Contains no forbidden special characters
        - Allowed: letters, spaces, hyphen (-), apostrophe (')
        """

        if not name or not name.strip():
            print("The name can't be empty!")
            return None

        parts = name.strip().split()

        if any(any(ch.isdigit() for ch in word) for word in parts):
            print("The name must not contain numbers!")
            return None

        allowed_extra = set(" -'")

        if any(not (ch.isalpha() or ch in allowed_extra) for ch in name):
            print("The name contains invalid characters!")
            return None

        return " ".join(x.capitalize() for x in parts)


    def check_student(self, name: str):
        """Finds a student by name (case-insensitive).

        Searches through the student list for a case-insensitive match
        of the provided name.

        Args:
            name (str): The student's name to search for

        Returns:
            dict or None: Student dictionary if found, None if no match found
        """
        clean = name.strip().lower()
        for st in self.students:
            if st["name"].lower() == clean:
                return st
        return None


    def add_to_dictionary(self, name: str):
        """Adds a new student to the dictionary after validation.

        Validates the student name, checks for duplicates, and adds the student
        to the dictionary with an empty grades list if validation passes.

        Args:
            name (str): The student's name to add

        Returns:
            None: This method doesn't return anything but may print status messages
        """
        correct_name = self.check_correct_name(name)
        if correct_name is None:
            return

        if self.check_student(correct_name):
            print(f"Student {correct_name} already exist!")
            return

        self.students.append({"name": correct_name, "grades": []})
        print(f"Student {correct_name} added!")


    def add_grade_to_student(self, name: str):
        """Adds grades for a student through interactive input.

        Prompts the user to enter grades for a specified student in a loop.
        Validates each grade and adds it to the student's record.

        Args:
            name (str): The name of the student to add grades for

        Returns:
            bool: True if operation completed (student exists), False if student not found

        """
        student = self.check_student(name)
        if not student:
            print(f"Student {name} not exist!")
            return False

        while True:
            new_grade = input("Enter the grade (or 'done' to finish): ").lower().strip()

            if new_grade == "done":
                print("The input of ratings is completed")
                break

            try:
                grade = int(new_grade)

                if not (0 <= grade <= 100):
                    print("The grade must be between 0 and 100!")
                    continue

                student["grades"].append(grade)
                print(f"Grade {grade} added for {student['name']}")

            except ValueError:
                print("Invalid input. Please enter a number.")

        return True


    def get_all_students(self):
        """Displays student averages and summary statistics.

        Calculates and displays the average grade for each student, followed by
        overall class statistics including maximum, minimum, and overall average.

        Returns:
            None: Outputs results directly to console
        """
        if not self.students:
            print("There is no list of students")
            return

        student_averages = []

        for student in self.students:
            if student["grades"]:
                avg = sum(student["grades"]) / len(student["grades"])
                student_averages.append(avg)
                print(f"{student['name']}`s average grade is {avg:.1f}.")
            else:
                print(f"{student['name']}`s average grade is: N/A.")

        if not student_averages:
            print("No grades to analyze!")
            return
        print("-" * 28)
        print(f"Max average: {max(student_averages):.1f}")
        print(f"Min average: {min(student_averages):.1f}")
        print(f"Overall average: {sum(student_averages) / len(student_averages):.1f}")


    def find_the_best_student(self):
        """Finds the student with the highest average grade.

        Identifies the top-performing student based on their average grade.
        Only considers students who have at least one grade recorded.

        Returns:
            None: Outputs the result directly to console
        """
        students_with_grades = [x for x in self.students if x["grades"]]

        if not students_with_grades:
            print("There are no grades in the list of students!")
            return

        best_student = max(students_with_grades,
                           key=lambda st: sum(st["grades"]) / len(st["grades"]))

        best_average = sum(best_student["grades"]) / len(best_student["grades"])
        print(f"The student with the highest average is {best_student['name']} "
              f"with a grade of {best_average:.1f}.")

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
                name = input("Add grades for a student: ")
                self.add_grade_to_student(name)

            elif choice == "3":
                self.get_all_students()

            elif choice == "4":
                self.find_the_best_student()

            elif choice == "5":
                print("Exiting program.")
                break

            else:
                print("Invalid option!")


if __name__ == "__main__":
    StudentsObj = StudentSGrades()
    StudentsObj.mainloop()
