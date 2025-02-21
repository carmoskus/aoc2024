
import pandas as pd
import re

in_re = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"

in_txt = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()

in_txt = open('data/day14_input.txt').read()

in1 = [tuple(int(x) for x in y) for y in re.findall(in_re, in_txt)]

# The robots outside the actual bathroom are in a space which is 
# 101 tiles wide and 103 tiles tall (when viewed from above).
# However, in this example, the robots are in a space which is 
# only 11 tiles wide and 7 tiles tall.
# nx = 11
# ny = 7
nx = 101
ny = 103

def advance(params, turns):
    x = (params[0] + params[2] * turns) % nx
    y = (params[1] + params[3] * turns) % ny
    return x, y

def quad(x, y):
    if x == nx // 2:
        sx = 0
    elif x < nx // 2:
        sx = -1
    else:
        sx = 1
    if y == ny // 2:
        sy = 0
    elif y < ny // 2:
        sy = -1
    else:
        sy = 1
    if sx < 0 and sy < 0:
        return 1
    if sx < 0 and sy > 0:
        return 2
    if sx > 0 and sy < 0:
        return 3
    if sx > 0 and sy > 0:
        return 4
    return 0

res1 = [advance(x, 100) for x in in1]
res1

res2 = [quad(x, y) for x, y in res1]
res3 = pd.Series(res2).value_counts()

res3
res3.drop(0).prod()
