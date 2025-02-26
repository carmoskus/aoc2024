
import pandas as pd
import functools

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

in_txt = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
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
            sites = mk_sites(i, j)
            n = [check_site(m1, i, j, '#') for i, j in sites]
            if sum(n) >= 3:
                m1.iat[i, j] = '#'
    if m1.equals(map_in):
        return m1
    return fill_map(m1)

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
def sym_to_vec(sym):
    if sym == '<':
        return 0, -1
    if sym == '>':
        return 0, 1
    if sym == '^':
        return -1, 0
    if sym == 'v':
        return 1, 0
def sym_dist(s1, s2):
    if s1 == s2:
        return 0
    if s1 == '<' and s2 == '>':
        return 2000
    if s1 == '^' and s2 == 'v':
        return 2000
    return 1000
def rot_left(s):
    if s == '<':
        return 'v'
    if s == 'v':
        return '>'
    if s == '>':
        return '^'
    if s == '^':
        return '<'
def rot_right(s):
    if s == '<':
        return '^'
    if s == '^':
        return '>'
    if s == '>':
        return 'v'
    if s == 'v':
        return '<'
    
def progress(m1, si, sj, sk, d=0):
    opts = check_neighbors(m1, si, sj)
    if len(opts) == 1:
        # One option, take the next step
        i, j = opts[0]
        c = get_sym(i-si, j-sj)
        m1.iat[si, sj] = c
        return progress(m1, i, j, c, d+1+sym_dist(sk, c))
    # Multiple options
    return si, sj, sk, d

def find_nodes(m1, node):
    df = m1.copy()
    si = node[0]
    sj = node[1]
    sk = node[2]
    di, dj = sym_to_vec(sk)
    df.iat[si, sj] = '@'
    res = [(si, sj, rot_left(sk), 1000), (si, sj, rot_right(sk), 1000)]
    if check_site(df, si+di, sj+dj, '.'):
        # Continue forward
        res.append(progress(df, si+di, sj+dj, sk, 1))
    return res

def map_nodes(df):
    df = df.copy()
    si = df.eq('S').idxmax(axis=1).idxmax()
    sj = df.eq('S').idxmax(axis=0).idxmax()
    sk = '>'
    nodes = {}
    nodes_to_check = {(si, sj, sk)}
    df.iat[si, sj] = "."
    
    while len(nodes_to_check) > 0:
        node = next(iter(nodes_to_check))
        nodes_to_check.remove(node)
        new_nodes = find_nodes(df, node)
        nodes[node] = new_nodes
        new_node_locs = {(i, j, k) for i, j, k, d in new_nodes if (i, j, k) not in nodes}
        nodes_to_check.update(new_node_locs)

    # Final nodes linking to end_node
    ei = df.eq('E').idxmax(axis=1).idxmax()
    ej = df.eq('E').idxmax(axis=0).idxmax()
    res = check_neighbors(df, ei, ej)
    for i, j in res:
        di = ei - i
        dj = ej - j
        k = get_sym(di, dj)
        opts = nodes.get((i, j, k), [])
        opts.append((ei, ej, k, 1))
        nodes[(i, j, k)] = opts
    for k in ['<', '>', 'v', '^']:
        nodes[(ei, ej, k)] = [(ei, ej, rot_left(k), 1000), (ei, ej, rot_right(k), 1000)]

    return nodes

def check_path(nodes, path):
    nodes_seen = set(path)
    # for i, j, k in path[:-1]:
    #     nodes_seen.update({(i, j, k) for i, j, k, d in nodes[(i, j, k)]})

    res = [(i, j, k, d) for i, j, k, d in nodes[path[-1]] if (i, j, k) not in nodes_seen]
    return res
def path_len(path):
    res = sum(node[3] for node in path)
    return res

def find_path(nodes, path, end_node):
    if path[-1] == end_node:
        return []
    res = check_path(nodes, path)
    # print("--", path, res)
    if res is None or len(res) == 0:
        return
    if len(res) == 1:
        # We now have a path of length 'd'
        # That goes from (si, sj) to (i, j)
        i, j, k, d = res[0]
        # Extend this to find the path from (i, j) to (ei, ej)
        con = find_path(nodes, path + [(i, j, k)], end_node)
        if con is None:
            return
        return [(i, j, k, d)] + con
    # This means we have multiple next options
    # Look at each potential path 
    # res_dict = {(i, j, k): d for i, j, k, d in res}
    # recur_res = []
    # if end_node in res_dict:
    #     recur_res.append([end_node + (res_dict[end_node],)])

    recur_res = [find_path(nodes, path + [(i, j, k)], end_node) for i, j, k, d in res]
    # print('-', path[-1], res, recur_res)
    min_val = 99999999999
    min_path = None
    for p1, p2 in zip(res, recur_res):
        if p2 is None:
            continue
        if p1[3] + path_len(p2) < min_val:
            min_val = p1[3] + path_len(p2)
            min_path = [p1] + p2
    return min_path

# find_path is picking
# (5, 1, ^) (5, 3, v, 2010) = 2010
# instead of
# (5, 1, ^) (5, 1, >, 1000) (5, 3, >, 2) (5, 3, v, 1000) = 2002
_=find_path(nodes, [(5, 1, '^')], (5, 3, 'v'))

check_path(nodes, [(5, 1, '^')])
check_path(nodes, [(5, 1, '^'), (5, 1, '>'), (5, 3, '>')])
_=find_path(nodes, [(5, 1, '^')], (5, 1, '>'))

#
in1 = parse_map(in_txt)
in2 = fill_map(in1)
nodes = map_nodes(in2)

in1
in2

#
si = in2.eq('S').idxmax(axis=1).idxmax()
sj = in2.eq('S').idxmax(axis=0).idxmax()
sk = '>'
ei = in2.eq('E').idxmax(axis=1).idxmax()
ej = in2.eq('E').idxmax(axis=0).idxmax()

paths = [find_path(nodes, [(si, sj, sk)], (ei, ej, k)) for k in ['^', '>']]
path_lens = [path_len(p) for p in paths]

path_lens
path_lens[pd.Series(path_lens).idxmin()]

paths[pd.Series(path_lens).idxmin()]

#
nodes[(5, 1, '^')]
nodes[(5, 1, '>')]

nodes[(5, 3, '^')]
nodes[(13, 5, '^')]


#
[node
 for node in set(functools.reduce(list.__add__, nodes.values()))
 if node[0] == 1 and node[1] == 13]

a = find_path(nodes, [(13, 1, '>')], (1, 13, '>'))
b = find_path(nodes, [(13, 1, '>')], (1, 13, '^'))
path_len(a)
path_len(b)
a
