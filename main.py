import re
import sympy as sp
from sympy.matrices.dense import MutableDenseMatrix

# Used for regex's
SYMBOL = r"[A-Z][a-z]?"
OPT_NUMS = r"\d*"
OPT_SPACES = r"\ *"
GROUPED_ELEMENTS = rf"\((?:{SYMBOL}{OPT_NUMS})+\)"
COMPOUND = rf"(?:(?:{SYMBOL}|{GROUPED_ELEMENTS}){OPT_NUMS})+"
SIDE = rf"(?:{COMPOUND}{OPT_SPACES}\+)*{OPT_SPACES}{COMPOUND}"
CHEMICAL_EQUATION = rf"{SIDE}{OPT_SPACES}=>{OPT_SPACES}{SIDE}"

def validate_input(chem_eq: str) -> str:
    chem_eq = chem_eq.strip()
    # Giant regex to test chemical equation
    test = re.match(rf"^{CHEMICAL_EQUATION}$", chem_eq)
    if test is not None: return ""

    if (arrow_count := chem_eq.count("=>")) != 1:
        return f"This equation has {arrow_count} arrows ( => ), but it needs exactly 1 arrow"
    if (extra_arrow_parts := re.search(r"=(?!\>)|(?<!\=)\>", chem_eq)) is not None:
        return f"Unexpected character \"{extra_arrow_parts.group()}\" at index {extra_arrow_parts.start()} (starting from 0)"
    ALLOWED_CHARS = r"A-Za-z0-9+=>\ \(\)"
    if (bad_chars := re.search(rf"[^{ALLOWED_CHARS}]", chem_eq)) is not None:
        return f"Unexpected character \"{bad_chars.group()}\" at index {bad_chars.start()} (starting from 0)"
    if (unexpected_lowercase := re.search(r"(?<![A-Z])([a-z])", chem_eq)) is not None:
        return f"Unexpected lowercase letter \"{unexpected_lowercase.group()}\" at index {unexpected_lowercase.start()} (starting from 0)"
    if (extra_plusses := re.search("(?:\+\s*){2,}", chem_eq)) is not None:
        return f"You should only have one plus sign between each compound, index {extra_plusses.start()} (starting from 0)"
    if (missing_plus := re.search(rf"({COMPOUND})\s+{COMPOUND}", chem_eq)) is not None:
        return f"You need to have a plus sign between compounds, or maybe you have an extra space, index {missing_plus.start() + len(missing_plus.groups(1))} (starting from 0)"
    if (out_of_place_number := re.search(rf"(?<![A-Za-z0-9\)])\d", chem_eq)) is not None:
        return f"Unexpected number at index {out_of_place_number.start() + 1} (starting from 0)"
    if (unexpected_plus := re.search(r"(?<![A-Za-z0-9\)])\+", chem_eq)) is not None:
        return f"Unexpected plus at index {unexpected_plus.start() + 1} (starting from 0)"
    if (nested_or_unclosed_parens := re.search(r"\([^\)]*\(|\([^\)]*$", chem_eq)) is not None:
        return f"You have nested (unsupported) or unclosed parentheses at index {nested_or_unclosed_parens.start()} (starting from 0)"
    if (unexpected_close_parens := re.search(r"^[^\(]\)|(?<=\))[^\(\)\n]*\)", chem_eq)) is not None:
        return f"Unexpected close parentheses at index {unexpected_close_parens.end() - 1} (starting from 0)"
    if (number_starts_with_zero := re.search(r"(?<=[A-Za-z\)])0")) is not None:
        return f"A subscript/coefficient cannot start with zero/0, index {number_starts_with_zero.end() - 1} (starting from 0)"
    return "You have an error, but we don't know what exactly it is"

def filter_parentheses(chem_eq: str):
    left, right = chem_eq.split("=>")
    left_comps, right_comps = left.split("+"), right.split("+")
    def fp_side(comps):
        new_comps = []
        for comp in comps:
            minis = re.findall(rf"{SYMBOL}{OPT_NUMS}|{GROUPED_ELEMENTS}{OPT_NUMS}", comp)
            new_comp = ""
            for mini in minis:
                if mini[0] != "(":
                    new_comp += mini
                    continue
                multiply = int(re.search(r"\d+$", mini).group())
                mini_eles = re.findall(rf"{SYMBOL}{OPT_NUMS}", re.search(rf"\(((?:{SYMBOL}{OPT_NUMS})+)\)", mini).group())
                for i, mini_ele in enumerate(mini_eles):
                    ele = re.search(SYMBOL, mini_ele).group()
                    coeff = 1
                    coeff_search = re.search(r"\d+", mini_ele)
                    if coeff_search is not None:
                        coeff = int(coeff_search.group())
                    coeff *= multiply
                    mini_eles[i] = f"{ele}{coeff if coeff > 1 else ''}"
                new_comp += "".join(mini_eles)
            new_comps.append(new_comp)
        return "+".join(new_comps)
    return f"{fp_side(left_comps)}=>{fp_side(right_comps)}"

def chem_eq_to_matrix(chem_eq: str) -> MutableDenseMatrix:
    elements = list(set(re.findall(r"[A-Z][a-z]?", chem_eq)))
    # print(elements)
    all_compounds = list(re.split(r"\+|=\>", chem_eq))
    # print(all_compounds)
    number_of_compounds = len(all_compounds)
    left_side, right_side = chem_eq.split("=>")
    matrix = sp.Matrix([[0] * number_of_compounds] * len(elements))
    for col, comp in enumerate(left_side.split("+")):
        for row, ele in enumerate(elements):
            # print(row, col, comp, ele, re.findall(rf"{ele}(?![a-z])(\d*)", comp))
            total_quantity = sum(int(quan or 1) for quan in re.findall(rf"{ele}(?![a-z])(\d*)", comp))
            matrix[row, col] = total_quantity
    for col, comp in enumerate(right_side.split("+"), start=len(left_side.split("+"))):
        for row, ele in enumerate(elements):
            # print(row, col, comp, ele, re.findall(rf"{ele}(?![a-z])(\d*)", comp))
            total_quantity = sum(int(quan or 1) for quan in re.findall(rf"{ele}(?![a-z])(\d*)", comp))
            matrix[row, col] = -1 * total_quantity
    # print(repr(matrix))
    return matrix

def get_reduced_row_echelon_form(matrix: MutableDenseMatrix) -> MutableDenseMatrix:
    return matrix.rref()[0]

def get_coefficients(rref: MutableDenseMatrix, chem_eq):
    all_compounds = list(re.split(r"\+|=\>", chem_eq))
    coefficients = [1] * len(all_compounds)
    denoms = [num.denominator() for num in rref.col(-1)]
    the_lcm = sp.lcm(denoms)
    for i, _ in enumerate(coefficients[:-1]):
        numer, denom = rref[i,-1].p, rref[i,-1].q
        if numer == 0:
            return [0] * len(all_compounds)
        coefficients[i] = abs(numer * (the_lcm / denom))
    coefficients[-1] = the_lcm
    return coefficients

def balance(chem_eq: str) -> str:
    chem_eq = chem_eq.strip()
    if (error := validate_input(chem_eq)) != "":
        return [], error
    spaceless = "".join(char for char in chem_eq if char != " ")
    no_parens = filter_parentheses(spaceless)
    matrix = chem_eq_to_matrix(no_parens)
    rref = matrix.rref()[0]
    # print(repr(rref))
    coefficients = get_coefficients(rref, no_parens)
    if len([coeff for coeff in coefficients if coeff != 0]) != len(coefficients):
        return [], "This equation either has no solutions or an infinite number of solutions"
    return coefficients, ''

def repl() -> None:
    SENTINEL = str(-1)
    print("Type -1 to stop")
    while True:
        inp = input()
        if inp == SENTINEL: break
        print(balance(inp))

def print_logo() -> None:
    with open("cosmic_chem.txt", "r") as cc_file:
        print(cc_file.read())

if __name__ == "__main__":
    pass
    # repl()
