
import pandas as pd
import re

in_txt = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
in_txt = open('data/day3_input.txt').read()

# re.findall(r'mul\(\d+,\d+\)', in_txt)
res1 = [int(x.group(1)) * int(x.group(2))
        for x in re.finditer(r'mul\((\d+),(\d+)\)', in_txt)]
res1

sum(res1)

# Part 2
in_txt = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

re.findall(r"mul\(\d+,\d+\)", in_txt)
re.findall(r"do\(\)", in_txt)
re.findall(r"don't\(\)", in_txt)

re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", in_txt)

res2 = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", in_txt)
res2

res3 = []
res3_on = True
for x in res2:
    if x == "do()":
        res3_on = True
    elif x == "don't()":
        res3_on = False
    elif res3_on:
        m = re.match(r"mul\((\d+),(\d+)\)", x)
        y = int(m.group(1)) * int(m.group(2))
        res3.append(y)
res3
sum(res3)
