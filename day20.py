
import pandas as pd
from heapq import heappush, heappop
import collections, itertools

def print_map(df):
    print("\n".join(df.apply(lambda x: "".join(x), axis=1).to_list()))
def mk_sites(i, j):
    return [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
def mk_sites2(i, j):
    return [(i-2, j), (i+2, j), (i, j-2), (i, j+2)]
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
            n = [not check_site(m1, i, j, '.') for i, j in mk_sites(i, j)]
            if sum(n) > 3 or (sum(n) == 3 and ((i, j) == (0, 0) or (i, j) == (ny-1, nx-1))):
                m1.iat[i, j] = '#'
    if m1.equals(map_in):
        return m1
    return fill_map(m1)
def progress(m, si, sj):
    m = m.copy()
    i, j = si, sj
    d = 0
    seen = set()
    dists = {}
    while True:
        m.iat[i, j] = "O"
        dists[(i, j)] = d
        opts = check_neighbors(m, i, j).difference(seen)
        if len(opts) == 1:
            seen.add((i, j))
            i, j = next(iter(opts))
            d += 1
            continue
        break
    return i, j, dists, m
def find_jumps(m, si, sj):
    diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    opts = [(di, dj) for di, dj in diffs if check_site(m, si+di, sj+dj, '#')]
    outs = []
    for di, dj in opts:
        i = si+2*di
        j = sj+2*dj
        if check_site(m, i, j, "."):
            outs.append((i, j))
    return outs
def find_shortcuts(dists, m, si, sj):
    i, j = si, sj
    seen = set()
    shorts = []
    while True:
        # Check for places to jump to
        opts = find_jumps(m, i, j)
        sd = dists[(i, j)]
        for ei, ej in opts:
            ed = dists[(ei, ej)]
            if ed - sd > 2:
                # Shortcut
                shorts.append((i, j, ei, ej, ed-sd-2))
        # Move forward normally
        opts = check_neighbors(m, i, j).difference(seen)
        if len(opts) != 1:
            break
        seen.add((i, j))
        i, j = next(iter(opts))
    return shorts

in_txt = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip()

in_txt = open('data/day20_input.txt').read()

#
in1 = pd.DataFrame([list(x) for x in in_txt.split("\n")])

si = in1.eq('S').idxmax(axis=1).idxmax()
sj = in1.eq('S').idxmax(axis=0).idxmax()
ei = in1.eq('E').idxmax(axis=1).idxmax()
ej = in1.eq('E').idxmax(axis=0).idxmax()

in2 = in1.copy()
in2.iat[si, sj] = "."
in2.iat[ei, ej] = "."
in2

# Check that there is only a single path from start to end
fin = progress(in2, si, sj)
fin[:2] == (ei, ej)
fin[3]

# Distance
fin[2][(ei, ej)]

# And that it covers everything
fin[3].eq('.').sum().sum()

shorts = find_shortcuts(fin[2], in2, si, sj)
#collections.Counter(d for i1, j1, i2, j2, d in shorts)
sum(1 for i1, j1, i2, j2, d in shorts if d >= 100)

#
max_phase = 20
def all_shortcuts(dists, m, si, sj):
    i, j = si, sj
    seen = set()
    shorts = set()
    while True:
        # Check for places to jump to
        sd = dists[(i, j)]
        for di in range(-max_phase, max_phase+1):
            for dj in range(-max_phase+abs(di), max_phase+1-abs(di)):
                if not check_site(m, i+di, j+dj, "."):
                    continue
                ed = dists[(i+di, j+dj)]
                pd = abs(di)+abs(dj)
                if ed - sd > pd:
                    shorts.add((i, j, i+di, j+dj, ed-sd-pd))
        # Move forward normally
        opts = check_neighbors(m, i, j).difference(seen)
        if len(opts) != 1:
            break
        seen.add((i, j))
        i, j = next(iter(opts))
    return shorts

all_shorts = all_shortcuts(fin[2], in2, si, sj)
# collections.Counter(d for i1, j1, i2, j2, d in all_shorts if d >= 50)
sum(1 for i1, j1, i2, j2, d in all_shorts if d >= 100)
