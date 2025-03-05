
import pandas as pd
import functools, itertools, collections

def map_from_txt(txt):
    return pd.DataFrame([list(x) for x in txt.split("\n")])
def num_loc(c):
    i = num_map.eq(c).idxmax(axis=0).max()
    j = num_map.eq(c).idxmax(axis=1).max()
    return i, j
@functools.cache
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

# in_txt = """
# 341A
# 480A
# 286A
# 579A
# 149A
# """.strip()

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
# res1 = [user_cmd(x) for x in in1]
# res2 = [len(next(iter(x))) for x in res1]
# res3 = [int(x[:-1]) for x in in1]
# sum(a*b for a,b in zip(res2, res3))

# Too slow
# res4 = [user_cmd2(x, 25) for x in in1]
# res5 = [len(next(iter(x))) for x in res4]
# res6 = [int(x[:-1]) for x in in1]
# sum(a*b for a,b in zip(res5, res6))

@functools.cache
def sing_dir_to_dir(in_txt):
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

num_txt = in1[0]
paths1 = comb_paths(trim_subpaths(num_to_dirs(num_txt)))

foo = [x+'A' for x in paths1[0].split('A')][:-1]

bar = [n_dir_to_dir(x, 25) for x in foo]
bar
baz = [sing_dir_to_dir(x) for x in foo]

len(paths1[0])
len(''.join(foo))
sum(bar)
len(''.join(baz))

bar
[len(x) for x in baz]

#
sing_dir_to_dir('029A')
dir_to_dirs('029A')

foo = trim_subpaths(num_to_dirs(in1[0]))
foo
foo[0][0]
bar = [sing_dir_to_dir(x[0]) for x in foo]
bar

dir_to_dirs(foo[0][0])
trim_subpaths(dir_to_dirs(foo[0][0]))
sing_dir_to_dir(foo[0][0])

for c in ['<', '>', 'v', '^']:
    print(sing_dir_to_dir(c+'A'))


paths1[0]
sing_dir_to_dir(paths1[0])
''.join(sing_dir_to_dir(x+'A') for x in paths1[0].split('A') if x != "")

foo = paths1[0]
for i in range(25):
    print(i, len(foo))
    foo = ''.join(sing_dir_to_dir(x+'A') for x in foo.split('A') if x != "")

foo

paths2 = [comb_paths(trim_subpaths([sing_dir_to_dir(y+'A') for y in x.split('A') if y != ""]))
          for x in paths1]

paths1[0]
paths2[0]

paths2 = trim_subpaths([[sing_dir_to_dir(y)[0] for y in x] for x in paths1])

for i in range(12):
    paths1 = trim_subpaths([[sing_dir_to_dir(y)[0] for y in x] for x in paths1])


paths1[2]
a = sing_dir_to_dir(paths1[2][0])
b = sing_dir_to_dir(paths1[2][1])
sum(len(x) for x in a)
sum(len(x) for x in b)

paths2 = [[sing_dir_to_dir(y)[0] for y in x] for x in paths1]
paths3 = [[sing_dir_to_dir(y)[0] for y in x] for x in paths2]

for x in paths1:
    for y in x:
        n = sing_dir_to_dir(y)

for i in range(1):
    paths1 = [solo_path(trim_subpaths(dir_to_dirs(x))) for x in paths1]
    paths1 = functools.reduce(set.union, (set(x) for x in paths1))
    min1 = min(len(p) for p in paths1)
    print(i+1, min1, len(paths1))
    paths1 = [p for p in paths1 if len(p) == min1]
    print(i+1, min1, len(paths1))
    prios = [calc_prio(p) for p in paths1]
    max_prio = max(prios)
    paths1 = [p for p, k in zip(paths1, prios) if k == max_prio]
    print(i+1, min1, len(paths1))
    paths1 = paths1[:1]
    print(i+1, min1, len(paths1))



# min lengths
# 4,12,28,68,172,438,1114
user_cmd2(in1[0], 25)
for i in range(1, 17):
    foo = user_cmd2(in1[0], i)
    for x in foo:
        l = [len(y) for y in x]
        p = [calc_prio(y) for y in x]
        print(i, len(x), min(l), max(l), min(p), max(p))   

num_txt = in1[0]
paths1 = comb_paths(num_to_dirs(num_txt))
min1 = min(len(p) for p in paths1)
paths1 = [p for p in paths1 if len(p) == min1]
prios = [calc_prio(p) for p in paths1]
max_prio = max(prios)
paths1 = [p for p, k in zip(paths1, prios) if k == max_prio]

min1, len(paths1)
for i in range(1):
    paths1 = [solo_path(trim_subpaths(dir_to_dirs(x))) for x in paths1]
    paths1 = functools.reduce(set.union, (set(x) for x in paths1))
    min1 = min(len(p) for p in paths1)
    print(i+1, min1, len(paths1))
    paths1 = [p for p in paths1 if len(p) == min1]
    print(i+1, min1, len(paths1))
    prios = [calc_prio(p) for p in paths1]
    max_prio = max(prios)
    paths1 = [p for p, k in zip(paths1, prios) if k == max_prio]
    print(i+1, min1, len(paths1))
    paths1 = paths1[:1]
    print(i+1, min1, len(paths1))


foo = dir_to_dirs(paths1[0])
for x in foo:
    l = [len(y) for y in x]
    p = [calc_prio(y) for y in x]
    if min(l) != max(l) or min(p) != max(p):
        print(len(x), min(l), max(l), min(p), max(p))
bar = trim_subpaths(foo)
for x in bar:
    l = [len(y) for y in x]
    p = [calc_prio(y) for y in x]
    if min(l) != max(l) or min(p) != max(p):
        print(len(x), min(l), max(l), min(p), max(p))
functools.reduce(int.__mul__, (len(x) for x in bar))
solo_path(bar)
baz = comb_paths(bar)
