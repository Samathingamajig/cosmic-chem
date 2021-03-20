from main import *
import os

def clear_screen() -> None:
    os.system("clear")

def press_continue() -> None:
    input("Press enter to continue")

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
    press_continue()

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
    press_continue()

def quiz() -> None:
    print("Quiz time!")
    input()

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
    press_continue()

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

if __name__ == "__main__":
    print_logo()
    menu()
