
import itertools, functools, collections

def connections(nmap, k):
    res = [(a,b) for a,b in nmap if a == k or b == k]
    return res
def connects_to(nmap, k):
    res1 = [b for a,b in nmap if a == k]
    res2 = [a for a,b in nmap if b == k]
    return res1+res2
def are_linked(nmap, sa, sb):
    for a,b in nmap:
        if (a == sa and b == sb) or (a == sb and b == sa):
            return True
    return False
def find_trios(nmap, opts):
    res = set()
    for k in opts:
        for a,b in itertools.combinations(connects_to(nmap, k), 2):
            if are_linked(nmap, a, b):
                res.add(tuple(sorted((k, a, b))))
    return res

in_txt = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".strip()

in_txt = open('data/day23_input.txt').read()

in1 = [tuple(x.split('-')) for x in in_txt.split("\n")]
in2 = set(x[0] for x in in1) | set(x[1] for x in in1)

#
res1 = [x for x in in2 if x.startswith('t')]
res2 = find_trios(in1, res1)
len(res2)

