
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

input1 = open('data/day1_input.txt').read().strip()

input_nums = pd.DataFrame([
    [int(a) for a in b.split()]
    for b in input1.split("\n")
], columns = ['a', 'b'])
input_nums

# Part 1
res1 = pd.DataFrame(OrderedDict(
    a = input_nums['a'].sort_values().reset_index(drop=True),
    b = input_nums['b'].sort_values().reset_index(drop=True)
)).assign(diff = lambda df: df.a - df.b)

res1

out1 = res1['diff'].abs().sum()
out1

# Part 2
input_nums.b.value_counts()
input_nums[['a']].set_index('a', drop=False)

res2 = input_nums[['a']].set_index('a', drop=False).join(input_nums.b.value_counts()).assign(
    y = lambda x: x['a'] * x['count']
)
res2

res2.y.sum()
