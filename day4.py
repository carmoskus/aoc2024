
import pandas as pd
import itertools

in_txt = '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''.strip()

in_txt = open('data/day4_input.txt').read().strip()

in1 = pd.DataFrame([list(x) for x in in_txt.split()])
in1

def check_letter(i: int, j: int, c: str):
    if i < 0 or i >= in1.shape[0] or j < 0 or j >= in1.shape[1] or in1.iat[i, j] != c[0]:
        return False
    return True

def check_from(i: int, j: int, s: str):
    if i < 0 or i >= in1.shape[0] or j < 0 or j >= in1.shape[1] or in1.iat[i, j] != s[0]:
        return 0
    if len(s) == 1:
        return 1
    # Check 8 neighboring directions
    success = 0
    for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
        if dx == 0 and dy == 0:
            continue
        for k in range(1, len(s)):
            if not check_letter(i + dx*k, j + dy*k, s[k]):
                break
        else:
            success += 1
    return success

# check_from(0, 5, 'XMAS')

sum(check_from(i, j, 'XMAS')
    for i, j in itertools.product(range(in1.shape[0]), range(in1.shape[1])))

# Part 2
def check_ex(i: int, j: int):
    if not check_letter(i, j, 'A'):
        return 0
    test1 = check_letter(i-1, j-1, 'M') and check_letter(i+1, j+1, 'S')
    test2 = check_letter(i-1, j-1, 'S') and check_letter(i+1, j+1, 'M')
    test3 = check_letter(i-1, j+1, 'M') and check_letter(i+1, j-1, 'S')
    test4 = check_letter(i-1, j+1, 'S') and check_letter(i+1, j-1, 'M')
    if (test1 or test2) and (test3 or test4):
        return 1
    return 0

sum(check_ex(i, j)
    for i, j in itertools.product(range(1, in1.shape[0]-1), range(1, in1.shape[1]-1)))
