
import pandas as pd

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

#
last_wall = in_txt.rfind("#")+1
map_txt = in_txt[:last_wall].strip()
cmd_txt = in_txt[last_wall:].strip()

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
        # Actually move the barrel
        # df.iat[r+dr, c+dc] = df.iat[r, c]
        # Then move myself
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

#
df = pd.DataFrame([list(x) for x in map_txt.split("\n")])
df
for k in cmd_txt:
    cmd(k)
    # print(df)
df

#
res1 = df.eq('O').assign(r=df.index).melt(
    id_vars='r', var_name='c').query('value').assign(gps=lambda x: x.c + 100 * x.r)
res1

res1.gps.sum()
