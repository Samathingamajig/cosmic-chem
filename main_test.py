import unittest
from main import *

class TestFull(unittest.TestCase):
    def test_main(self):
        tests = [
            ["AgNO3+Na2CO3=>Ag2CO3+NaNO3", [2, 1, 1, 2]],
            ["BaCl2+K3PO4=>Ba3P2O8+KCl", [3, 2, 1, 6]]
        ]
        for inp, out in tests:
            self.assertEqual(balance(inp), out)

if __name__ == "__main__":
    unittest.main()
