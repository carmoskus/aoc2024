
import pandas as pd
import functools, itertools, collections

def map_from_txt(txt):
    return pd.DataFrame([list(x) for x in txt.split("\n")])

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

def map_loc(m, c):
    i = m.eq(c).idxmax(axis=0).max()
    j = m.eq(c).idxmax(axis=1).max()
    return i, j
num_loc = functools.partial(map_loc, m=num_map)
dir_loc = functools.partial(map_loc, m=dir_map)

def valid_map_loc(m, i, j):
    if i < 0 or j < 0 or i >= m.shape[0] or j >= m.shape[1]:
        return False
    return m.iat[i, j] != '#'
valid_num_map = functools.partial(valid_map_loc, m=num_map)
valid_dir_map = functools.partial(valid_map_loc, m=dir_map)

def map_paths_between(m, a, b):
    si, sj = a
    ei, ej = b
    di = ei - si
    dj = ej - sj
    opts = []
    if di == 0 and dj == 0:
        # We're here
        return ["A"]
    if di < 0 and valid_map_loc(m, si-1, sj):
        opts += ['^' + x for x in map_paths_between(m, (si-1, sj), b)]
    if di > 0 and valid_map_loc(m, si+1, sj):
        opts += ['v' + x for x in map_paths_between(m, (si+1, sj), b)]
    if dj < 0 and valid_map_loc(m, si, sj-1):
        opts += ['<' + x for x in map_paths_between(m, (si, sj-1), b)]
    if dj > 0 and valid_map_loc(m, si, sj+1):
        opts += ['>' + x for x in map_paths_between(m, (si, sj+1), b)]
    return opts
num_paths_between = functools.partial(map_paths_between, m=num_map)
dir_paths_between = functools.partial(map_paths_between, m=num_map)

def num_to_dirs(num_txt: str) -> list[list[str]]:
    start = num_loc('A')
    paths = []
    for c in num_txt:
        cur = num_loc(c)
        res = num_paths_between(start, cur)
        start = cur
        paths.append(res)
    return paths
def dir_to_dirs(dir_txt: str) -> list[list[str]]:
    start = dir_loc('A')
    paths = []
    for c in dir_txt:
        cur = dir_loc(c)
        res = dir_paths_between(start, cur)
        start = cur
        paths.append(res)
    return paths

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

in_txt = """
029A
980A
179A
456A
379A
341A
480A
286A
579A
149A
""".strip()

in1 = [x for x in in_txt.split("\n")]
in2 = [int(x[:-1]) for x in in1]

@functools.cache
def get_expand_len(x: str, n):
    return PathSet(dir_to_dirs(x)).expand_len_i(n-1)

# Specifies a list of lists
# First list is a series of components
# Each component is a list of options for that spot
class PathSet:
    def __init__(self, path: list[list[str]]):
        self.path = path
    
    def min_len(self) -> int:
        l = 0
        for part in self.path:
            l += min(len(x) for x in part)
        return l
    
    def num_combos(self) -> int:
        n = 1
        for part in self.path:
            n *= len(part)
        return n
    
    def flatten(self) -> list[str]:
        iters = [range(len(x)) for x in self.path]
        outs = []
        for idxs in itertools.product(*iters):
            res = ""
            for i, j in enumerate(idxs):
                res += self.path[i][j]
            outs.append(res)
        return outs
    
    def expand_len(self):
        """Run one round of dir_to_dirs expansion and return length"""
        tot = 0
        for part in self.path:
            n_opts = [PathSet(dir_to_dirs(x)).min_len() for x in part]
            tot += min(n_opts)
        return tot

    def expand_len2(self):
        """Run two rounds of dir_to_dirs expansion and return length"""
        tot = 0
        for part in self.path:
            n_opts = [PathSet(dir_to_dirs(x)).expand_len() for x in part]
            tot += min(n_opts)
        return tot
    
    def expand_len_i(self, n):
        if n == 1:
            return self.expand_len()
        tot = 0
        for part in self.path:
            n_opts = [get_expand_len(x, n) for x in part]
            tot += min(n_opts)
        return tot

# Part1
out1 = [PathSet(num_to_dirs(num_txt)).expand_len2() for num_txt in in1]
# 132532
sum(a*b for a,b in zip(out1, in2))

# Part 2
out2 = [PathSet(num_to_dirs(num_txt)).expand_len_i(25) for num_txt in in1]
# 165644591859332
sum(a*b for a,b in zip(out2, in2))

