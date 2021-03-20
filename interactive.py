from main import *
import random
import os
import re

equations = set()

def clear_screen() -> None:
    os.system("clear")

def press_enter_to_menu() -> None:
    input("\nPress enter to return to the menu")

def solve_equations() -> None:
    print("Time to solve some equations")
    print("Use \"=>\" as the arrow/equal sign")
    SENTINEL = "stop"
    while True:
        inp = input(f"\nEnter a chemical equation (type \"{SENTINEL}\" to stop)\n")
        if inp == SENTINEL: break
        coeffs, error = balance(inp)
        if error != "":
            print(error)
            continue
        print("The coefficients are:", coeffs)
        spaceless = "".join(char for char in inp if char != " ")
        print(pretty_balanced_chem_eq(spaceless, coeffs))
    press_enter_to_menu()

def solve_equations_with_explanations() -> None:
    print("Time to solve some equations, but fancier")
    print("Use \"=>\" as the arrow/equal sign")
    SENTINEL = "stop"
    while True:
        inp = input(f"\nEnter a chemical equation (type \"{SENTINEL}\" to stop)\n")
        if inp.lower() == SENTINEL: break
        if (error := validate_input(inp)) != "":
            print(error)
            continue
        print("The Regular Expression says that the input is a valid chemical equation")
        coeffs, error = balance(inp, explain=True)
        if error != "":
            print(error)
            continue
        print("The coefficients are:", coeffs)
        spaceless = "".join(char for char in inp if char != " ")
        print(pretty_balanced_chem_eq(spaceless, coeffs))
    press_enter_to_menu()

def quiz() -> None:
    global equations
    print("Quiz time!")
    print("Answer each equation with a list of coefficients, separated by a space")
    print("Example: \"1 6 3 2\"")
    print()
    correct = incorrect = total = 0
    SENTINEL = "stop"
    while True:
        if equations == set():
            load_equations()
        equation = random.choice([*equations])
        print(f"Balance this equation: (type \"{SENTINEL}\" to stop)")
        print(equation)
        compound_count = len(re.split(r"\+|\=\>", equation))
        list_validator = r"^(?:\d+\s+){" + str(compound_count - 1) + r"}\d+$"
        while re.match(list_validator, (inp := input())) is None:
            if inp.lower() == SENTINEL: break
            print(f"Invalid input! Your list should only contain numbers, be separated by a single space, and be of length {compound_count}")
        if inp.lower() == SENTINEL: break
        official_answer, _ = balance(equation)
        given_answer = [int(n) for n in inp.split(" ")]
        if official_answer == given_answer:
            print("Correct!")
            correct += 1
        else:
            print(f"Incorrect! The correct coefficients are {', '.join(str(n) for n in official_answer)}")
            incorrect += 1
        total += 1
        print(pretty_balanced_chem_eq(equation, official_answer))
        print(f"Current score => Correct: {correct} ; Incorrect: {incorrect} ; Total: {total} ; Correct/Incorrect ratio: {correct / incorrect if incorrect != 0 else 'N/A'} ; Grade: {correct / total * 100}")
        print()
    print()
    print(f"Final score => Correct: {correct} ; Incorrect: {incorrect} ; Total: {total} ; Correct/Incorrect ratio: {correct / incorrect if incorrect != 0 else 'N/A'} ; Grade: {correct / total * 100}")
    press_enter_to_menu()

def validate_solutions() -> None:
    print("Validated")
    input()

def about() -> None:
    parts = {
        "Author": "Samuel Gunter",
        "Project name": "Cosmic Chem",
        "Purpose": "To automatically balance chemical equations, with options explanations, to quiz on balancing equations, and to validate possible solutions",
        "How it works": "When input it received, it first validates the chemical equation with a Regular Expression, then it parses the equation into a matrix where each column in a compound, each row is an element, and the intersection is how many moles of the specific element in that compound. It then transforms the matrix into the \"Row Reduced Echelon Form\", grabs the last column, finds the greatest common denominator, multiples that column by the gcd, and that is your coefficients for the compounds, except the last compound's coefficient is just the gcd from before."
    }
    for key, value in parts.items():
        print(f"{key}: {value}\n")
    press_enter_to_menu()

def menu() -> None:
    clear_screen()
    print_logo()
    print()
    print("What would you like to do next?")
    print("a) Balance chemical equations")
    print("b) Balance chemical equations with explanations")
    print("c) Quiz yourself")
    print("d) Validate solutions")
    print("e) View the About page")
    print("f) Exit the program")
    while True:
        inp = input().lower()
        if len(inp) == 0:
            print("Please enter a letter a-f")
            continue
        elif len(inp) > 1:
            print("Please only enter one letter a-f")
            continue
        if inp not in "abcdef":
            print("Please enter a letter a-f")
            continue
        break
    if inp != "f": clear_screen()
    if inp == "a":
        solve_equations()
        print()
        menu()
    elif inp == "b":
        solve_equations_with_explanations()
        print()
        menu()
    elif inp == "c":
        quiz()
        print()
        menu()
    elif inp == "d":
        validate_solutions()
        print()
        menu()
    elif inp == "e":
        about()
        print()
        menu()
    elif inp == "f":
        print()
        print("Goodbye!")
        exit(0)

def load_equations() -> None:
    global equations
    with open("equations.txt", "r") as file:
        equations = set(file.read().splitlines())
        equations = [eq for eq in equations if len(eq) > 0 and eq[0] != "#"]

if __name__ == "__main__":
    menu()
