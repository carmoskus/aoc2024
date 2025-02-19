
import pandas as pd

in_txt = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()

in_txt = open('data/day10_input.txt').read().strip()

in1 = pd.DataFrame([[int(y) for y in x] for x in in_txt.split("\n")])
in1

long1 = pd.melt(in1.assign(r=lambda x: x.index), id_vars='r', var_name='c')
long1 = long1[long1.value == 0].drop('value', axis=1).sort_values(['r', 'c'])
long1

def check_loc(i, j, x):
    if i < 0 or j < 0 or i >= in1.shape[0] or j >= in1.shape[1]:
        return False
    return in1.iat[i, j] == x

def count_ends(i, j):
    cur = in1.iat[i, j]
    if cur == 9:
        return {(i, j)}
    res = set()
    if check_loc(i+1, j, cur+1):
        res.update(count_ends(i+1, j))
    if check_loc(i-1, j, cur+1):
        res.update(count_ends(i-1, j))
    if check_loc(i, j+1, cur+1):
        res.update(count_ends(i, j+1))
    if check_loc(i, j-1, cur+1):
        res.update(count_ends(i, j-1))
    return res

def count_paths(i, j):
    cur = in1.iat[i, j]
    if cur == 9:
        return 1
    res = 0
    if check_loc(i+1, j, cur+1):
        res += count_paths(i+1, j)
    if check_loc(i-1, j, cur+1):
        res += count_paths(i-1, j)
    if check_loc(i, j+1, cur+1):
        res += count_paths(i, j+1)
    if check_loc(i, j-1, cur+1):
        res += count_paths(i, j-1)
    return res

res1 = [count_ends(x.r, x.c) for i, x in long1.iterrows()]
[len(x) for x in res1]
sum(len(x) for x in res1)

res2 = [count_paths(x.r, x.c) for i, x in long1.iterrows()]
sum(res2)
