
import functools, itertools, collections

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

in_txt = open('data/day24_input.txt').read()

#
raw_in1 = in_txt[:in_txt.rfind(':')+3].strip()
raw2_in1 = [tuple(x.split(":")) for x in raw_in1.split("\n")]
in1 = {a: int(b.strip()) for a,b in raw2_in1}
raw_in2 = in_txt[in_txt.rfind(':')+3:].strip()
raw2_in2 = [tuple(x.split()) for x in raw_in2.split("\n")]
in2 = [(i[0], a, b, c) for a, i, b, _, c in raw2_in2]

print(in1)
print(in2)

def execute(instr, a, b):
    match instr:
        case 'A':
            return a and b
        case 'O':
            return a or b
        case 'X':
            return int(a != b)
def state_output(state):
    opts = list(reversed(sorted(x for x in state.keys() if x.startswith('z'))))
    res = [state[x] for x in opts]
    out = 0
    for i in range(len(res)):
        out <<= 1
        out += res[i]
    return out

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
state
state_output(state)

# Part2
