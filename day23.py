
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

res3 = find_trios(in1, in2)

# Trim stuff down
sub_in2 = functools.reduce(set.union, [set(x) for x in res3])
sub_in1 = [(a,b) for a,b in in1 if a in sub_in2 and b in sub_in2]
len(in2), len(sub_in2)
len(in1), len(sub_in1)

# Combine trios to turn them into quads
# Start with a node: 'ta'
# Find trios it is part of: {('co', 'ka', 'ta'), ('co', 'de', 'ta'), ('de', 'ka', 'ta')}
# Start with first trio: ('co', 'ka', 'ta')
# Look at other node options: {'de'}
# Check extra connections needed for quad: co-de, ka-de, ta-de
def expand_groups(nmap, groups):
    new_groups = set()
    old_seen = set()
    opts = set(functools.reduce(tuple.__add__, groups))
    for cur in opts:
        sub_groups = {x for x in groups if cur in x}.difference(old_seen)
        if len(sub_groups) == 0:
            continue
        sub_opts = set(functools.reduce(tuple.__add__, sub_groups))
        for g in sub_groups:
            my_opts = sub_opts.difference(set(g))
            for opt in my_opts:
                links = [are_linked(nmap, opt, x) for x in g]
                if sum(links) == len(g):
                    new = tuple(sorted(g + (opt,)))
                    new_groups.add(new)
                    for i in range(len(new)):
                        old_seen.add(new[:i] + new[i+1:])
    return new_groups

# quads = expand_groups(sub_in1, res3)
# quads

# quad_nodes = functools.reduce(set.union, (set(x) for x in quads))
# quad_map = [(a,b) for a,b in sub_in1 if a in quad_nodes and b in quad_nodes]
# g5 = expand_groups(quad_map, quads)

# g5_nodes = functools.reduce(set.union, (set(x) for x in g5))

#
gsize = 3
cur_map = sub_in1
cur_groups = res3

while True:
    new_groups = expand_groups(cur_map, cur_groups)
    if len(new_groups) == 0:
        break
    gsize += 1
    cur_groups = new_groups
    new_nodes = functools.reduce(set.union, (set(x) for x in new_groups))
    cur_map = [(a,b) for a,b in cur_map if a in new_nodes and b in new_nodes]

gsize, cur_groups

#
','.join(next(iter(cur_groups)))
