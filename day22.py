
import collections, functools, itertools
import pandas as pd

def mix(a, b):
    return a ^ b
def prune(a):
    return a % 16777216
def update(sec: int) -> int:
    a = sec * 64
    sec = mix(sec, a)
    sec = prune(sec)

    b = sec // 32
    sec = mix(sec, b)
    sec = prune(sec)

    c = sec*2048
    sec = mix(sec, c)
    sec = prune(sec)

    return sec
def update_n(sec: int, n: int) -> int:
    for i in range(n):
        sec = update(sec)
    return sec
def gen_sec_n(sec: int, n: int) -> list[int]:
    res = [sec]
    for i in range(n):
        sec = update(sec)
        res.append(sec)
    return res

def series_to_dict(series):
    costs = series.apply(lambda x: x % 10)
    diffs = costs.rolling(2).apply(lambda x: x.iat[1] - x.iat[0])
    res = {}
    for x in diffs.rolling(4):
        cur = tuple(x.to_list())
        if len(cur) != 4 or cur in res:
            continue
        res[cur] = costs.iat[x.index.stop-1]
    return res
def merge_dicts(a: dict, b: dict):
    opts = set(a.keys()) | set(b.keys())
    out = {k: a.get(k,0)+b.get(k,0) for k in opts}
    return out


#
in_txt = """
1
10
100
2024
""".strip()

in_txt = """
1
2
3
2024
""".strip()

in_txt = open('data/day22_input.txt').read()

in1 = [int(x) for x in in_txt.split("\n")]

# Part1
res1 = [update_n(x, 2000) for x in in1]
sum(res1)

# Part2
res2 = [gen_sec_n(x, 2000) for x in in1]
res3 = [pd.Series(x) for x in res2]

# Finding the target
cost_dicts = [series_to_dict(x) for x in res3]
full_costs = functools.reduce(merge_dicts, cost_dicts)

# 1994 is wrong; too low I think
max(full_costs.values())
