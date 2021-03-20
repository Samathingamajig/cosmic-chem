import unittest
from main import *

class TestFull(unittest.TestCase):
    def test_main(self):
        tests = [
            ["AgNO3+Na2CO3=>Ag2CO3+NaNO3", [2, 1, 1, 2]],
            ["BaCl2+K3PO4=>Ba3P2O8+KCl", [3, 2, 1, 6]]
        ]
        for i, (inp, out) in enumerate(tests):
            if balance(inp) != (out, ''):
                print(i, inp, "|", out)
            self.assertEqual(balance(inp), (out, ''))
    
    def test_equations_txt(self):
        with open("equations.txt", "r") as file:
            equations = file.read().splitlines()
            equations = [eq for eq in equations if eq != "" and eq[0] != "#"]
        for i, eq in enumerate(equations):
            if balance(eq)[1] != "":
                print(i, eq)
            self.assertEqual(balance(eq)[1], "")

if __name__ == "__main__":
    unittest.main()
