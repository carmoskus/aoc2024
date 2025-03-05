
import pandas as pd
import functools, itertools, collections

def map_from_txt(txt):
    return pd.DataFrame([list(x) for x in txt.split("\n")])
def num_loc(c):
    i = num_map.eq(c).idxmax(axis=0).max()
    j = num_map.eq(c).idxmax(axis=1).max()
    return i, j
def dir_loc(c):
    i = dir_map.eq(c).idxmax(axis=0).max()
    j = dir_map.eq(c).idxmax(axis=1).max()
    return i, j
def valid_num_map(i, j):
    if i < 0 or j < 0 or i >= num_map.shape[0] or j >= num_map.shape[1]:
        return False
    return num_map.iat[i, j] != '#'
def valid_dir_map(i, j):
    if i < 0 or j < 0 or i >= dir_map.shape[0] or j >= dir_map.shape[1]:
        return False
    return dir_map.iat[i, j] != '#'
def comb_paths(paths):
    foo = [range(len(x)) for x in paths]
    outs = []
    for idxs in itertools.product(*foo):
        res = ""
        for i, j in enumerate(idxs):
            res += paths[i][j]
        outs.append(res)
    return outs
def num_paths_between(a, b):
    si, sj = a
    ei, ej = b
    di = ei - si
    dj = ej - sj
    opts = []
    if di == 0 and dj == 0:
        # We're here
        return ["A"]
    if di < 0 and valid_num_map(si-1, sj):
        opts += ['^' + x for x in num_paths_between((si-1, sj), b)]
    if di > 0 and valid_num_map(si+1, sj):
        opts += ['v' + x for x in num_paths_between((si+1, sj), b)]
    if dj < 0 and valid_num_map(si, sj-1):
        opts += ['<' + x for x in num_paths_between((si, sj-1), b)]
    if dj > 0 and valid_num_map(si, sj+1):
        opts += ['>' + x for x in num_paths_between((si, sj+1), b)]
    return opts
def dir_paths_between(a, b):
    si, sj = a
    ei, ej = b
    di = ei - si
    dj = ej - sj
    opts = []
    if di == 0 and dj == 0:
        # We're here
        return ["A"]
    if di < 0 and valid_dir_map(si-1, sj):
        opts += ['^' + x for x in dir_paths_between((si-1, sj), b)]
    if di > 0 and valid_dir_map(si+1, sj):
        opts += ['v' + x for x in dir_paths_between((si+1, sj), b)]
    if dj < 0 and valid_dir_map(si, sj-1):
        opts += ['<' + x for x in dir_paths_between((si, sj-1), b)]
    if dj > 0 and valid_dir_map(si, sj+1):
        opts += ['>' + x for x in dir_paths_between((si, sj+1), b)]
    return opts
def num_to_dirs(num_txt):
    start = num_loc('A')
    paths = []
    for c in num_txt:
        cur = num_loc(c)
        res = num_paths_between(start, cur)
        start = cur
        paths.append(res)
    return paths
def dir_to_dirs(dir_txt):
    start = dir_loc('A')
    paths = []
    for c in dir_txt:
        cur = dir_loc(c)
        res = dir_paths_between(start, cur)
        start = cur
        paths.append(res)
    return paths
def user_cmd(num_txt):
    paths1 = comb_paths(num_to_dirs(num_txt))
    min1 = min(len(p) for p in paths1)
    paths1 = [p for p in paths1 if len(p) == min1]

    paths2 = [comb_paths(dir_to_dirs(x)) for x in paths1]
    paths2 = functools.reduce(set.union, (set(x) for x in paths2))
    min2 = min(len(p) for p in paths2)
    paths2 = [p for p in paths2 if len(p) == min2]

    paths3 = [comb_paths(dir_to_dirs(x)) for x in paths2]
    paths3 = functools.reduce(set.union, (set(x) for x in paths3))
    min3 = min(len(p) for p in paths3)
    paths3 = [p for p in paths3 if len(p) == min3]

    return paths3

#
num_map_txt = """
789
456
123
#0A
""".strip()
dir_map_txt = """
#^A
<v>
""".strip()
num_map = map_from_txt(num_map_txt)
dir_map = map_from_txt(dir_map_txt)

#
in_txt = """
029A
980A
179A
456A
379A
""".strip()

in_txt = """
341A
480A
286A
579A
149A
""".strip()

#
in1 = [x for x in in_txt.split("\n")]

# Test code
# u1 = user_cmd('029A')
# "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A" in u1
# u2 = user_cmd('980A')
# "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A" in u2
# u3 = user_cmd('179A')
# "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A" in u3
# u4 = user_cmd('456A')
# "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A" in u4
# u5 = user_cmd('379A')
# "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A" in u5

#
res1 = [user_cmd(x) for x in in1]
res2 = [len(next(iter(x))) for x in res1]
res3 = [int(x[:-1]) for x in in1]
sum(a*b for a,b in zip(res2, res3))
