
import collections, functools, itertools

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

#
in_txt = """
1
10
100
2024
""".strip()

in_txt = open('data/day22_input.txt').read()

in1 = [int(x) for x in in_txt.split("\n")]

# Part1
res1 = [update_n(x, 2000) for x in in1]
sum(res1)

# Test
sec = 123
for i in range(10):
    sec = update(sec)
    print(sec)

update_n(1, 2000)
