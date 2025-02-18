
import pandas as pd
import numpy as np
import itertools, functools

in_txt = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()

in_txt = open('data/day8_input.txt').read()

in1 = pd.DataFrame([list(x) for x in in_txt.split("\n")])
in1

# Work out frequencies
# Symbols other than '.'
long1 = pd.melt(in1.assign(r=lambda x: x.index), id_vars='r', var_name='c')
long1 = long1[long1.value != '.']
long1

res1 = long1.value.value_counts()
res1
res1.index

all_nodes = {}
for freq in res1.index:
    freq_locs = long1[long1.value == freq]
    freq_series = [np.array([x.r, x.c]) for i, x in freq_locs.iterrows()]
    freq_nodes = set()
    for i, j in itertools.combinations(range(len(freq_series)), 2):
        loc1 = freq_series[i]
        loc2 = freq_series[j]
        delta = loc2 - loc1
        freq_nodes.add(tuple(loc1-delta))
        freq_nodes.add(tuple(loc2+delta))
    all_nodes[freq] = freq_nodes
all_nodes

full_nodes = functools.reduce(set.union, all_nodes.values())
filt_nodes = {x for x in full_nodes if x[0] >= 0 and x[1] >= 0 and x[0] < in1.shape[0] and x[1] < in1.shape[1]}
filt_nodes

len(filt_nodes)
