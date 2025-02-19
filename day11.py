
import functools

@functools.cache
def blink_num(x):
    if x == 0:
        return 1, 
    if len(str(x)) % 2 == 0:
        y = str(x)
        a = y[:len(y)//2]
        b = y[len(y)//2:]
        return int(a), int(b)
    return x*2024,

def blink(my_in):
    my_out = []
    for x in my_in:
        if x == 0:
            my_out.append(1)
        elif len(str(x)) % 2 == 0:
            y = str(x)
            a = y[:len(y)//2]
            b = y[len(y)//2:]
            my_out.append(int(a))
            my_out.append(int(b))
        else:
            my_out.append(x*2024)
    return my_out

def mblink(n, my_in):
    for i in range(n):
        my_in = blink(my_in)
    return my_in

mblink(1, [125, 17])
mblink(2, [125, 17])
mblink(3, [125, 17])
mblink(4, [125, 17])
mblink(5, [125, 17])
mblink(6, [125, 17])

len(mblink(25, [125, 17]))

#
in_txt = open('data/day11_input.txt').read()

in1 = [int(x) for x in in_txt.split()]

len(mblink(25, in1))

# len(mblink(75, in1))

# Could try a memoize/ dynamic programming approach to optimize
# Return the number of stones that result from blinking the given input stone 'n' times
@functools.cache
def pred_blink(n, in_num):
    if n == 0:
        return 1
    out_nums = blink_num(in_num)
    if len(out_nums) == 1:
        return pred_blink(n-1, out_nums[0])
    return pred_blink(n-1, out_nums[0]) + pred_blink(n-1, out_nums[1])

res1 = [pred_blink(25, x) for x in in1]
res1
sum(res1)

res2 = [pred_blink(75, x) for x in in1]
res2
sum(res2)

