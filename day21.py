
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
def solo_path(paths):
    res = "".join(x[0] for x in paths)
    return [res]
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
def user_cmd2(num_txt, num_keypads):
    paths1 = comb_paths(num_to_dirs(num_txt))
    min1 = min(len(p) for p in paths1)
    paths1 = [p for p in paths1 if len(p) == min1]

    for i in range(num_keypads):
        paths1 = [solo_path(trim_subpaths(dir_to_dirs(x))) for x in paths1]
        paths1 = functools.reduce(set.union, (set(x) for x in paths1))
        min1 = min(len(p) for p in paths1)
        paths1 = [p for p in paths1 if len(p) == min1]

    return paths1
def calc_prio(path):
    num_reps = 0
    for i in range(1, len(path)):
        if path[i] == path[i-1]:
            num_reps += 1
    return num_reps
def trim_subpaths(foo):
    res = []
    for x in foo:
        l = [len(y) for y in x]
        min_l = min(l)
        x = [a for a,b in zip(x, l) if b == min_l]
        p = [calc_prio(y) for y in x]
        max_p = max(p)
        x = [a for a,b in zip(x, p) if b == max_p]
        res.append(x)
    return res
        

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

# Too slow
# res4 = [user_cmd2(x, 25) for x in in1]
# res5 = [len(next(iter(x))) for x in res4]
# res6 = [int(x[:-1]) for x in in1]
# sum(a*b for a,b in zip(res5, res6))

@functools.cache
def sing_dir_to_dir(in_txt):
    # Check more options that just [0]
    res = [x[0] for x in trim_subpaths(dir_to_dirs(in_txt))]
    return ''.join(res)

@functools.cache
def n_dir_to_dir(in_txt, n):
    if n == 0:
        return len(in_txt)
    subs = [x for x in sing_dir_to_dir(in_txt).split('A')][:-1]
    sub_counts = collections.Counter(subs)
    count = 0
    for k, l in sub_counts.items():
        count += l*n_dir_to_dir(k+'A', n-1)
    return count

def count_num_to_dir_n(num_txt, n):
    paths1 = comb_paths(trim_subpaths(num_to_dirs(num_txt)))
    min_l = None
    min_p = None
    for p in paths1:
        foo = [x+'A' for x in p.split('A')][:-1]
        res = [n_dir_to_dir(x, n) for x in foo]
        l = sum(res)
        if min_l is None or l < min_l:
            min_p = res
            min_l = l
    return min_p

def expand_dir(dir_txt):
    if 'A' in dir_txt[:-1]:
        return [expand_dir(x+'A') for x in dir_txt.split('A')[:-1]]
    opts = comb_paths(dir_to_dirs(dir_txt))
    min_l = min(len(x) for x in opts)
    opts = [x for x in opts if len(x) == min_l]

    res = functools.reduce(
        list.__add__, 
        (comb_paths(dir_to_dirs(x)) for x in opts))
    min_l = min(len(x) for x in res)
    res = [x for x in res if len(x) == min_l]
    return res
def expand_dir2(dir_txt):
    if 'A' in dir_txt[:-1]:
        return [expand_dir(x+'A') for x in dir_txt.split('A')[:-1]]
    opts = comb_paths(dir_to_dirs(dir_txt))
    min_l = min(len(x) for x in opts)
    opts = [x for x in opts if len(x) == min_l]

    res = functools.reduce(
        list.__add__, 
        (comb_paths(dir_to_dirs(x)) for x in opts))
    min_l = min(len(x) for x in res)
    res = [x for x in res if len(x) == min_l]

    res = functools.reduce(
        list.__add__, 
        (comb_paths(dir_to_dirs(x)) for x in res))
    min_l = min(len(x) for x in res)
    res = [x for x in res if len(x) == min_l]

    return res

def comb_path_len(paths):
    l = 0
    for x in paths:
        l += min(len(y) for y in x)
    return l

def calc_dir_len(paths):
    min_a = min_b = None
    for p in paths:
        a = n_dir_to_dir(p, 2)
        b = min(len(x) for x in expand_dir(p))
        if min_a is None or a < min_a:
            min_a = a
        if min_b is None or b < min_b:
            min_b = b
    return min_a,min_b

# Compare values fully expanded twice to results from count_num
seen = set()
opts = set()

for num_txt in in1:
    paths1 = comb_paths(num_to_dirs(num_txt))
    opts.update(
        set(x+'A' for x in functools.reduce(
        list.__add__, (x.split('A')[:-1] for x in paths1))))

while len(opts) > 0:
    cur = opts.pop()
    seen.add(cur)
    paths = dir_to_dirs(cur)
    for x in paths:
        for y in x:
            if y in seen or y in opts:
                continue
            opts.add(y)
    a,b = calc_dir_len([cur])
    if a != b:
        print(a, b, cur)

seen

#
paths1 = num_to_dirs(in1[4])
cpaths1 = comb_paths(paths1)

foo = expand_dir(cpaths1[0])
bar = expand_dir2(cpaths1[0])

foo[0][0]
bar[0][0]


len(foo)
len(bar)
len(bar[0])

foo = [expand_dir(p) for p in cpaths1]
len(cpaths1)
len(foo)
cpaths1[0]
foo[0]
bar = [comb_paths(p) for p in foo]


calc_dir_len(['<A'])
expand_dir('<A')
comb_path_len(expand_dir('<A'))
min(len(x) for x in expand_dir('<A'))
n_dir_to_dir('<A', 1)
n_dir_to_dir('<A', 2)
comb_paths(dir_to_dirs('<A'))
[len(x) for x in comb_paths(dir_to_dirs('<A'))]
[comb_paths(dir_to_dirs(x)) for x in comb_paths(dir_to_dirs('<A'))]
foo = [comb_paths(dir_to_dirs(x)) for x in comb_paths(dir_to_dirs('<A'))]
min(min(len(y) for y in x) for x in foo)


for num_txt in in1:
    paths = comb_paths(num_to_dirs(num_txt))
    path_subs = set(x+'A' for x in functools.reduce(
        list.__add__, (x.split('A')[:-1] for x in paths)))
    path_subs = path_subs.difference(seen)

    a, b = calc_dir_len(paths)
    if a != b:
        print(a, b, num_txt)

# min lengths for 029A
# 4,12,28,68,172?,438?,1114?
foo = [count_num_to_dir_n(x, 2) for x in in1]
bar = [sum(x) for x in foo]
bar
sum([x*y for x,y in zip(res3, bar)])

res4 = [count_num_to_dir_n(x, 25) for x in in1]
res5 = [sum(x) for x in res4]
res5
# 304173986714766 is wrong - too high
# 189357384273226 is wrong - too high
# 165644591859332
sum([x*y for x,y in zip(res3, res5)])
