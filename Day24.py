# Set up possible directions correpsonding to each symbol
DIRECTIONS = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}
SYMBOLS = {v: k for k, v in DIRECTIONS.items()}

def get_input(input_file: str='Inputs/Day24_Inputs.txt') -> tuple:
    """
    Parse an input file giving the layout of a valley, bounded by walls (#) and containing empty
    space (.) surrounded by a series of moving blizzards (>, v, <, ^) represented by arrows
    indicating their direction of movement. Extracts the initial blizzard layout, the entrance and
    exit from the valley and the dimensions of the valley.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the valley layout.
        The default is 'Inputs/Day24_Inputs.txt'.

    Returns
    -------
    all_blizzards : dict(tuple: list(tuple))
        Dictionary of lists of the initial coordinates of every blizzard going in a given direction,
        hashed by the unit vector of that direction, in the form (x, y).

    journey_bounds : tuple(tuple(int))
        The coordinates (x, y) of the entrance and exit from the valley in the form (entrance,
        exit).

    valley_bounds : tuple(int)
        The dimensions of the valley in the form (length, width).

    """
    # Parse input file
    with open(input_file) as f:
        lines = [line.strip() for line in f.readlines()]
    # Calculate valley dimensions, discounting the walls
    valley_length = len(lines) - 2
    valley_width = len(lines[0]) - 2
    # Find the coordinates of the start (first row) and end (last row)
    begin = (-1, lines[0].index('.') - 1)
    end = (valley_length, lines[-1].index('.') - 1)
    # Initliase empty blizzard position dictionary
    all_blizzards = {direction: [] for direction in DIRECTIONS.values()}
    # For each row of the valley within the walls
    for i, line in enumerate(lines[1:-1]):
        # Check each character
        for j, c in enumerate(line.strip('#')):
            if c == '.':
                continue
            # If a blizzard, add to the list corresponding to its direction
            all_blizzards[DIRECTIONS[c]].append((i, j))

    return all_blizzards, (begin, end), (valley_length, valley_width)

def draw_valley(all_blizzards: dict, journey_bounds: tuple, valley_bounds: tuple,
                player_pos: tuple) -> None:
    """
    Draw the current valley layout, with walls marked as '#', blizzards marked by arrows of their
    direction, or the number of blizzards in that spot if there are multiple, empty spots as '.'
    and the player position marked as 'E'.

    Parameters
    ----------
    all_blizzards : dict(tuple: list(tuple))
        Dictionary of lists of the initial coordinates of every blizzard going in a given direction,
        hashed by the unit vector of that direction, in the form (x, y).
    journey_bounds : tuple(tuple(int))
        The coordinates (x, y) of the entrance and exit from the valley in the form (entrance,
        exit).
    valley_bounds : tuple(int)
        The dimensions of the valley in the form (length, width).
    player_pos : tuple(int)
        Current player position in the form (x, y).

    Returns
    -------
    None.

    """
    # Print the upper wall with entrance
    print('#' + ''.join('E' if (-1, j) == player_pos else '.' if j == journey_bounds[0][1] else '#' \
                        for j in range(valley_bounds[1])) + '#')
    # For each row
    for i in range(valley_bounds[0]):
        # Add left wall
        row = '#'
        for j in range(valley_bounds[1]):
            # Add player if found
            if (i, j) == player_pos:
                row += 'E'
                continue
            # Count how many blizzards on the same spot and add correpsonding character
            matched_symbols = []
            for direction, blizzards in all_blizzards.items():
                if (i, j) in blizzards:
                    matched_symbols.append(SYMBOLS[direction])
            if len(matched_symbols) == 0:
                row += '.'
            elif len(matched_symbols) == 1:
                row += matched_symbols[0]
            else:
                row += str(len(matched_symbols))
        # Add right wall and print
        print(row + '#')

    # Print the lower wall with exit
    print('#' + ''.join('E' if (valley_bounds[0] + 1, j) == player_pos else '.' if j == journey_bounds[1][1] else '#' \
                        for j in range(valley_bounds[1])) + '#')

def add_coords(curr: tuple, dir_: tuple, bounds: tuple=None, moves: int=1) -> tuple:
    """
    Finds the new coordinates after moving a given number of spaces in a given direction from
    initial coordinates. If bounds are specified, the coordinates will wrap around when these
    boundaries are exceeded.

    Parameters
    ----------
    curr : tuple(int)
        The initial coordinates.
    dir_ : tuple(int)
        Unit vector of the direction being moved in.
    bounds : tuple(int) or None, optional
        If not None, then the upper boundaries of the grid in the form (x_max, y_max).
        The default is None.
    moves : int, optional
        The number of spaces to move.
        The default is 1.

    Returns
    -------
    new_pos : tuple(int)
        Coordinates of the new position after the movement.

    """
    # If boundaries, perform wrapping with % b
    if bounds:
        return tuple(map(lambda x, y, b : (x + moves*y) % b, curr, dir_, bounds))
    # Else just add the unit vector multplied by the number of moves
    else:
        return tuple(map(lambda x, y : x + moves*y, curr, dir_))

def coord_is_in_bounds(coord: tuple, bounds: tuple, journey_bounds: tuple) -> tuple:
    """
    Checks if a set of coordinates are within a set of boundaries, or match an element from a
    separate, special set of coordinates.

    Parameters
    ----------
    coord : tuple(int)
        Coordinate to check in the form (x, y).
    bounds : tuple(int)
        Upper boundaries in the form (x_max, y_max).
    journey_bounds : tuple(tuple(int))
        Tuple of coordinates outside the bounds which should also pass this check.

    Returns
    -------
    is_in_bounds : bool
        Whether the coordinate is within the given bounds or special set of coordinates.

    """
    # Check if coords are in special set, or if coords are between 0 and upper bounds
    return coord in journey_bounds or all(map(lambda c, b : 0 <= c < b, coord, bounds))

def move_blizzards(all_blizzards: dict, valley_bounds: tuple, moves: int=1) -> dict:
    """
    Move a set of blizzards in a valley a set number of positions from given starting points, in
    the directions in which they are moving. If a blizzard moves outside given bounds of the valley
    then the coordinates should wrap around to 0.

    Parameters
    ----------
    all_blizzards : dict(tuple: list(tuple))
        Dictionary of lists of the initial coordinates of every blizzard going in a given direction,
        hashed by the unit vector of that direction, in the form (x, y).
    valley_bounds : tuple(int)
        The dimensions of the valley in the form (length, width).
    moves : int, optional
        The number of spaces for each blizzard to move.
        The default is 1.

    Returns
    -------
    next_blizzards : dict(tuple: list(tuple))
        Dictionary of lists of the final coordinates of every blizzard after the movements.

    """
    # Create copy of blizzards to edit
    next_blizzards = all_blizzards.copy()
    # For the blizzards in each direction
    for direction, blizzards in all_blizzards.items():
        # Set up lambda for movement in current direction
        move_in_dir = lambda t : add_coords(t, direction, valley_bounds, moves)
        # Map onto blizzards moving in that direction
        next_blizzards[direction] = list(map(move_in_dir, blizzards))

    return next_blizzards

def find_possible_moves(curr_pos: tuple, next_blizzards: dict, valley_bounds: tuple,
                        journey_bounds: tuple) -> set:
    """
    Finds the possible next moves for a player in a given position in a valley containing a set
    of moving blizzards. Possible moves are up, down, left, right or no move, but a player cannot
    move/remain in a position which will be occupied by a blizzard. Additionally, the player cannot
    move outside given valley bounds, except into given entrance and exit points.

    Parameters
    ----------
    curr_pos : tuple(int)
        Current player position in the form (x, y).
    next_blizzards : dict(tuple: list(tuple))
        Dictionary of lists of the initial coordinates of every blizzard going in a given direction,
        hashed by the unit vector of that direction, in the form (x, y).
    valley_bounds : tuple(int)
        The dimensions of the valley in the form (length, width).
    journey_bounds : tuple(tuple(int))
        The coordinates (x, y) of the entrance and exit from the valley in the form (entrance,
        exit).

    Returns
    -------
    next_positions : set(tuple(int))
        List of the potential coordinates which the player can move to.

    """
    # If the current position will not contain a blizzard next turn, not moving is an option
    if curr_pos not in next_blizzards:
        next_positions = {curr_pos}
    # Else remaining here is not an option
    else:
        next_positions = set()
    # For each possible movement direction
    for direction in DIRECTIONS.values():
        # Find new coordinates after this move
        next_pos = add_coords(curr_pos, direction)
        # If this position is within the boundaries and will not contain a blizzard next turn,
        # it is an option
        if coord_is_in_bounds(next_pos, valley_bounds, journey_bounds) and \
            next_pos not in next_blizzards:
            next_positions.add(next_pos)

    return next_positions

### All this is just to find the lowest common multiple of two numbers ###
                                                                         #
def next_prime(n: int) -> int:                                           #
    """                                                                  #
    Finds the next highest prime number after a given integer.           #
                                                                         #
    Parameters                                                           #
    ----------                                                           #
    n : int                                                              #                                                                         #                                                                         #
        The current number.                                              #
                                                                         #                                                                         #                                                                         #
    Returns                                                              #
    -------                                                              #
    n : int                                                              #
        The next highest prime number after the given integer.           #
                                                                         #
    """                                                                  #
    n += 1                                                               #
    # While the number has any factors between 2 and sqrt(n), increment  #
    while not all(n%i for i in range(2, int(n**0.5))):                   #
        n += 1                                                           #
                                                                         #
    return n                                                             #
                                                                         #
def prime_factors(n: int) -> set:                                        #
    """                                                                  #
    Finds the prime factors of a given integer.                          #
                                                                         #
    Parameters                                                           #
    ----------                                                           #
    n : int                                                              #
        Number to find the prime factors for.                            #
                                                                         #
    Returns                                                              #
    -------                                                              #
    factors : set(tuple(int))                                            #
        Set of the prime factors of the given number, in the form        #
        (factor, occurance).                                             #
                                                                         #
    """                                                                  #
                                                                         #
    factors = set()                                                      #
    # Start at 2                                                         #
    f = 2                                                                #
    # While there are remaining factors                                  #
    while n > 1:                                                         #
        # Count occurances of current factor                             #
        num = 1                                                          #
        while n%f == 0:                                                  #
            n /= f                                                       #
            # Add new factor with occurance count                        #
            factors.add((f, num))                                        #
            num += 1                                                     #
        # Check next highest prime number                                #
        f = next_prime(f)                                                #
                                                                         #
    return factors                                                       #
                                                                         #
import operator                                                          #
from functools import reduce                                             #
                                                                         #
def gcd(a: int, b: int) -> int:                                          #
    """                                                                  #
    Find the greatest common divisor of two integers.                    #
                                                                         #
    Parameters                                                           #
    ----------                                                           #
    a : int                                                              #
        First integer.                                                   #                                                                         #
    b : int                                                              #
        Second integer.                                                  #
                                                                         #
    Returns                                                              #
    -------                                                              #
    gcd : int                                                            #
        Greatest common divisor of the two integers.                     #
                                                                         #
    """                                                                  #
    # Find prime factors of the numbers                                  #
    a_f = prime_factors(a)                                               #
    b_f = prime_factors(b)                                               #
    # Find all common prime factors                                      #
    c_f = [f[0] for f in a_f.intersection(b_f)]                          #
    # GCD is the product of these common factors                         #
    return reduce(operator.mul, c_f, 1)                                  #
                                                                         #
def lcm(a: int, b: int) -> int:                                          #
    """                                                                  #
    Find the lowest common multiple of two integers.                     #
                                                                         #
    Parameters                                                           #
    ----------                                                           #
    a : int                                                              #
        First integer.                                                   #
    b : int                                                              #
        Second integer.                                                  #
                                                                         #
    Returns                                                              #
    -------                                                              #
    lcm : int                                                            #
        Lowest common multiple of the two integers.                      #
                                                                         #
    """                                                                  #
    # Find GCD of the numbers, then multiply by the uncommon factors     #
    # from both numbers                                                  #
    return int((a / gcd(a, b)) * b)                                      #
                                                                         #
##########################################################################

def find_fastest_route_bfs(journey_bounds: tuple, all_blizzard_states: list, valley_bounds: tuple,
                           start_moves: int=0) -> list:
    """
    Performs a breadth-first search to find the fewest number of moves required to move between
    given journey bounds, in a valley of given dimensions containing a set of blizzards which
    move in set directions every move and which the player cannot share the same position with at
    any time.

    Parameters
    ----------
    journey_bounds : tuple(tuple(int))
        The coordinates (x, y) of the entrance and exit from the valley in the form (entrance,
        exit).
    all_blizzard_states : list(set(tuple))
        Dictionary of lists of the initial coordinates of every blizzard going in a given direction,
        hashed by the unit vector of that direction, in the form (x, y).
    valley_bounds : tuple(int)
        The dimensions of the valley in the form (length, width).
    start_moves : int, optional
        The number of moves to start at.
        The default is 0.

    Returns
    -------
    fewest_moves : int
        The fewest number of moves required to move between given journey bounds, after the given
        number of starting moves.

    """
    # Initalise queue of states for BFS with (position, moves_to_reach) describing each state
    queue = [(journey_bounds[0], start_moves)]
    # Initalise set of checked states
    checked_states = set()

    # While there are unchecked states
    while queue:
        # Get next highest priority state
        curr_pos, curr_moves = queue.pop(0)
        # Find possible next positions from current position
        next_positions = find_possible_moves(curr_pos,
                                             all_blizzard_states[(curr_moves + 1) % len(all_blizzard_states)],
                                             valley_bounds, journey_bounds)
        # If we have reached the target end point, return the current move count
        if journey_bounds[1] in next_positions:
            return curr_moves + 1
        # Else for each possible next position (if any)
        for pos in next_positions:
            # Create correpsonding state
            next_state = (pos, curr_moves + 1)
            # Check if this has already been checked
            if next_state not in checked_states:
                # If not, add to the queue and set of checked states
                queue.append(next_state)
                checked_states.add(next_state)

def Day24_Part1(input_file: str='Inputs/Day24_Inputs.txt') -> int:
    """
    Finds the fewest number of moves required to reach the other side of valley containing a
    set of blizzards which move in set directions every move and which the player cannot share the
    same position with at any time. The layout of the valley is given in an input file, with the
    valley walls marked as '#', empty space as '.' and blizzards represented by arrows indicating
    their direction of their movement ('>', 'v', '<', '^'). When blizzards reach a valley wall,
    they wrap around to the opposite side and continue moving in the same direction.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the valley layout.
        The default is 'Inputs/Day24_Inputs.txt'.

    Returns
    -------
    start_to_end : int
        The fewest number of moves required to reach the other side of valley.

    """
    # Extract initial blizzard positions and journey and valley boundaries from input file
    all_blizzards, journey_bounds, valley_bounds = get_input(input_file)

    # Find fewest number of moves required for the blizzards to recover their initial positions
    num_blizzard_states = lcm(*valley_bounds)
    all_blizzard_states = []
    # Find every possible unique blizzard layout
    for moves in range(num_blizzard_states + 1):
        all_blizzard_states.append(move_blizzards(all_blizzards, valley_bounds, moves))

    # Assert that the blizzards recovered their initial positions at the end
    assert all_blizzard_states[0] == all_blizzard_states[-1]

    # Join together all blizzard positions into a single set
    all_blizzard_states = [set(bliz for direc in blizzard_state.values() for bliz in direc) \
                           for blizzard_state in all_blizzard_states[:-1]]

    # Perform a breadth-first search through the valley to find the lowest number of moves required
    start_to_end = find_fastest_route_bfs(journey_bounds, all_blizzard_states, valley_bounds)

    return start_to_end

def Day24_Part1and2(input_file: str='Inputs/Day24_Inputs.txt') -> tuple:
    """
    Finds the fewest number of moves required to reach the other side of valley containing a
    set of blizzards which move in set directions every move and which the player cannot share the
    same position with at any time. Then finds the fewest number of moves to do this, then go back
    to the start and then go back to the end all in a row, with the blizzards continuing to move
    the whole time. The layout of the valley is given in an input file, with the valley walls
    marked as '#', empty space as '.' and blizzards represented by arrows indicating their
    direction of their movement ('>', 'v', '<', '^'). When blizzards reach a valley wall, they wrap
    around to the opposite side and continue moving in the same direction. 

    Parameters
    ----------
    input_file : str, optional
        Input file containing the valley layout.
        The default is 'Inputs/Day24_Inputs.txt'.

    Returns
    -------
    start_to_end : int
        The fewest number of moves required to reach the other side of valley.
    start_to_end_and_back_and_back : int
        The fewest number of moves required to reach the other side of valley, then go back to the
        start, and then go back to the end again.

    """
    # Extract initial blizzard positions and journey and valley boundaries from input file
    all_blizzards, journey_bounds, valley_bounds = get_input(input_file)
    
    # Find fewest number of moves required for the blizzards to recover their initial positions
    num_blizzard_states = lcm(*valley_bounds)
    all_blizzard_states = []
    # Find every possible unique blizzard layout
    for moves in range(num_blizzard_states + 1):
        all_blizzard_states.append(move_blizzards(all_blizzards, valley_bounds, moves))

    # Assert that the blizzards recovered their initial positions at the end
    assert all_blizzard_states[0] == all_blizzard_states[-1]

    # Join together all blizzard positions into a single set
    all_blizzard_states = [set(bliz for direc in blizzard_state.values() for bliz in direc) \
                           for blizzard_state in all_blizzard_states[:-1]]

    # Perform a breadth-first search through the valley to find the lowest number of moves required
    # to go from the start to the end the first time
    start_to_end = find_fastest_route_bfs(journey_bounds, all_blizzard_states, valley_bounds)
    
    # Perform a breadth-first search through the valley to find the lowest number of moves required
    # to go from the end back to the start
    start_to_end_and_back = find_fastest_route_bfs(journey_bounds[::-1], all_blizzard_states,
                                                   valley_bounds, start_to_end)
    
    # Perform a breadth-first search through the valley to find the lowest number of moves required
    # to go from the start to the end the second time
    start_to_end_and_back_and_back = find_fastest_route_bfs(journey_bounds, all_blizzard_states,
                                                            valley_bounds, start_to_end_and_back)

    return start_to_end, start_to_end_and_back_and_back
