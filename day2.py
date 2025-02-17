
import pandas as pd
import string

in_txt = '''
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''.strip().split('\n')

in_txt = [x.strip() for x in open('data/day2_input.txt').readlines() if x.strip() != ""]

# Loop this
def check_line(line: str):
    in1 = pd.Series(int(x) for x in line.split())
    in1

    in2 = in1.rolling(2).apply(lambda x: x.iloc[1] - x.iloc[0]).dropna()
    in2

    # First check
    res1 = in2.lt(0).all() or in2.gt(0).all()
    # Second check
    res2 = in2.abs().max() <= 3
    return res1 and res2

#
sum(check_line(line) for line in in_txt)

# Part 2
