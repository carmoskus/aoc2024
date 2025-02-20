
import pandas as pd
import functools

def check_site(i, j, c):
    if i < 0 or j < 0 or i >= in1.shape[0] or j >= in1.shape[1]:
        return 1
    return int(in1.iat[i, j] != c)
def check_site2(i, j, c):
    if i < 0 or j < 0 or i >= in2.shape[0] or j >= in2.shape[1]:
        return False
    return in2.iat[i, j] == c
def count_perim(i, j):
    cur = in1.iat[i, j]
    return check_site(i-1, j, cur) + \
            check_site(i+1, j, cur) + \
            check_site(i, j-1, cur) + \
            check_site(i, j+1, cur)
def calc_perim(c):
    block = long1[long1.value == c]
    perim = 0
    for i, x in block.iterrows():
        perim += count_perim(x.r, x.c)
    return perim
def calc_perim2(c):
    block = long2[long2.value == c]
    perim = 0
    for i, x in block.iterrows():
        perim += count_perim(x.r, x.c)
    return perim
def update_from(i: int, j: int, c: str):
    cur = in2.iat[i, j]
    in2.iat[i, j] = c
    if check_site2(i-1, j, cur):
        update_from(i-1, j, c)
    if check_site2(i+1, j, cur):
        update_from(i+1, j, c)
    if check_site2(i, j-1, cur):
        update_from(i, j-1, c)
    if check_site2(i, j+1, cur):
        update_from(i, j+1, c)

def calc_sides(i, j):
    c = in2.iat[i, j]
    sides = set()
    if not check_site2(i-1, j, c):
        # If we're blocked off, then this is a side
        sides.add((0, i-1, j))
    if not check_site2(i+1, j, c):
        sides.add((1, i+1, j))
    if not check_site2(i, j-1, c):
        sides.add((2, i, j-1))
    if not check_site2(i, j+1, c):
        sides.add((4, i, j+1))
    return sides

def reduce_sides(my_sides: set):
    out_sides = {(d, i, j) for (d, i, j) in my_sides 
                 if (d, i-1, j) not in my_sides and (d, i, j-1) not in my_sides}
    return out_sides

def calc_all_sides(c):
    block = long2[long2.value == c]
    res = [calc_sides(x.r, x.c) for i, x in block.iterrows()]
    return functools.reduce(set.union, res)


in_txt = """
AAAA
BBCD
BBCC
EEEC
""".strip()

in_txt = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""".strip()

in_txt = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""".strip()

in_txt = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""".strip()

in_txt = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()

in_txt = open('data/day12_input.txt').read()

#
in1 = pd.DataFrame([list(x) for x in in_txt.split("\n")])
in1

long1 = pd.melt(in1.assign(r=lambda x: x.index), id_vars='r', var_name='c').sort_values(['r', 'c'])
res1 = long1.value.value_counts(sort=False)
res1

in2 = in1.copy()
for v in res1.index:
    n = 1
    long2 = pd.melt(in2.assign(r=lambda x: x.index), id_vars='r', var_name='c').sort_values(['r', 'c'])
    block = long2[long2.value == v]
    while block.shape[0] > 0:
        i = block.r.iat[0]
        j = block.c.iat[0]
        update_from(i, j, v + str(n))
        long2 = pd.melt(in2.assign(r=lambda x: x.index), id_vars='r', var_name='c').sort_values(['r', 'c'])
        block = long2[long2.value == v]
        n += 1
in2

long2 = pd.melt(in2.assign(r=lambda x: x.index), id_vars='r', var_name='c'
               ).sort_values(['r', 'c'])
res2 = long2.value.value_counts(sort=False)
res2

res3 = res2.copy()
# Calculate perimeter for each area
for c, v in res3.items():
    res3.at[c] = calc_perim2(c)

res4 = pd.DataFrame({'a': res2, 'p': res3}).assign(cost = lambda x: x.a * x.p)
res4

sum(res4.cost)

# Part2
res5 = res2.copy()
# Calculate perimeter for each area
for c, v in res5.items():
    res5.at[c] = len(reduce_sides(calc_all_sides(c)))

res6 = pd.DataFrame({'a': res2, 's': res5}).assign(cost = lambda x: x.a * x.s)
res6

sum(res6.cost)
