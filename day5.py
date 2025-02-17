#

class PageRules:
    def __init__(self):
        self.rules = []

    def add_rule(self, i, j):
        # i must be printed before j
        self.rules.append((i, j))

    def check(self, in1):
        rel_rules = [(i, j)
                     for i, j in self.rules
                     if i in in1 and j in in1]
        print(len(self.rules), len(rel_rules))

#
in_txt = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''.strip()

in_txt = open('data/day5_input.txt').read().strip()

in_brk1 = in_txt.rfind("|")
in_brk2 = in_brk1 + in_txt[in_brk1:].find("\n")

txt1 = in_txt[:in_brk2].strip()
txt2 = in_txt[in_brk2+1:].strip()

in1 = [[int(y) for y in x.split("|")] for x in txt1.split("\n")]
in2 = [[int(y) for y in x.split(',')] for x in txt2.split("\n")]

def check_line(order):
    rel_rules = [(i, j)
                 for i, j in in1
                 if i in order and j in order]
    for a, b in rel_rules:
        if order.index(a) > order.index(b):
            return 0
    return order[len(order) // 2]



check_line(in2[0])
res1 = [check_line(x) for x in in2]
res1

sum(res1)

# Part2
filt_in2 = [a for a, b in zip(in2, res1) if b == 0]

order = filt_in2[0]

def fix_line(order):
    rel_rules = [(i, j)
                 for i, j in in1
                 if i in order and j in order]
    rel_idx = [(order.index(a), order.index(b)) for a,b in rel_rules]
    rel_idx2 = [(i, j) for i, j in rel_idx if i > j]

    print(len(rel_idx2)) # Assumed to always be 1

    i, j = rel_idx2[0]
    new_order = order.copy()
    new_order[i] = order[j]
    new_order[j] = order[i]

    new_order
    return check_line(new_order)

res2 = [fix_line(x) for x in filt_in2]
res2

sum(res2)