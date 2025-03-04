
import re, collections, functools

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

in_txt = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".strip()

in_txt = open('data/day17_input.txt').read()

class Mach:
    def __init__(self, in_txt):
        m = re.search(in_re, in_txt).groups()
        self.a_start = int(m[0])
        self.b_start = int(m[1])
        self.c_start = int(m[2])
        self.prog = [int(x) for x in m[3].split(",")]
        self.reset()

    def reset(self):
        self.a = self.a_start
        self.c = self.b_start
        self.c = self.c_start
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

    def go(self, new_a = None, max_steps = int(1e7)):
        self.reset()
        if new_a is not None:
            self.a = new_a
        res = []
        for i in range(max_steps):
            try:
                o = self.step()
                if o is not None:
                    res.append(o)
            except IndexError:
                return res
    def search(self, start = 1, stop = int(8e8), max_steps = int(1e8)):
        for a in range(start, stop):
            self.reset()
            self.a = a
            res = []
            for i in range(max_steps):
                try:
                    o = self.step()
                    if o is not None:
                        res.append(o)
                        if len(res) > len(self.prog):
                            break
                        if res[-1] != self.prog[len(res)-1]:
                            break
                        # if len(res) == len(self.prog):
                        #     break
                except IndexError:
                    break
            # Check res
            if len(res) > len(self.prog):
                continue
            if res == self.prog:
                return a

    pass

m = Mach(in_txt)

# Program: 2,4,1,1,7,5,4,7,1,4,0,3,5,5,3,0
# 2,4  1,1  7,5  4,7  1,4  0,3  5,5  3,0
#
# bst c(4) = bst A      Put last 3 bits of A in B
# bxl 1                 Flip last bit of B
# cdv c(5) = cdv B      Put A / 2^B in C
# bxc                   Put B ^ C in B
# bxl 4                 Put B ^ 4 in B
# adv c(3) = adv 3      Put A / 2^3 in A
# out c(5) = out B      Print B
# jnz 0                 Loop if A isn't 0
#
# 16 outputs needs 1e15 in octal
a = 0o1000000000000000
b = 0o10000000000000000

print(m.go(5*a+6*a//8))
print(m.go(5*a+7*a//8-1))

print(m.go(5*a + 6*a//8 + 19*a//1024 + 13*a//16192))
for i in range(32):
    print(i, m.go(5*a + 6*a//8 + 19*a//1024 + 13*a//16192 + i*a//518144))

# 1-7: 1 output = 1e0
# 10-77: 2 outputs = 1e1
# 100-777: 3 outputs = 1e2
#
# Last digit goes 5, 7, 6, 1, 0, 3, 2
# 5a ends with 0
# (5 + 24/32)*a through (5 + 27/32)*a has 3 almost last
#
y = None
for i in range(5*a, 6*a, a//64):
    x = m.go(i)
    if x is not None:
        if x != y:
            y = x
            print(oct(i), ",".join(str(y) for y in x))

res = m.go()
res
','.join(str(x) for x in res)

def match_end(m, start, stop, n):
    matches = []
    for i in range(start, stop, (stop-start)//64):
        res = m.go(i)
        if res[-n:] == m.prog[-n:]:
            matches.append(i)
    return matches
def find_match(m, n, start, stop, step):
    begin = end = None
    going = False
    for i in range(start, stop, step):
        res = m.go(i)
        if res is not None and res[-n:] == m.prog[-n:]:
            if not going:
                begin = i
                going = True
        elif going:
            end = i
            going = False
            return begin, end
def find_matches(m, n, start, stop):
    step = 8**max(1, n-1)
    begin = end = None
    going = False
    ranges = []
    for i in range(start, stop, step):
        res = m.go(i)
        if res is not None and res[n:] == m.prog[n:]:
            if not going:
                begin = i
                going = True
        elif going:
            end = i
            going = False
            ranges.append((begin, end))
    if going:
        end = i
        going = False
        ranges.append((begin, end))
    return ranges

find_matches(m, 15, a, b)
find_matches(m, 14, 175921860444160, 211106232532992)
find_matches(m, 13, 202310139510784, 206708186021888)
foo = find_matches(m, 12, 202310139510784, 203409651138560)
bar = functools.reduce(list.__add__, (find_matches(m, 11, x[0], x[1]) for x in foo))
for x in bar:
    print(find_matches(m, 10, x[0], x[1]))
find_matches(m, 9, 202365974085632, 202367047827456)
find_matches(m, 9, 202640851992576, 202641925734400)

opts = [(a, b)]
for i in range(15, -1, -1):
    new_opts = functools.reduce(list.__add__, (
        find_matches(m, i, x[0], x[1]) for x in opts))
    if len(new_opts) == 0:
        break
    opts = new_opts

i
opts

for x in opts:
    print(m.go(x[0]))
    print(m.go(x[1]-1))

for i in range(opts[0][0], opts[0][1]):
    print(m.go(i))

m.go(opts[0][0]+2)
m.go(opts[0][0]+2) == m.prog
opts[0][0]+2

find_matches(m, 8, 203191245340672, 203191262117888)
find_matches(m, 8, 203191245340672, 203191245340672)

m.go(opts[0][0])
m.go(opts[0][1]-1)
m.go(opts[1][0])
