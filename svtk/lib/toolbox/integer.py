import math as m

def minmax(n, min_val, max_val):
    '''Limit n to be between min_val and max_val'''
    assert(min_val<=max_val)
    return max(min(n,max_val), min_val)

def nth_middle(n, min_val, max_val):
    '''
    take a stick, break it in half, then break those sticks in half, and so on, until you do
    it i times.
    If these sticks were instead rulers, this function would return where the next break
    would be in the ruler's range, if you were neatly breaking the ruler from left to right.

    credit for making this non-recursive goes to: http://math.stackexchange.com/a/1706893/324663
    '''
    assert (min_val <= max_val)
    depth = m.floor(m.log2(n+1))
    node = n - (1<<depth) + 1
    section_size = (max_val - min_val) / (1<<depth)
    middle = min_val + node*section_size + section_size/2
    return middle


