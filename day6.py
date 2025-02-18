
import pandas as pd
import numpy as np
import itertools

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

in1_raw = pd.DataFrame([list(x) for x in in_txt.split("\n")])
in1 = in1_raw.copy()
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

res1 = pd.melt(in1.eq('X').assign(r=lambda x: x.index), id_vars='r', var_name='c')
res1 = res1[res1.value].drop("value", axis=1)
res1.shape

# Testing out directions and rotations
# np.matmul(np.array([-1,0]), m_rot) # Start, heading "up"
# np.matmul(np.array([0,1]), m_rot)
# np.matmul(np.array([1,0]), m_rot)
# np.matmul(np.array([0,-1]), m_rot)

# Part 2
#
def check_obs(obs_i: int, obs_j: int):
    if check_letter(obs_i, obs_j, "#"):
        return False
    i = in1_raw.eq('^').idxmax(axis=1).idxmax()
    j = in1_raw.eq('^').idxmax(axis=0).idxmax()
    if obs_i == i and obs_j == j:
        return False
    dx = -1
    dy = 0
    log = set()
    looping = False
    in1.iat[obs_i, obs_j] = "#"
    while True:
        if (i, j, dx, dy) in log:
            # Found a loop
            looping = True
            break
        log.add((i, j, dx, dy))
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
        i += dx
        j += dy

    # Turn off inserted obstancle
    in1.iat[obs_i, obs_j] = "."
    return looping

# obs_locs = [(i, j)
#             for i, j in itertools.product(range(in1.shape[0]), range(in1.shape[1]))
#             if check_obs(i, j)]
obs_locs = [(x.r, x.c)
            for i, x in res1.iterrows()
            if check_obs(x.r, x.c)]
obs_locs
len(obs_locs)

