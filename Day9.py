import numpy as np

def get_input(input_file: str='Inputs/Day9_Inputs.txt') -> list:
    """
    Parse an input file containing a list of movements for one end of a rope in the form:
    direction, distance, where distance can be U, D, L or R for up, down, left and right
    respectively.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the movements.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    moves : list(list(str, int))
        A list of the extracted movements in the form: [direction(str), distance(int)].

    """
    # Parse input file
    file = open(input_file)
    moves = []
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            moves.append([line[0], int(line[1])])

    file.close()

    return moves

def Day9_Part1(input_file: str='Inputs/Day9_Inputs.txt') -> int:
    """
    Calculates how many positions the tail of a rope visits, as the head of the rope follows a set
    of movement instructions given in an input file. The tail must always stay adjacent to the head,
    either directly or diagonally, and they can overlap.

    Parameters
    ----------
    input_file : str, optional
        The input file giving the movement instructions for the head of the rope.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    number_of_pos : int
        The number of different positions visited by the tail.

    """
    # Parse input file
    moves = get_input(input_file)
    # Start head and tail at the same arbitrary point
    head_pos, tail_pos = [0, 0], [0, 0]
    all_tail_pos = set()
    for move in moves: # For each move of the head
        for i in range(move[1]): # For each step in each move
            # Move the head position in the given direction by one step
            if move[0] == 'U':
                head_pos[1] += 1
            if move[0] == 'D':
                head_pos[1] -= 1
            if move[0] == 'R':
                head_pos[0] += 1
            if move[0] == 'L':
                head_pos[0] -= 1
            # Calculate the separation in each axis of the head and tail of the rope
            separation = [[abs(tail_pos[i] - head_pos[i]) <= j for i in range(2)] for j in range(2)]
            if not all(separation[1]): # If they are <= 1 space from each other, do nothing
                if any(separation[0]): # Else if they are separated directly along an axis
                    # The tail follows the head in the same direction
                    i = separation[0].index(0)
                    tail_pos[i] += np.sign(head_pos[i] - tail_pos[i])
                else: # Else the tail must be 2 away in one axis, 1 in the other
                    # Move the tail back behind the head
                    j = separation[1].index(1)
                    tail_pos[j] = 1*head_pos[j]
                    tail_pos[(j+1)%2] += np.sign(head_pos[(j+1)%2] - tail_pos[(j+1)%2])
            # Add the new tail position to a set
            all_tail_pos.add(tuple(tail_pos))

    # Length of set is number of unique positions
    number_of_pos = len(all_tail_pos)
    
    return number_of_pos

def Day9_Part2(input_file: str='Inputs/Day9_Inputs.txt', output_path: bool=True) -> int:
    """
    Calculates how many positions the tail of a rope visits, as the head of the rope follows a set
    of movement instructions given in an input file. Now the tail is connected to the head via 8
    additional knots, which must always stay adjacent to the knot in front of them, either directly
    or diagonally, and they can overlap.

    Parameters
    ----------
    input_file : str, optional
        The input file giving the movement instructions for the head of the rope.
        The default is 'Inputs/Day9_Inputs.txt'.

    output_path : bool, optional
        Whether to print the full path of the tail to a file.
        The default is True.

    Returns
    -------
    number_of_pos : int
        The number of different positions visited by the tail.

    """
    # Parse input file
    moves = get_input(input_file)
    # Start each knot at the same arbitrary point
    knot_pos = [[0, 0] for i in range(10)]
    all_tail_pos = set()
    for move in moves: # For each move of the head
        for m in range(move[1]): # For each step in each move
            for n in range(len(knot_pos)): # For each knot in the rope
                if n == 0: # If the current knot is the head
                    # Move the head position in the given direction by one step
                    if move[0] == 'U':
                        knot_pos[0][1] += 1
                    if move[0] == 'D':
                        knot_pos[0][1] -= 1
                    if move[0] == 'R':
                        knot_pos[0][0] += 1
                    if move[0] == 'L':
                        knot_pos[0][0] -= 1
                else: # Else follow the previous knot
                    # Calculate the separation in each axis of the current and previous knot
                    separation = [[abs(knot_pos[n][i] - knot_pos[n-1][i]) <= j for i in range(2)] \
                                  for j in range(3)]
                    if not all(separation[1]): # If they are <= 1 space from each other, do nothing
                        if any(separation[0]): # Else if they are separated directly along an axis
                            # The knot follows the previous in the same direction
                            i = separation[0].index(0)
                            knot_pos[n][i] += np.sign(knot_pos[n-1][i] - knot_pos[n][i])
                        elif any(separation[1]):
                            # Else if the current and previous knots are 2 apart in one axis,
                            # 1 in the other
                            # Move the current knot back behind the previous one
                            j = separation[1].index(1)
                            knot_pos[n][j] = 1*knot_pos[n-1][j]
                            knot_pos[n][(j+1)%2] += np.sign(knot_pos[n-1][(j+1)%2] - knot_pos[n][(j+1)%2])
                        else:
                            # Else if the current and previous knots are separated by 2 in each
                            # axis (now possible) move current knot diagonally towards previous
                            for k in range(2):
                                knot_pos[n][k] += np.sign(knot_pos[n-1][k] - knot_pos[n][k])

                    if n == len(knot_pos) - 1: # If the current knot is the tail
                        # Add the new tail position to a set
                        all_tail_pos.add(tuple(knot_pos[n]))
    
    if output_path: # If selected, output full tail path to file 'Day9_TailPath.txt'
        file = open('Day9_TailPath.txt', 'w')
        for y in range(-62, 276)[::-1]:
            line = ''
            for x in range(-158, 48):
                if (x, y) in all_tail_pos:
                    line += '#'
                else:
                    line += '.'
            file.write(line + '\n')
        file.close()

    # Length of set is number of unique positions
    number_of_pos = len(all_tail_pos)
    
    return number_of_pos
