
import functools, itertools, collections

def execute(instr, a, b):
    match instr:
        case 'A':
            return a and b
        case 'O':
            return a or b
        case 'X':
            return int(a != b)
def state_output(state, k='z'):
    opts = list(reversed(sorted(x for x in state.keys() if x.startswith(k))))
    res = [state[x] for x in opts]
    out = 0
    for i in range(len(res)):
        out <<= 1
        out += res[i]
    return out

def get_inputs(rules, out):
    inputs = set()
    to_check = {out}
    while len(to_check) > 0:
        cur = to_check.pop()
        res = [(a,b) for i, a, b, c in rules if c == cur]
        res = set(sum(res, start=tuple()))
        inputs.update(x for x in res if x.startswith('x') or x.startswith('y'))
        to_check.update(x for x in res if not x.startswith('x') and not x.startswith('y'))
    return inputs

in_txt = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
""".strip()

in_txt = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
""".strip()

in_txt = """
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
""".strip()

in_txt = open('data/day24_input.txt').read()

#
raw_in1 = in_txt[:in_txt.rfind(':')+3].strip()
raw2_in1 = [tuple(x.split(":")) for x in raw_in1.split("\n")]
in1 = {a: int(b.strip()) for a,b in raw2_in1}
raw_in2 = in_txt[in_txt.rfind(':')+3:].strip()
raw2_in2 = [tuple(x.split()) for x in raw_in2.split("\n")]
in2 = [(i[0], a, b, c) for a, i, b, _, c in raw2_in2 if a < b] + \
      [(i[0], b, a, c) for a, i, b, _, c in raw2_in2 if b < a]

#
state = in1.copy()
rules = in2.copy()
while len(rules) > 0:
    rule = rules.pop(0)
    if rule[1] in state and rule[2] in state:
        # Inputs are ready
        a = state[rule[1]]
        b = state[rule[2]]
        state[rule[3]] = execute(rule[0], a, b)
        pass
    else:
        # Inputs aren't ready - send to back of queue
        rules.append(rule)
state_output(state)
state_output(state, 'x') + state_output(state, 'y')

state_output(state, 'x')
state_output(state, 'y')

# Part2
[(i, a, b, c) for i, a, b, c in in2 if a == 'x00' and b == 'y00']

# Check from x,y
for i in range(45):
    res = [(x, a, b, c) 
           for x, a, b, c in in2 
           if a == 'x{:02}'.format(44-i) and b == 'y{:02}'.format(44-i)]
    print(44-i, sorted(res))

# Check from z
# 8 ('A', 'x08', 'y08', 'z08')
# Should be pointing toward FOO, and there should be
# ('X', ?, ?, FOO)
def check_outputs(rules):
    for i in range(45):
        res = [(x, a, b, c) for x, a, b, c in rules if c == 'z{:02}'.format(44-i)]
        cur = res[0]
        if cur[0] != 'X':
            print(44-i, cur)
check_outputs(in2)

# Find free xor statements that might swap - we get 3 for 3
[(i, a, b, c) 
 for i, a, b, c in in2 
 if i == 'X' and not c.startswith('z') and not (a.startswith('x') and b.startswith('y'))]

# Swap with z08
max(get_inputs(in2, 'cdj'))
# Swap with z32
max(get_inputs(in2, 'gfm'))
# Swap with z16
max(get_inputs(in2, 'mrb'))

def flip_rules(in_rules, flips):
    flip_vals = set(sum(flips, start=tuple()))
    out_rules = [(i, a, b, c) for i, a, b, c in in_rules if c not in flip_vals]
    for oa, ob in flips:
        rule1 = [(i, a, b, c) for i, a, b, c in in_rules if c == oa][0]
        rule2 = [(i, a, b, c) for i, a, b, c in in_rules if c == ob][0]
        out_rules.append(rule1[:3] + (ob,))
        out_rules.append(rule2[:3] + (oa,))
    return out_rules

flip_outs = [('z08', 'cdj'), ('z16', 'mrb'), ('z32', 'gfm')]
new_rules = flip_rules(in2, flip_outs)

check_outputs(new_rules)

# Check from x,y
for i in range(45):
    res = [(x, a, b, c) 
           for x, a, b, c in new_rules
           if a == 'x{:02}'.format(44-i) and b == 'y{:02}'.format(44-i)]
    print(44-i, sorted(res))
# Check from input ANDs
for i in range(45):
    res = [(x, a, b, c) 
           for x, a, b, c in new_rules
           if x == 'A' and a == 'x{:02}'.format(44-i) and b == 'y{:02}'.format(44-i)]
    res2 = [(x, a, b, c) 
           for x, a, b, c in new_rules
           if a == res[0][3] or b == res[0][3]]
    print(44-i, sorted(res2))
# Found anomoly
# 38 [('A', 'kvn', 'qjd', 'bgj'), ('X', 'kvn', 'qjd', 'z38')]
# Comes from
# ('A', 'x38', 'y38', 'qjd')
# But should be a single OR

max(get_inputs(in2, 'qjd'))
max(get_inputs(in2, 'kvn'))

# Check from input XORs
for i in range(45):
    res = [(x, a, b, c) 
           for x, a, b, c in new_rules
           if x == 'X' and a == 'x{:02}'.format(44-i) and b == 'y{:02}'.format(44-i)]
    res2 = [(x, a, b, c) 
           for x, a, b, c in new_rules
           if a == res[0][3] or b == res[0][3]]
    print(44-i, sorted(res2))
# Found anomoly
# 38 [('O', 'bgj', 'dhm', 'bqf')]
# Comes from 
# ('X', 'x38', 'y38', 'dhm')

flip_outs2 = [('qjd', 'dhm')]
new_rules2 = flip_rules(new_rules, flip_outs2)

flip_names = sorted(sum(flip_outs, start=tuple()) + sum(flip_outs2, start=tuple()))
','.join(flip_names)
