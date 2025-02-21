
import pandas as pd
import re, time

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

#
def safety_gen(my_in):
    i = 0
    while True:
        res1 = [advance(x, i) for x in my_in]
        res2 = [quad(x, y) for x, y in res1]
        res3 = pd.Series(res2).value_counts()
        yield res3.drop(0).prod()
        i += 1

g = safety_gen(in1)
res4 = [next(g) for i in range(10000)]

min(res4[:1000])
res4.index(min(res4[:1000]))
res4[369:374]

min(res4)
res4.index(min(res4))
res4[1378:1384]

min(res4[1400:])
res4.index(min(res4[1400:]))
res4[1480:1486]

def mk_pic(my_in, n):
    res = [advance(x, n) for x in my_in]
    pic1 = pd.DataFrame([["." for i in range(nx)] for j in range(ny)])
    for x, y in res:
        c = pic1.iat[y, x]
        if c == ".":
            pic1.iat[y, x] = '1'
        else:
            pic1.iat[y, x] = str(int(pic1.iat[y, x])+1)
    pic1.columns = ["" for i in range(pic1.shape[1])]
    pic1.index = ["" for i in range(pic1.shape[0])]

    return "\n".join("".join(pic1.iat[y, x] for x in range(pic1.shape[1])) for y in range(pic1.shape[0]))

print(mk_pic(in1, 6532))

res4[:100]
res4[67:70]

foo = pd.Series(res4)
foo[foo < 120000000][:20]

for i in foo[foo < 120000000].index[20:30]:
    print(i)
    print(mk_pic(in1, i))
    time.sleep(0.4)
