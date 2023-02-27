def get_input(input_file: str='Inputs/Day23_Inputs.txt') -> list:
    """
    Parse an input file giving the layout of a grove, with the positions of each of a group of
    elves marked as '#'.

    Parameters
    ----------
    input_file : str, optional
        The input file giving the grove layout.
        The default is 'Inputs/Day23_Inputs.txt'.

    Returns
    -------
    curr_pos : list(int, int)
        The (x, y) coordinates of each elf relative to the top left corner of the grid being
        (1000, 1000).

    """
    # Parse input file
    with open(input_file) as f:
         rows = [row.strip() for row in f.readlines()]

    curr_pos = []
    start_in_col = 0
    i = 0
    # For every row
    while i < len(rows):
        try:
            # Find the next elf along in that row
            # Shift all coordinates by (1000, 1000) to make room for grid growth
            curr_pos.append((i + 1000, rows[i].index('#', start_in_col) + 1000))
            # Set the point in that row to search from next
            start_in_col = curr_pos[-1][1] - 1000 + 1
        except:
            # If no elves left in current row, move to the next
            start_in_col = 0
            i += 1

    return curr_pos

def draw_rows(curr_pos: list) -> None:
    """
    Draw the current layout of the grove, with elf positions marked as '#'.

    Parameters
    ----------
    curr_pos : list(int, int)
        The (x, y) coordinates of each elf relative to the top left corner of the grid being
        (1000, 1000).

    Returns
    -------
    None.

    """
    # Find boundaries of grove
    col_min = min(p[0] for p in curr_pos)
    col_max = max(p[0] for p in curr_pos)
    row_min = min(p[1] for p in curr_pos)
    row_max = max(p[1] for p in curr_pos)
    # Draw grove
    for i in range(col_min-1, col_max+2):
        print(''.join(['#' if (i, j) in curr_pos else '.' for j in range(row_min-1, row_max+2)]))
    print('\n')

import operator

def add(t1: tuple, t2: tuple) -> tuple:
    """
    Add two tuples together element-wise.

    Parameters
    ----------
    t1 : tuple(int)
        First tuple of numbers.
    t2 : tuple(int)
        Second equal-length tuple of numbers.

    Returns
    -------
    t : tuple
        New tuple with sum of elements of t1 and t2.

    """
    return tuple(map(operator.add, t1, t2))

from collections import defaultdict

# List of all eight directions
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
# List of sets of three proposed directions, indexed as 0 = 'N', 1 = 'S', 2 = 'W', 3 = 'E'
PROP_DIRECTIONS = [[(-1, 0), (-1, 1), (-1, -1)], [(1, 0), (1, 1,), (1, -1)],
                   [(0, -1), (-1, -1), (1, -1)], [(0, 1), (-1, 1), (1, 1)]]

def one_round(curr_pos: list, first_dir_index: int) -> tuple:
    """
    Processes one round of movement for all elves in a 2D grid, given their starting positions and
    the index of the first proposal which should be made this round.

    Movement Rules
    --------------
    First, each Elf considers the eight positions adjacent to themselves. If no other Elves are in
    one of those eight positions, the Elf does not do anything during this round. Otherwise, the
    Elf looks in each of four directions in the following order and proposes moving one step in the
    first valid direction:
        If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north
        one step.

        If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south
        one step.
        
        If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west
        one step.
        
        If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east
        one step.

    After each Elf has had a chance to propose a move, the second half of the round can begin.
    Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to
    propose moving to that position. If two or more Elves propose moving to the same position, none
    of those Elves move.

    Finally, at the end of the round, the first direction the Elves considered is moved to the end
    of the list of directions.

    Parameters
    ----------
    curr_pos : list(int, int)
        The (x, y) coordinates of each elf relative to the top left corner of the grid being
        (1000, 1000).
    first_dir_index : int
        The index of the proposal to be made first this round.

    Returns
    -------
    curr_pos : list(int, int)
        The new coordinates of each elf after the round.
    changed : bool
        Whether any elf positions changed this round.

    """
    # Use defaultdict with lists to store coordinates of elves which want to move to a given spot
    moving = defaultdict(list)
    # Create set of current elf positions for faster searching
    curr_pos_set = set(curr_pos)
    # Set order of proposals for this round
    proposals = [(first_dir_index + i)%4 for i in range(4)]
    # For each elf
    for n, elf in enumerate(curr_pos):
        # Only consider moving if there are no adjacent elves
        if any(add(elf, direc) in curr_pos_set for direc in DIRECTIONS):
            # For each proposal, in the current order
            for proposal in proposals:
                # If the three corresponding positions are free, propose to move into that spot
                # and move onto the next elf
                if not any(add(elf, direc) in curr_pos_set for direc in PROP_DIRECTIONS[proposal]):
                    moving[add(elf, DIRECTIONS[proposal])].append(n)
                    break

    # For each new proposed position, if only one elf proposed moving there, perform the movement,
    # else ignore it
    for new, prev in moving.items():
        if len(prev) == 1:
            curr_pos[prev[0]] = new

    # If moving is not empty, the grid has changed
    changed = len(moving) > 0

    return curr_pos, changed

def Day23_Part1(input_file: str='Inputs/Day23_Inputs.txt') -> int:
    """
    Finds the number of empty spaces in the smallest rectangle that contains every elf on a grid
    after 10 rounds of movement according to a set of rules, given the starting layout of the elves
    in the grid.

    Movement Rules
    --------------
    First, each Elf considers the eight positions adjacent to themselves. If no other Elves are in
    one of those eight positions, the Elf does not do anything during this round. Otherwise, the
    Elf looks in each of four directions in the following order and proposes moving one step in the
    first valid direction:
        If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north
        one step.

        If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south
        one step.
        
        If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west
        one step.
        
        If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east
        one step.

    After each Elf has had a chance to propose a move, the second half of the round can begin.
    Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to
    propose moving to that position. If two or more Elves propose moving to the same position, none
    of those Elves move.

    Finally, at the end of the round, the first direction the Elves considered is moved to the end
    of the list of directions.

    Parameters
    ----------
    input_file : str, optional
        The input file giving the grove layout.
        The default is 'Inputs/Day23_Inputs.txt'.

    Returns
    -------
    empty_squares : int
        The number of empty spaces in the smallest rectangle that contains every elf on the grid.

    """
    # Parse the input file to get the initial grid layout
    curr_pos = get_input(input_file)

    # Start with the North proposal
    first_dir_index = 0
    round_num = 1

    # Do 10 rounds of moving
    while round_num <= 10:
        curr_pos, changed = one_round(curr_pos, first_dir_index)

        # Shift the order of proposals by one space
        first_dir_index = (first_dir_index + 1)%4
        round_num += 1

    # Find the boundaries of the smallest rectangle containing every elf
    col_min = min(p[0] for p in curr_pos)
    col_max = max(p[0] for p in curr_pos)
    row_min = min(p[1] for p in curr_pos)
    row_max = max(p[1] for p in curr_pos)

    # Find the number of empty spots in that rectangle
    empty_squares = (col_max - col_min + 1)*(row_max - row_min + 1) - len(curr_pos)

    return empty_squares

def Day23_Part2(input_file: str='Inputs/Day23_Inputs.txt') -> int:
    """
    Finds the number of rounds of movement required for a given starting layout of elves in a grid,
    before no elves move anymore, according to a set of movement rules.

    Movement Rules
    --------------
    First, each Elf considers the eight positions adjacent to themselves. If no other Elves are in
    one of those eight positions, the Elf does not do anything during this round. Otherwise, the
    Elf looks in each of four directions in the following order and proposes moving one step in the
    first valid direction:
        If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north
        one step.

        If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south
        one step.
        
        If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west
        one step.
        
        If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east
        one step.

    After each Elf has had a chance to propose a move, the second half of the round can begin.
    Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to
    propose moving to that position. If two or more Elves propose moving to the same position, none
    of those Elves move.

    Finally, at the end of the round, the first direction the Elves considered is moved to the end
    of the list of directions.

    Parameters
    ----------
    input_file : str, optional
        The input file giving the grove layout.
        The default is 'Inputs/Day23_Inputs.txt'.

    Returns
    -------
    round_num : int
        The number of rounds required before no elves move anymore.

    """
    # Parse the input file to get the initial grid layout
    curr_pos = get_input(input_file)
    
    # Start with the North proposal
    first_dir_index = 0
    round_num = 0

    changed = True
    # Continue until the grid doesn't change
    while changed:
        round_num += 1
        curr_pos, changed = one_round(curr_pos, first_dir_index)

        # Shift the order of proposals by one space
        first_dir_index = (first_dir_index + 1)%4

    # Return the last round number
    return round_num
