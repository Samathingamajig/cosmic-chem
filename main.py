#!/usr/local/bin/python3.9

def lcm(*nums: int) -> int:
    lcm = max(nums)
    while True:
        failure = False
        for num in nums:
            failure = lcm % num != 0
            if failure: break
        if not failure: return lcm
        lcm += 1

def gcd(*nums: int) -> int:
    gcd = 1
    new_gcd = gcd
    while new_gcd <= min(nums):
        failure = False
        for num in nums:
            failure = num % new_gcd != 0
            if failure: break
        if not failure: gcd = new_gcd
        new_gcd += 1
    return gcd

class Compound:
    def __init__(self):
        self.coefficient = 1
        self.elements = {}
    
    def add_element(self, symbol: str, quantity: int) -> None:
        if symbol in self.elements.keys():
            self.elements[symbol] += quantity
        else:
            self.elements[symbol] = quantity
    
    def amount_of_raw(self, symbol: str) -> int:
        if symbol in self.elements.keys():
            return self.elements[symbol]
        return 0
    
    def amount_of(self, symbol: str) -> int:
        if symbol in self.elements.keys():
            return self.coefficient * self.elements[symbol]
        return 0
    
    def readable(self) -> str:
        return str(self.coefficient if self.coefficient > 1 else '') + "".join(f"{ele}{quant if quant > 1 else ''}" for ele, quant in self.elements.items())
    
    def __str__(self) -> str:
        return "{" + f"{self.coefficient}, {', '.join(str(ele) for ele in self.elements.items())}" + "}"

class Side:
    def __init__(self):
        self.compounds = []
    
    def add_compound(self, compound: Compound) -> None:
        self.compounds.append(compound)
    
    def amount_of(self, symbol: str) -> int:
        total_amount = 0
        for comp in self.compounds:
            total_amount += comp.amount_of(symbol)
        return total_amount
    
    def is_balanced_with(self, other) -> bool:
        return self.totals() == other.totals()
    
    def simple_elements(self) -> set[str]:
        symbols = self.totals().keys()
        simple_elements = set()
        for symbol in symbols:
            seen = 0
            for compound in self.compounds:
                if symbol in compound.elements.keys():
                    seen += 1
                    if seen > 1: break
            if seen == 1:
                simple_elements.add(symbol)
        return simple_elements
    
    def get_compounds_with_symbol(self, symbol: str) -> set[Compound]:
        return set(comp for comp in self.compounds if comp.amount_of(symbol) > 0)

    def get_se_compound(self, symbol: str) -> Compound:
        return list(self.get_compounds_with_symbol(symbol))[0]
    
    def totals(self) -> dict:
        totals = {}
        for comp in self.compounds:
            for sym, quant in comp.elements.items():
                if sym in totals.keys():
                    totals[sym] += quant * comp.coefficient
                else:
                    totals[sym] = quant * comp.coefficient
        return totals
    
    def readable(self) -> str:
        return f"{' + '.join(comp.readable() for comp in self.compounds)}"
    
    def __str__(self) -> str:
        return f"[{' + '.join(str(comp) for comp in self.compounds)}]"

class ChemicalEquation:
    def __init__(self):
        self.left = None
        self.right = None
    
    def add_side(self, side: Side) -> None:
        if self.left is None:
            self.left = side
        else:
            self.right = side
    
    def sses_are_balanced(self) -> bool:
        _lt, _rt = self.totals()
        lt, rt = _lt.copy(), _rt.copy()
        sses = self.super_simple_elements()
        for sym in _lt.keys():
            if sym not in sses:
                del lt[sym]
        for sym in _rt.keys():
            if sym not in sses:
                del rt[sym]
        return lt == rt
    
    def is_balanced(self) -> bool:
        return self.left.is_balanced_with(self.right)
    
    def totals(self) -> dict:
        return self.left.totals(), self.right.totals()
    
    def super_simple_elements(self) -> set[str]:
        return self.left.simple_elements() & self.right.simple_elements()
    
    def non_sses(self) -> set[str]:
        return (
            set(self.left.totals().keys())
            .union(set(self.right.totals().keys()))
            ).difference(self.super_simple_elements())
    
    def balance_sses(self) -> None:
        if self.sses_are_balanced(): return
        sses = self.super_simple_elements()
        lt, rt = self.totals()
        while not self.sses_are_balanced():
            for sse in sses:
                if lt[sse] != rt[sse]:
                    the_lcm = lcm(lt[sse], rt[sse])
                    lc = self.left.get_se_compound(sse)
                    rc = self.right.get_se_compound(sse)
                    lc.coefficient *= the_lcm // lt[sse]
                    rc.coefficient *= the_lcm // rt[sse]
                lt, rt = self.totals()
    
    def balance(self) -> None:
        if self.is_balanced(): return
        self.balance_sses()
        # lt, rt = self.totals()
        # non_sses = self.non_sses()
        # for nsse in non_sses:
        #     if lt[nsse] == rt[nsse]: continue
        #     lcs = self.left.get_compounds_with_symbol(nsse)
        #     rcs = self.right.get_compounds_with_symbol(nsse)
        #     if len(lcs) == 1:
        #         lc = list(lcs)[0]
        #         for rc in rcs:
        #             the_max = max(lc.amount_of_raw(nsse), rc.amount_of_raw(nsse))
        #             the_gcd = gcd(lc.amount_of_raw(nsse), rc.amount_of_raw(nsse))
        #             lc.coefficient

    
    def readable(self) -> str:
        return f"{self.left.readable()} => {self.right.readable()}"

    def __str__(self) -> str:
        return f"{self.left} => {self.right}"

def parse_input(inp: str):
    assert inp.find("=>") != -1
    sides_str = inp[:inp.find("=>")], inp[inp.find("=>")+2:]
    chem_equat = ChemicalEquation()
    for side_str in sides_str:
        side = Side()
        for compound_str in side_str.split("+"):
            compound = Compound()
            symbol = ""
            quantity = ""
            for i, char in enumerate(compound_str):
                if char.isalpha():
                    if char.isupper() and i > 0:
                        compound.add_element(symbol, int(quantity) if len(quantity) > 0 else 1)
                        symbol = ""
                        quantity = ""
                    symbol += char
                elif char.isdigit():
                    quantity += char
                else:
                    raise Exception(f"Invalid character: {char}")
            compound.add_element(symbol, int(quantity) if len(quantity) > 0 else 1)
            side.add_compound(compound)
        chem_equat.add_side(side)
    return chem_equat

def main():
    global ce1, ce2, ce3, ce4
    inp = "C3H8+O2=>H2O+CO2"
    ce1 = parse_input(inp)
    # print(ce1)
    # print(ce1.left.totals())
    # print(ce1.right.totals())
    ce1.balance()
    print(ce1.readable())
    print("----------")
    inp = "C3H7+O2=>H2O+CO2"
    ce2 = parse_input(inp)
    # print(ce2)
    # print(ce2.left.totals())
    # print(ce2.right.totals())
    ce2.balance()
    print(ce2.readable())
    print("----------")
    inp = "Ag2S=>Ag+S8"
    ce3 = parse_input(inp)
    # print(ce3)
    # print(ce3.left.totals())
    # print(ce3.right.totals())
    ce3.balance()
    print(ce3.readable())
    print("----------")
    inp = "C12H22O11+O2=>CO2+H2O"
    ce4 = parse_input(inp)
    # print(ce4)
    # print(ce4.left.totals())
    # print(ce4.right.totals())
    ce4.balance()
    print(ce4.readable())

if __name__  == "__main__":
    main()
