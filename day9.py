import pandas as pd

in_txt = """
2333133121414131402
""".strip()

in_txt = open("data/day9_input.txt").read().strip()

in1 = []
for i, c in enumerate(in_txt):
    if i % 2 == 0:
        # File
        in1.append((i // 2, int(c)))
    else:
        # Gap
        in1.append((-1, int(c)))
in1

def compress(my_in):
    my_in = my_in.copy()
    i = 0
    while i < len(my_in):
        fid, size = my_in[i]
        if fid != -1:
            # Data segment
            i += 1
            continue
        # Gap, grab whatever is at the end
        if i == len(my_in) - 1:
            # We already are the last entry
            my_in.pop()
            break
        # Move stuff from last entry into current gap
        last_fid, last_size = my_in[-1]
        if last_fid == -1:
            my_in.pop()
            continue
        mv_size = min(size, last_size)
        if mv_size == size:
            # Completely remove current gap
            my_in[i] = (last_fid, size)                
            if mv_size == last_size:
                # Completely remove last entry
                my_in.pop()
            else:
                my_in[-1] = (last_fid, last_size-mv_size)
        else:
            # mv_size < size
            # Insert data before what remains of gap
            my_in[i] = (-1, size-mv_size)
            my_in.insert(i, (last_fid, mv_size))
            my_in.pop()
        i += 1
    # Compress the tail if fids are contiguous
    tail_fid = my_in[-1][0]
    tail_count = 1
    tail_sum = my_in[-1][1]
    cur_last = my_in[-1 - tail_count]
    while cur_last[0] == tail_fid:
        tail_count += 1
        tail_sum += cur_last[1]
        cur_last = my_in[-1 - tail_count]

    my_in = my_in[:-tail_count] + [(tail_fid, tail_sum)]

    return my_in

res1 = compress(in1)

in1
res1

res2 = []
for fid, size in res1:
    for i in range(size):
        res2.append(fid)
res2

res3 = [i*x for i, x in enumerate(res2)]
sum(res3)

# Part 2
def compress_gaps(my_in):
    my_out = []
    cur_gap = 0
    for fid, size in my_in:
        if cur_gap > 0:
            # We are extending a gap
            if fid == -1:
                # Continue extension
                cur_gap += size
            else:
                # Extension complete
                my_out.append((-1, cur_gap))
                cur_gap = 0
                my_out.append((fid, size))
        else:
            if fid == -1:
                # Start gap extension
                cur_gap = size
            else:
                # Move file into output
                my_out.append((fid, size))
    return my_out
        

my_in = in1.copy()

top_fid = max(x[0] for x in my_in)
while top_fid > 0:
    # print(top_fid, my_in)
    # print(top_fid, compress_gaps(my_in))
    top_i = [i for i, x in enumerate(my_in) if x[0] == top_fid][0]
    top_size = my_in[top_i][1]

    i = 0
    while i < top_i:
        if my_in[i][0] != -1:
            i += 1
            continue
        cur_size = my_in[i][1]
        # Gap
        if cur_size == top_size:
            # Exactly big enough to store us
            my_in[i] = (top_fid, top_size)
            my_in[top_i] = (-1, top_size)
            break
        elif cur_size > top_size:
            # More than big enough to store us
            my_in[i] = (-1, cur_size - top_size)
            my_in[top_i] = (-1, top_size)
            my_in.insert(i, (top_fid, top_size))
            break
        i += 1
    top_fid -= 1
    my_in = compress_gaps(my_in)

my_in

res4 = []
for fid, size in my_in:
    for i in range(size):
        res4.append(max(0, fid))
res5 = [i*x for i, x in enumerate(res4)]
sum(res5)
