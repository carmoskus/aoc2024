
import itertools
import pandas as pd

def parse_lock(block):
    lines = block.split("\n")[1:]
    heights = {}
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "." and j not in heights:
                heights[j] = i
    res = tuple(heights[i] for i in range(5))
    return ('l',) + res
def parse_key(block):
    lines = block.split("\n")[:-1]
    heights = {}
    for i, line in enumerate(reversed(lines)):
        for j, c in enumerate(line):
            if c == "." and j not in heights:
                heights[j] = i
    res = tuple(heights[i] for i in range(5))
    return ('k',) + res
def parse_block(block):
    if block[:5] == '#'*5:
        return parse_lock(block)
    return parse_key(block)

#
in_txt = open('data/day25_test1.txt').read()
in_txt = open('data/day25_input.txt').read()

#
in_blocks = in_txt.split("\n\n")
in1 = [parse_block(x) for x in in_blocks]

#
keys = [pd.Series(x[1:]) for x in in1 if x[0] == 'k']
locks = [pd.Series(x[1:]) for x in in1 if x[0] == 'l']
count = 0
for x,y in itertools.product(keys, locks):
    if (x+y).max() <= 5:
        count += 1
count
