
import numpy as np
import re

def check_params(params):
    a = np.array([params[0], params[1]])
    b = np.array([params[2], params[3]])
    o = np.array([params[4], params[5]])

    n_b = min(o[0] // b[0], o[1] // b[1])
    while n_b > 0:
        o2 = o - n_b * b
        if o2[0] % a[0] == 0 and o2[1] % a[1] == 0:
            n_a = o2[0] // a[0]
            if n_a == o2[1] // a[1]:
                return n_a, n_b
        n_b -= 1
    return
def check_params2(params):
    a = np.array([params[0], params[1]])
    b = np.array([params[2], params[3]])
    o = np.array([10000000000000+params[4], 10000000000000+params[5]])

    n_b = min(o[0] // b[0], o[1] // b[1])
    while n_b > 0:
        o2 = o - n_b * b
        if o2[0] % a[0] == 0 and o2[1] % a[1] == 0:
            n_a = o2[0] // a[0]
            if n_a == o2[1] // a[1]:
                return n_a, n_b
        n_b -= 1
    return


in_re = r"""
Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
""".strip()

in_txt = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()

in_txt = open('data/day13_input.txt').read()

#
in1 = [tuple(int(x) for x in y) for y in re.findall(in_re, in_txt)]
in1

res1 = [check_params(x) for x in in1]
res1

sum(1 for x in res1 if x is not None)
sum(x[0]*3 + x[1] for x in res1 if x is not None)

# Part 2
res2 = [check_params2(x) for x in in1]
res2

sum(1 for x in res1 if x is not None)
sum(x[0]*3 + x[1] for x in res1 if x is not None)
