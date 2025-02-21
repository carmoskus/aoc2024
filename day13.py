
import re

# Intersect two lines
# One comes from 0,0 at a slope of A
# y = ady/adx*x
# The other comes from ox,oy (target loc) at a slope of B
# y - oy = bdy/bdx*(x - ox)
# Intersect
# ady/adx * x = bdy/bdx*(x - ox) + oy
# ady/adx * x = bdy/bdx * x - bdy/bdx * ox + oy
# x * (ady/adx - bdy/bdx) = oy - bdy/bdx * ox
# x = (oy - bdy/bdx * ox) / (ady/adx - bdy/bdx)
# If intersection is integer units from each endpoint, that is result
#
# Try a manual, integer-based intersection using sets instead?

def check_int(params, shift=0):
    adx = params[0]
    ady = params[1]
    bdx = params[2]
    bdy = params[3]
    ox = params[4] + shift
    oy = params[5] + shift

    x = (oy - bdy/bdx * ox) / (ady/adx - bdy/bdx)
    # y = (ady/adx * x)

    a1 = x / adx
    ia1 = round(a1)
    b1 = (ox - x) / bdx
    ib1 = round(b1)
    
    if ia1*adx + ib1*bdx == ox and ia1*ady + ib1*bdy == oy:
        return ia1, ib1


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

res1 = [check_int(x) for x in in1]
res1

sum(1 for x in res1 if x is not None)
sum(x[0]*3 + x[1] for x in res1 if x is not None)

# Part 2
res2 = [check_int(x, 10000000000000) for x in in1]
res2

sum(1 for x in res2 if x is not None)
sum(x[0]*3 + x[1] for x in res2 if x is not None)
