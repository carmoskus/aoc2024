
import pandas as pd
import string

in_txt = '''
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''.strip()

in_txt = open('data/day2_input.txt').read().strip()


in1 = pd.DataFrame([
    [int(a) for a in b.split()]
    for b in in_txt.split("\n")
], columns = [x for x in string.ascii_lowercase[:5]])
in1

in1.iloc[0, :].rolling(2).apply(lambda x: x[1] - x[0]).dropna()
in1.iloc[1, :].rolling(2).apply(lambda x: x[1] - x[0]).dropna()

in2 = in1.apply(lambda x: x.rolling(2).apply(lambda y: y[1] - y[0]), 1).drop('a', axis=1)
in2

# First check
res1 = in2.lt(0).all(axis=1) | in2.gt(0).all(axis=1)
res1

# Second check
# The remaining inputs
in2[res1]

in2[res1].abs().max(axis=1)
res2 = in2[res1].abs().max(axis=1).le(3)
res2

res2.sum()
