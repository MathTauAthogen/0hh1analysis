import random
import time
import operator

currentTime = time.time()

def factorial (n):
    if (n < 0):
        raise Exception ( "Negative factorial?" )
    if (n == 0):
        return 1
    return n * factorial (n - 1)

def binom (n, k):
    if (k > n): return 0
    return factorial (n) // factorial (k) // factorial (n-k)

poss_rows = []

side_length = int(input ( "What side length?" )) # TODO: Change. This is really 1/2 of the side length, as the side length must be even so we multiply by 2.

### The below function is meant to generate all possible sequences of zeros and ones with an equal number of zeroes and ones, at first without regard to Rule 2. Each sequence lists exactly the black squares in the row.

def even_sequences (depth, thus_far, iterator, even_sequence_list ):
    
    if(depth == 0):
        even_sequence_list[:] = even_sequence_list + [ thus_far ]
        return    

    for i in range(iterator, 2 * side_length):
        even_sequences (depth - 1, thus_far + [i], i + 1, even_sequence_list )

### END FUNCTION

even_sequence_list = []

even_sequences (side_length, [], 0, even_sequence_list)


def filter_sequences ( even_sequence_list ):
    good_sequence_list = []
    for i in even_sequence_list:
        string_form = ""
        for k in range (2 * side_length):
            if k in i:
                string_form += "1"
            else:
                string_form += "0"
        if ("000" not in string_form and "111" not in string_form):
            good_sequence_list += [string_form]
    return good_sequence_list

good_sequence_list = filter_sequences ( even_sequence_list ) 

### The below is designed to generate the full list of grids if possible, but probably too slow

grids = []

def checkGood ( grid, i ):
    if ( len(grid) < 3 ):
        return True
    else:
        if ((grid[-1][i] == grid[-2][i]) and (grid[-1][i] == grid [-3][i])):
            return False
    return True

def transpose ( grid ): #TODO: Replace with good transpose function
    grid2 = []
    for i in range(len(grid[0])):
        grid2 += [[]]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid2[j] += [grid[i][j]]
    return grid2

def checkCols ( grid ):
    grid2 = transpose ( grid )
    for i in range (len(grid2)):
        if (sum(map(int,grid2[i])) != side_length):
            return False
        for j in range(i + 1, len(grid2)):
            if(grid2[i] == grid2[j]):
                return False
    return True

def check_grid ( grid ):
    good = True
    for i in range ( 2 * side_length ):
        good = good and checkGood ( grid, i )
    if ( len(grid) == 2 * side_length ):
        good = good and checkCols ( grid )
    return good

tickscounter = 0

def make_grids ( grids, curr_grid, prior_nums, depth, col_ones ):
    global tickscounter
    tickscounter += 1
    if depth == 0:
        if (check_grid(curr_grid)):
            grids += [curr_grid]
            return
    if(not check_grid( curr_grid )):
        return
    for j in range (len(good_sequence_list)):
        if (j not in prior_nums):
            new_col_ones = col_ones[:]
            new_col_ones += map(int, good_sequence_list[j].split())
            if (side_length + 1 not in new_col_ones):
                make_grids( grids, curr_grid + [good_sequence_list[j]], prior_nums + [j], depth - 1, new_col_ones )

###

print ( binom (2 * side_length , side_length) )

print ( len(good_sequence_list) )

make_grids ( grids, [], [], 2 * side_length, [0] * (2 * side_length) )

print ( len(grids) )

print ( tickscounter )

#print ( grids )

#print ( good_sequence_list )

print ( time.time() - currentTime )
