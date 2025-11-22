class StudentSGrades:
    def __init__(self):
        """Initialize a class to manage student grades.

        Creates empty data structures to store information about students
        and their academic performance.
        """
        self.students = []
        self.average = []


    def check_student(self, name):
        """Checks the correctness of the student's name and its presence in the list.

        Performs two basic checks:
            1. Checks that the name is not empty after clearing spaces
            2. Checks if a student with that name exists in the list (case-insensitive and spaces-free)

        Args:
            name (str): The name of the student to check

        Returns:
            bool:
                - False if the name is empty after clearing
                - True if a student with the same name already exists in the list
                - False if a student with the same name is not found
        """
        clean_name = name.strip().lower()

        if len(clean_name) < 1:
            return False

        for student in self.students:
            if student["name"].strip().lower() == clean_name:
                return True

        return False


    @staticmethod
    def check_correct_name(name):
        """Verifies the correctness of the student's name and normalizes it.

        Args:
            name (str): The student's original name for verification and normalization

        Returns:
            str or None:
                - Normalized name if successful
                - None if the name is empty or contains numbers
        """
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
        """Adds it to the dictionary list.

        If the self.check_student check is successful, it adds the student
        to the dictionary sheet with an empty list of grades, otherwise we return to the beginning

        Args:
            - name(str): The corrected name of the student for verification and normalization
        """
        correct_name = self.check_correct_name(name)
        if correct_name is None:
            return

        exists = self.check_student(correct_name)

        if exists:
            print(f"Student {correct_name} already exist!")
            return

        else:
            new_student = {"name": correct_name, "grades": []}
            self.students.append(new_student)
            print(f"Student {correct_name} added!")


    def add_grade_to_student(self, name):
        """Adds grades for the specified student.

        The process of adding ratings:

        Args:
            name (str): The name of the student for whom grades are being added

        Returns:
            bool:
                - False if the student does not exist
                - True if the scores were added successfully
        """
        exists = self.check_student(name)

        if not exists:
            print(f"Student {name} not exist!")
            return False

        else:
            while True:
                new_grades = input("Enter the score (or 'done' to exit): ").lower()

                if new_grades == "done":
                    print("The input of ratings is completed")
                    break

                try:
                    grade = round(float(new_grades), 1)

                    for student in self.students:
                        if not (0 <= grade <= 100):
                            print("The grade must be between 0 and 100!")
                            break

                        if student["name"] == name:
                            student["grades"].append(grade)
                            self.average.append(grade)
                            print(f"Grade {grade} added for {name}")
                            break

                    print("dictionary", self.students)

                except ValueError:
                    print("Mistake! Enter a number or 'done'")

            return True


    def get_all_students(self):
        """Outputs a report on all students with statistics calculated.

        Displays for each student:
            - Average score on all grades (if there are grades)
            - Message 'N/A' if the student has no grades

        After displaying the individual results, it displays the overall statistics:
            - Maximum average score among all students
            - Minimum average score among all students
            - The overall average score for all grades of all students

        Returns:
            None: The function does not return values, but outputs a report to the console

        Raises:
            ZeroDivisionError: Handled inside the function for students without grades
            """
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
        """
        Finds the student with the highest average score.

        The search process:
            1. Checks the presence of students in the list
            2. Filters students who have at least one grade
            3. Uses the max() function with a lambda expression to find the student
            with a maximum average score
            4. Displays information about the best student

        Note:
            - The arithmetic mean of all student grades is used for the calculation
            - The comparison takes place among students who have at least one grade
            - Lambda function: lambda student: sum(student["grades"]) / len(student["grades"])
        """
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
              f" with a grade of {best_average:.1f}")


    def mainloop(self):
        """The program's main loop is the user interface.

        Loop continues until the user selects the exit option
        If an invalid option is entered, a warning message is displayed
        """
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
                print("Existing program")
                break
            else:
                print("Invalid option!")


if __name__ == "__main__":
    StudentsObj = StudentSGrades()
    StudentsObj.mainloop()
