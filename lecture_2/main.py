def generate_profile(age):
    """Determine life stage based on age.

    Categorizes user into life stages: Child (≤12), Teenager (13-19), Adult (≥20).
    """
    if age <= 12:
        return "Child"
    elif age <= 19:
        return "Teenager"
    else:
        return "Adult"


def build_profile(full_name, birth_year):
    """Generate user profile data and display the complete profile.

    Calculates age and life stage, then continuously queries hobbies until the user hits stop
    to create a full dictionary-style profile
    """
    current_age = 2025 - birth_year
    life_stage = generate_profile(current_age)

    hobbies = []

    while True:
        user_hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
        if user_hobby.lower() == "stop":
            break
        if user_hobby.strip():
            hobbies.append(user_hobby)

    user_profile = {
        'Name': full_name,
        'Age': current_age,
        'Life Stage': life_stage,
        'Favorite Hobbies': hobbies,
    }

    display_profile(user_profile)


def display_profile(user_profile):
    """Displaying the profile summary in a formatted way.

    Formats and prints user profile data with special handling for hobbies.
    Handles single hobby, multiple hobbies, and no hobbies cases.
    """
    print("---")
    print("Profile Summary:")

    for key, value in user_profile.items():
        if key == 'Favorite Hobbies' and isinstance(value, list):
            if len(value) > 1:
                print(f"{key} ({len(value)}):")
                for hobby in value:
                    print(f"- {hobby}")
            elif len(value) == 1:
                print(f"{key:20}: {value[0]}")
            else:
                print("You didn't mention any hobbies")
        else:
            print(f"{key}: {value}")
    print("---")


def mainloop():
    """Main interaction loop for collecting and processing user information.

    Orchestrates the complete user registration flow:
    - Collects full name and birth year
    - Validates input data
    - Proceeds to hobby collection on success
    - Displays error message on validation failure
    """
    print("Hello, user! Could you give some information about yourself?")
    full_name = input("Enter your full name: ")
    birth_year_str = input("Enter your birth year: ")

    build_profile(full_name, int(birth_year_str))


if __name__ == "__main__":
    mainloop()
