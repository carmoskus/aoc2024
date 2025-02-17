
import pandas as pd
import numpy as np

m_rot = np.array([[0,-1],[1,0]])

in_txt = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()

in_txt = open('data/day6_input.txt').read()

def check_letter(i: int, j: int, c: str):
    if i < 0 or i >= in1.shape[0] or j < 0 or j >= in1.shape[1] or in1.iat[i, j] != c[0]:
        return False
    return True

in1 = pd.DataFrame([list(x) for x in in_txt.split("\n")])
in1

#
i = in1.eq('^').idxmax(axis=1).idxmax()
j = in1.eq('^').idxmax(axis=0).idxmax()
dx = -1
dy = 0
while True:
    if i < 0 or j < 0 or i >= in1.shape[0] or j >= in1.shape[0]:
        # We escaped
        break
    if check_letter(i, j, '#'):
        # We bumped into something
        i -= dx
        j -= dy
        new_delta = np.matmul(np.array([dx, dy]), m_rot)
        dx = new_delta[0]
        dy = new_delta[1]
        i += dx
        j += dy
        continue
    # Stepped onto a normal tile - mark it
    in1.iat[i, j] = 'X'
    i += dx
    j += dy

in1

in1.eq('X').sum().sum()

# Testing out directions and rotations
np.matmul(np.array([-1,0]), m_rot)
np.matmul(np.array([0,1]), m_rot)
np.matmul(np.array([1,0]), m_rot)
np.matmul(np.array([0,-1]), m_rot)
