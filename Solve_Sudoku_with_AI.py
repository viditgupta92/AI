rows = "ABCDEFGHI"
cols = "123456789"

def cross(a,b):
    return [r+c for r in a for c in b]

boxes = cross(rows,cols)

row_units = [cross(r,cols) for r in rows]
col_units = [cross(rows,c) for c in cols]
square_units = [cross(r,c) for r in ['ABC','DEF','GHI'] for c in ['123','456','789']]
unitlist = row_units + col_units + square_units
units = dict((b, [u for u in unitlist if b in u]) for b in boxes)
peers = dict((b, set(sum(units[b],[])) - set([b])) for b in boxes)

all_digits = '123456789'

grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    map = {}
    ctr = 0
    for row in row_units:
        for box in row:
            if grid[ctr] == '.':
                map[box] = all_digits
            else:
                map[box] = grid[ctr]
            ctr += 1
    return map

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for k,v in values.items():
        if(len(v) == 1):
            digit = v
            for peer in peers[k]:
                values[peer] = values[peer].replace(digit, '')

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in all_digits:
            lst = []
            for box in unit:
                if digit in values[box]:
                    lst.append(box)
            if len(lst) == 1:
                values[lst[0]] = digit

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Using the Eliminate Strategy
        values = eliminate(values)
        # Using the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        for k,v in values.items():
            if len(v) == 0:
                return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities

    if values == False:
        return False

    min_key = None
    min_value = 10

    for k,v in values.items():
        if len(v) > 1 and len(v) < min_value:
            min_value = len(v)
            min_key = k

    if min_key == None:
        return values

    for v in values[min_key]:
        lst = values.copy()
        lst[min_key] = v
        flag = search(lst)
        if flag:
            return flag

values = grid_values(grid)
values = search(values)
display(values)