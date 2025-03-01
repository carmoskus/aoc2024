
import re

in_re = r"""
Register A: (\d+)
Register B: (\d+)
Register C: (\d+)
*
Program: ([0-9,]+)
""".strip()

in_txt = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".strip()

in_txt = open('data/day17_input.txt').read()

re.search(in_re, in_txt).groups()

class Mach:
    def __init__(self, in_txt):
        m = re.search(in_re, in_txt).groups()
        self.a = int(m[0])
        self.b = int(m[1])
        self.c = int(m[2])
        self.prog = [int(x) for x in m[3].split(",")]
        self.idx = 0

    def combo(self, x):
        match x:
            case 4: return self.a
            case 5: return self.b
            case 6: return self.c
        return x
    
    def step(self):
        op = self.prog[self.idx]
        opd = self.prog[self.idx+1]
        self.idx += 2

        match op:
            case 0:
                num = self.a
                denom = 2**self.combo(opd)
                self.a = num // denom
            case 1:
                self.b = self.b ^ opd
            case 2:
                self.b = self.combo(opd) % 8
            case 3:
                if self.a != 0:
                    self.idx = opd
            case 4:
                self.b = self.b ^ self.c
            case 5:
                res = self.combo(opd) % 8
                return res
            case 6:
                num = self.a
                denom = 2**self.combo(opd)
                self.b = num // denom
            case 7:
                num = self.a
                denom = 2**self.combo(opd)
                self.c = num // denom

    def go(self, max_steps = int(1e6)):
        res = []
        for i in range(max_steps):
            try:
                o = self.step()
                if o is not None:
                    res.append(o)
            except:
                return res
    pass

m = Mach(in_txt)

res = m.go()
res
','.join(str(x) for x in res)
