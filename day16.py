
import pandas as pd

in_txt = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".strip()

def parse_map(map_str):
    return pd.DataFrame([list(x) for x in in_txt.split("\n")])
def check_site(m, i, j, c):
    if i < 0 or j < 0 or i >= m.shape[0] or j >= m.shape[1]:
        return False
    return m.iat[i, j] == c
def mk_sites(i, j):
    return [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
def fill_map(map_in):
    m1 = map_in.copy()
    for i in range(m1.shape[0]):
        for j in range(m1.shape[1]):
            if m1.iat[i, j] != ".":
                continue
            sites = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            n = [check_site(m1, i, j, '#') for i, j in sites]
            if sum(n) >= 3:
                m1.iat[i, j] = '#'
    if m1.equals(map_in):
        return m1
    return fill_map(m1)

in1 = parse_map(in_txt)

in2 = fill_map(in1)

in1
in2

def check_neighbors(m1, si, sj):
    return [(i, j) for i, j in mk_sites(si, sj) if check_site(m1, i, j, '.')]

def get_sym(di, dj):
    if di == 0:
        if dj < 0:
            return '<'
        else:
            return '>'
    else:
        if di > 0:
            return 'v'
        else:
            return '^'

def progress(m1, si, sj, d=0):
    opts = check_neighbors(m1, si, sj)
    if len(opts) == 1:
        # One option, take the next step
        i, j = opts[0]
        c = get_sym(i-si, j-sj)
        m1.iat[si, sj] = c
        return progress(m1, i, j, d+1)
    # Multiple options
    return si, sj, d

def find_nodes(m1, si, sj):
    df = m1.copy()
    df.iat[si, sj] = '@'
    opts = check_neighbors(df, si, sj)
    res = [progress(df, i, j, 1) for i, j in opts]
    return res

si = in2.eq('S').idxmax(axis=1).idxmax()
sj = in2.eq('S').idxmax(axis=0).idxmax()
ei = in2.eq('E').idxmax(axis=1).idxmax()
ej = in2.eq('E').idxmax(axis=0).idxmax()

df = in2.copy()
nodes_checked = {}
nodes_from = {}
# nodes_to_check = {(df.eq('S').idxmax(axis=1).idxmax(), df.eq('S').idxmax(axis=0).idxmax())}
df.iat[si, sj] = "."
# df.iat[ei, ej] = "."
nodes_to_check = {(si, sj)}
while len(nodes_to_check) > 0:
    node = next(iter(nodes_to_check))
    nodes_to_check.remove(node)
    new_nodes = find_nodes(df, node[0], node[1])
    nodes_checked[node] = new_nodes
    for i, j, d in new_nodes:
        nodes_from[(i, j)] = (node[0], node[1], d)
    new_nodes = {(i, j) for i, j, d in new_nodes if (i, j) not in nodes_checked}
    nodes_to_check.update(new_nodes)

nodes_checked
nodes_from

(si, sj)
(ei, ej)

# From start
nodes_checked[(13, 1)]
nodes_checked[(11, 1)] # 3 opts, inc loop

nodes_checked[(9, 3)]
nodes_checked[(11, 3)]

def check_path(nodes, path):
    nodes_seen = set(path)
    for i, j in path[:-1]:
        nodes_seen.update({(i, j) for i, j, d in nodes[(i, j)]})

    res = [(i, j, d) for i, j, d in nodes[path[-1]] if (i, j) not in nodes_seen]
    return res

check_path(nodes_checked, [(13, 1)])
check_path(nodes_checked, [(13, 1), (11, 1)])

# First branch gives two
check_path(nodes_checked, [(13, 1), (11, 1), (9, 3)])
check_path(nodes_checked, [(13, 1), (11, 1), (11, 3)])

# Direct extension of previous two after redundant options eliminated
check_path(nodes_checked, [(13, 1), (11, 1), (9, 3), (7, 3)])
check_path(nodes_checked, [(13, 1), (11, 1), (11, 3), (11, 5)])

def path_len(path):
    res = sum(d for i, j, d in path)
    return res
def find_path(nodes, path, ei, ej):
    si, sj = path[-1]
    if si == ei and sj == ej:
        return []
    res = check_path(nodes, path)
    if res is None or len(res) == 0:
        return
    if len(res) == 1:
        # We now have a path of length 'd'
        # That goes from (si, sj) to (i, j)
        i, j, d = res[0]
        # Extend this to find the path from (i, j) to (ei, ej)
        con = find_path(nodes, path + [(i, j)], ei, ej)
        if con is None:
            return
        return [(i, j, d)] + con
    # This means we have multiple next options
    # Look at each potential path 
    res_dict = {(i, j): d for i, j, d in res}
    if (ei, ej) in res_dict:
        return [(ei, ej, res_dict[(ei, ej)])]

    recur_res = [find_path(nodes, path + [(i, j)], ei, ej) for i, j, d in res]
    min_val = 99999999999
    min_path = None
    for p1, p2 in zip(res, recur_res):
        if p2 is None:
            continue
        if p1[2] + path_len(p2) < min_val:
            min_val = p1[2] + path_len(p2)
            min_path = [p1] + p2
    return min_path

find_path(nodes_checked, [(13, 1)], 1, 13)
a = find_path(nodes_checked, [(13, 1)], 1, 12)
b = find_path(nodes_checked, [(13, 1)], 2, 13)
path_len(a)
path_len(b)
a

check_path(nodes_checked, [(13, 1), (11, 1)])
check_path(nodes_checked, [(13, 1), (11, 1), (11, 3)])


find_path(nodes_checked, [(13, 1)], 11, 1)
find_path(nodes_checked, [(13, 1), (11, 1)], 11, 3)
find_path(nodes_checked, [(13, 1), (11, 1), (11, 3)], 11, 5)
