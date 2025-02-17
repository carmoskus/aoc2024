
import pandas as pd
import re

in_txt = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
in_txt = open('data/day3_input.txt').read()

# re.findall(r'mul\(\d+,\d+\)', in_txt)
res1 = [int(x.group(1)) * int(x.group(2))
        for x in re.finditer(r'mul\((\d+),(\d+)\)', in_txt)]
res1

sum(res1)