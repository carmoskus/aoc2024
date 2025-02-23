
import pandas as pd

#
def mv(r, c, dr, dc):
    if df.iat[r, c] == "#":
        # hit a wall
        return
    if df.iat[r, c] == ".":
        # move into blank space
        df.iat[r, c] = df.iat[r-dr, c-dc]
        df.iat[r-dr, c-dc] = "."
        return r, c
    if df.iat[r, c] == "O":
        # Pressing into a barrel
        # See what moving into the next square does
        beyond = mv(r+dr, c+dc, dr, dc)
        if beyond is None:
            # Hit a wall
            return
        # Then move myself
        df.iat[r, c] = df.iat[r-dr, c-dc]
        df.iat[r-dr, c-dc] = "."
        return r, c
    if df.iat[r, c] == "[":
        if dc == 0:
            # Moving vertically
            b1 = mv(r+dr, c+dc, dr, dc)
            if b1 is None:
                return
            else:
                b2 = mv(r+dr, c+dc+1, dr, dc)
                if b2 is None:
                    # Hit wall on 2nd, reverse 1st
                    df.iat[r, c] = df.iat[r+dr, c+dc]
                    df.iat[r+dr, c+dc] = "."
                    return
                else:
                    df.iat[r, c] = df.iat[r-dr, c-dc]
                    df.iat[r-dr, c-dc] = "."
                    return r, c
        # Moving horizontally
        b1 = mv(r+dr, c+dc, dr, dc)
        if b1 is None:
            return
        df.iat[r, c] = df.iat[r-dr, c-dc]
        df.iat[r-dr, c-dc] = "."
        return r, c
    if df.iat[r, c] == "]":
        if dc == 0:
            # Moving vertically
            b1 = mv(r+dr, c+dc, dr, dc)
            if b1 is None:
                return
            else:
                b2 = mv(r+dr, c+dc-1, dr, dc)
                if b2 is None:
                    # Hit wall on 2nd, reverse 1st
                    df.iat[r, c] = df.iat[r+dr, c+dc]
                    df.iat[r+dr, c+dc] = "."
                    return
                else:
                    df.iat[r, c] = df.iat[r-dr, c-dc]
                    df.iat[r-dr, c-dc] = "."
                    return r, c
        # Moving horizontally
        b1 = mv(r+dr, c+dc, dr, dc)
        if b1 is None:
            return
        df.iat[r, c] = df.iat[r-dr, c-dc]
        df.iat[r-dr, c-dc] = "."
        return r, c

def cmd(cmd):
    # Find current loc
    r = df.eq('@').idxmax(axis=1).idxmax()
    c = df.eq('@').idxmax(axis=0).idxmax()
    
    dr = 0
    dc = 0
    if cmd == '<':
        dc = -1
    elif cmd == '>':
        dc = 1
    elif cmd == "^":
        dr = -1
    elif cmd == "v":
        dr = 1
    
    if dr == 0 and dc == 0:
        return

    res = mv(r+dr, c+dc, dr, dc)
    return res

def str_to_map(map_str):
    return pd.DataFrame([list(x) for x in map_str.split("\n")])

def resize_map(m1):
    m2 = ""
    for r in range(m1.shape[0]):
        for c in range(m1.shape[1]):
            if m1.iat[r, c] == "#":
                m2 += "##"
            elif m1.iat[r, c] == ".":
                m2 += ".."
            elif m1.iat[r, c] == "O":
                m2 += "[]"
            elif m1.iat[r, c] == "@":
                m2 += "@."
        m2 += "\n"
    return str_to_map(m2.strip())

def check_map(m1):
    l1 = m1.assign(r = lambda x: x.index).melt(id_vars='r', var_name='c')
    return l1.value.value_counts(sort=False).sort_index()

#
in_txt = """
########
#......#
#......#
#......#
#..@...#
#......#
#......#
########

<^^>>>vv<v>>v<<
""".strip()

in_txt = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""".strip()

in_txt = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
""".strip()

in_txt = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()

in_txt = open('data/day15_input.txt').read()

in_txt = """
#########
#.......#
#..OO...#
#.O..O..#
#..OO...#
#..O....#
#..@....#
#########

<^^>>>vv<v>>v<<
""".strip()

#
last_wall = in_txt.rfind("#")+1
map_txt = in_txt[:last_wall].strip()
cmd_txt = in_txt[last_wall:].strip()

#
in1 = str_to_map(map_txt)
df = in1.copy()
df
for k in cmd_txt:
    _ = cmd(k)
    # print(df)
df

#
res1 = df.eq('O').assign(r=df.index).melt(
    id_vars='r', var_name='c').query('value').assign(gps=lambda x: x.c + 100 * x.r)
res1

res1.gps.sum()

# Part 2
def run_cmds(s):
    for k in s:
        cmd(k)

in2 = resize_map(in1)

df = in2.copy()
df
run_cmds('<^><<<^^>^>>^>>>>>v<>>v<')
df
run_cmds('vvv<<<^')
df

start_stats = check_map(df)
for k in cmd_txt:
    _ = cmd(k)
    stats = check_map(df)
    if not stats.equals(start_stats):
        print("CHANGED")
        break
    # print(df)
df

res2 = df.eq('[').assign(r=df.index).melt(
    id_vars='r', var_name='c').query('value').assign(gps=lambda x: x.c + 100 * x.r)
res2

res2.gps.sum()

# Check stuff
