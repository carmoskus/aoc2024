
in_txt = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()

in_txt = open('data/day7_input.txt').read()

in1 = [(int(x.split(':')[0]), [int(y) for y in x.split(':')[1].strip().split()])
       for x in in_txt.split("\n")]

def check_expr(target, current, remaining):
    if current > target:
        # We overshot
        return False    
    if len(remaining) == 0:
        return current == target
    # Branch recursion
    return check_expr(target, current*remaining[0], remaining[1:]) or check_expr(target, current+remaining[0], remaining[1:])
def start_check(row):
    target, inputs = row
    return check_expr(target, inputs[0], inputs[1:])

res1 = [start_check(x) for x in in1]

sum(res1)

sum(x[0] for x, y in zip(in1, res1) if y)

# Part 2
def op_conc(a, b):
    return int(str(a) + str(b))
def check_expr2(target, current, remaining):
    if current > target:
        # We overshot
        return False    
    if len(remaining) == 0:
        return current == target
    # Branch recursion
    return check_expr2(target, current*remaining[0], remaining[1:]) or \
        check_expr2(target, op_conc(current, remaining[0]), remaining[1:]) or \
        check_expr2(target, current+remaining[0], remaining[1:])
def start_check2(row):
    target, inputs = row
    return check_expr2(target, inputs[0], inputs[1:])

res2 = [start_check2(x) for x in in1]

sum(res2)

sum(x[0] for x, y in zip(in1, res2) if y)

