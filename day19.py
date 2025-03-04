
import functools

in_txt = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip()

in_txt = open('data/day19_input.txt').read()

#
in1 = [x.strip() for x in in_txt.split("\n")[0].split(",")]
in2 = [x for x in in_txt.split("\n")[1:] if x.strip() != ""]

#
def make_from(opts, target):
    @functools.cache
    def f(y):
        for x in opts:
            if len(x) <= len(y) and x == y[:len(x)]:
                # We start with x
                if len(x) == len(y):
                    # Success
                    return True
                if f(y[len(x):]):
                    return True
        return False
    return f(target)

res1 = [make_from(in1, x) for x in in2]
res1
sum(res1)
