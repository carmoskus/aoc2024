
import pandas as pd
from collections import OrderedDict

input1 = '''
3   4
4   3
2   5
1   3
3   9
3   3
'''.strip()

input1 = open('day1_input.txt').read().strip()

input_nums = pd.DataFrame([
    [int(a) for a in b.split()]
    for b in input1.split("\n")
], columns = ['a', 'b'])
input_nums

res1 = pd.DataFrame(OrderedDict(
    a = input_nums['a'].sort_values().reset_index(drop=True),
    b = input_nums['b'].sort_values().reset_index(drop=True)
)).assign(diff = lambda df: df.a - df.b)

res1

out1 = res1['diff'].abs().sum()
out1
