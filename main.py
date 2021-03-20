import re
import sympy as sp
from sympy.matrices.dense import MutableDenseMatrix
from sympy.polys.ring_series import _coefficient_t

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
    matrix = chem_eq_to_matrix(chem_eq)
    rref = matrix.rref()[0]
    coefficients = get_coefficients(rref, chem_eq)
    return coefficients

def repl() -> None:
    SENTINEL = str(-1)
    print("Type -1 to stop")
    while True:
        inp = input()
        if inp == SENTINEL: break
        print(balance(inp))

if __name__ == "__main__":
    repl()