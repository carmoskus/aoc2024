
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

df1 = pd.DataFrame(
    [[int(x) for x in y.split()] for y in in_txt],
    columns = list(string.ascii_lowercase[:5])
)
df1

df2 = df1.apply(lambda x: x.rolling(2).apply(lambda y: y.iat[1] - y.iat[0]), axis=1).dropna(axis=1)
df2

in_txt = [x.strip() for x in open('data/day2_input.txt').readlines() if x.strip() != ""]

# Loop this
in_series = [pd.Series([int(x) for x in line.split()]) for line in in_txt]

def check_line(in1):
    in2 = in1.rolling(2).apply(lambda x: x.iloc[1] - x.iloc[0]).dropna()

    # First check
    res1 = in2.lt(0).all() or in2.gt(0).all()
    # Second check
    res2 = in2.abs().max() <= 3
    return res1 and res2

# Results for part1
# [check_line(line) for line in in_series]
sum(check_line(line) for line in in_series)

# Part 2
def check_line_vars(in1):
    if check_line(in1):
        return True
    # Drop one input in series
    for i in range(len(in1)):
        if check_line(in1.drop(i)):
            return True
    
    return False

#
# [check_line_vars(line) for line in in_series]

sum(check_line_vars(line) for line in in_series)
