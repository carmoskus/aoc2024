
import pandas as pd
from heapq import heappush, heappop

def print_map(df):
    print("\n".join(df.apply(lambda x: "".join(x), axis=1).to_list()))
def mk_sites(i, j):
    return [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
def check_site(m, i, j, c):
    if i < 0 or j < 0 or i >= m.shape[0] or j >= m.shape[1]:
        return False
    return m.iat[i, j] == c
def check_neighbors(m, si, sj):
    res = {(i, j) for i, j in mk_sites(si, sj) if check_site(m, i, j, '.')}
    return res
def fill_map(map_in):
    m1 = map_in.copy()
    for i in range(m1.shape[0]):
        for j in range(m1.shape[1]):
            if m1.iat[i, j] != ".":
                continue
            sites = mk_sites(i, j)
            n = [check_site(m1, i, j, '#') for i, j in sites]
            if sum(n) >= 3:
                m1.iat[i, j] = '#'
    if m1.equals(map_in):
        return m1
    return fill_map(m1)

in_txt = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip()

in_txt = open('data/day18_input.txt').read()

# Demo
nx = 7
ny = 7
nz = 12
# Real
nx = 71
ny = 71
nz = 1024

#
in1_full = [tuple(int(x) for x in y.split(",")) for y in in_txt.split("\n")]
in1 = [tuple(int(x) for x in y.split(",")) for y in in_txt.split("\n")[:nz]]

in2 = pd.DataFrame([["." for y in range(ny)] for x in range(nx)])
for x, y in in1:
    in2.iat[y, x] = "#"
print_map(in2)

in3 = fill_map(in2)
print_map(in3)

#
si = sj = 0
ei = ny - 1
ej = nx - 1

#
opts = []
heappush(opts, (0, si, sj))
dists = {(si, sj): 0}
while len(opts) > 0:
    dr, i, j = heappop(opts)
    d = dists[(i, j)]+1
    if (i, j) == (ei, ej):
        print("Success:", d-1)
    for x in mk_sites(i, j):
        if not check_site(in3, x[0], x[1], "."):
            continue
        if x not in dists:
            dists[x] = d
            heappush(opts, (-i-j, x[0], x[1]))
        elif d < dists[x]:
            dists[x] = d
            heappush(opts, (-i-j, x[0], x[1]))
