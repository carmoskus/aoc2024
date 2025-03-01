
import pandas as pd
import functools, itertools

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

def print_map(df):
    print("\n".join(df.apply(lambda x: "".join(x), axis=1).to_list()))

def nodes_to_edges(nodes):
    edges = set()
    for k, v in nodes.items():
        for o in v:
            edges.add((k, o[:-1], o[-1]))
    return list(edges)
def calc_shorts(edges, start):
    dist = {start: 0}
    # Look at neighbors
    new = list(dist.keys())
    while len(new) > 0:
        cur = new.pop()
        opts = [(i, j, d) for i, j, d in edges if i == cur] + [(j, i, d) for i, j, d in edges if j == cur]
        for i, j, d in opts:
            if j not in dist:
                dist[j] = dist[cur] + d
                new.append(j)
            elif dist[j] > dist[cur] + d:
                dist[j] = dist[cur] + d
                new.append(j)
    return dist
def calc_paths(edges, mins, start):
    # Filter edges down to just those with min distance
    shorts = set()
    new = [start]
    while len(new) > 0:
        cur = new.pop()
        sub = [(a, b, d) for a, b, d in edges if a == cur] + [(b, a, d) for a, b, d in edges if b == cur]
        for a, b, d in sub:
            if d == mins[b] - mins[a]:
                shorts.add((a, b, d))
                new.append(b)
    return shorts

def min_path(edges, mins, cur, ei, ej):
    # Filter edges down to just those with min distance
    sub = [(a, b, d) for a, b, d in edges if a == cur]
    for a, b, d in sub:
        if d == mins[b] - mins[a]:
            # Potential shortest path
            if ei == b[0] and ej == b[1]:
                # Found the end
                return [(a, b, d)]
            res = min_path(edges, mins, b, ei, ej)
            if res is not None:
                return [(a, b, d)] + res
def min_path2(edges, mins, cur, ei, ej):
    # Filter edges down to just those with min distance
    sub = [(a, b, d) for a, b, d in edges if a == cur]
    sub = [(a, b, d) for a, b, d in sub if d == mins[b] - mins[a]]

    if len(sub) == 1:
        a, b, d = sub[0]
        if ei == b[0] and ej == b[1]:
            # Found the end
            return [(a, b, d)]
        res = min_path2(edges, mins, b, ei, ej)
        if res is not None:
            return [(a, b, d)] + res
    elif len(sub) > 1:
        path = []
        for a, b, d in sub:
            # Potential shortest path
            if ei == b[0] and ej == b[1]:
                # Found the end
                path.append([(a, b, d)])
                continue
            res = min_path2(edges, mins, b, ei, ej)
            if res is not None:
                path.append([(a, b, d)] + res)
        if len(path) == 1:
            return path[0]
        elif len(path) > 1:
            return path

def separate_paths(path):
    sub = []
    i = 0
    while i < len(path) and type(path[i]) == tuple:
        sub.append(path[i])
        i += 1
    if i == len(path):
        # We're done
        return sub
    opts = []
    while i < len(path):
        x = separate_paths(path[i])
        if x == path[i]:
            opts.append(sub + x)
        else:
            for y in x:
                opts.append(sub + y)
        i += 1
    return opts

def expand_path(df, path):
    df = df.copy()
    for a, b, d in path:
        i, j, k = a
        ei, ej, ek = b
        df.iat[i, j] = 'O'
        if a[:2] != b[:2]:
            # If we aren't rotating, go straight one
            di, dj = sym_to_vec(k)
            i += di
            j += dj
            df.iat[i, j] = 'O'
            if i == ei and j == ej:
                continue
        opts = check_neighbors(df, i, j)
        while len(opts) == 1:
            i, j = opts[0]
            df.iat[i, j] = 'O'
            opts = check_neighbors(df, i, j)
    return df

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

in_txt = open('data/day16_input.txt').read()

#
in1 = parse_map(in_txt)
in2 = fill_map(in1)
nodes = map_nodes(in2)
edges = nodes_to_edges(nodes)

print_map(in2)

#
si = in2.eq('S').idxmax(axis=1).idxmax()
sj = in2.eq('S').idxmax(axis=0).idxmax()
sk = '>'
ei = in2.eq('E').idxmax(axis=1).idxmax()
ej = in2.eq('E').idxmax(axis=0).idxmax()

start = (si, sj, sk)
mins = calc_shorts(edges, (si, sj, sk))
min_keys = [(i, j, k) for i, j, k in mins.keys() if i == ei and j == ej]
min(mins[x] for x in min_keys)

path = min_path(edges, mins, (si, sj, sk), ei, ej)
path2 = min_path2(edges, mins, (si, sj, sk), ei, ej)

paths = separate_paths(path2)
path_d = [sum(d for a, b, d in x) for x in paths]
path_d

min_paths = [p for p, d in zip(paths, path_d) if d == min(path_d)]

for y in min_paths:
    for x in y:
        print(x)
    print()

expand_path(in2, min_paths[0])
expand_path(in2, min_paths[1])

path_set = functools.reduce(
    set.union,
    [{(x.r, x.c)
     for x in expand_path(in2, p).eq('O').assign(r=in2.index).melt(id_vars='r', var_name='c').query('value').itertuples()}
    for p in min_paths])

len(path_set)
