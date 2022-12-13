import numpy as np

def get_input(input_file: str='Inputs/Day12_Inputs.txt') -> list:
    """
    Parse an input file giving the elevation of each square in a grid as a letter, with "a" being
    the lowest point and "z" the highest. Start (S) and end (E) squares are also marked, with
    heights "a" and "z" respectively.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the elevations of the grid squares.
        The default is 'Inputs/Day12_Inputs.txt'.

    Returns
    -------
    elevation : numpy.ndarray(int)
        2D array of the elevation of the grid squares.

    start : tuple
        Coordinates of the start square in the grid.

    end : tuple
        Coordinates of the end square in the grid.

    """
    # Parse input file
    file = open(input_file)
    # Start y (row) at 0
    elevation, y = [], 0
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            line = line[0]
            if 'S' in line: # If start point is in line
                # Store location
                start = (y, line.index('S'))
                # Replace with real height
                line = line.replace('S', 'a')
            if 'E' in line: # If end point is in line
                # Store location
                end = (y, line.index('E'))
                # Replace with real height
                line = line.replace('E', 'z')
            # Separate out row and convert letters to integer heights
            elevation.append([ord(c) - 97 for c in line])
            # Increment row
            y += 1

    file.close()

    return np.array(elevation), start, end

def Day12_Part1(input_file: str='Inputs/Day12_Inputs.txt') -> int:
    """
    Calculate the distance of the shortest possible route between given start and end squares on
    a grid, where the elevation of each square is given in an input file. Routes can only move
    between adjacent square, and the elevation of the destination square can be at most one higher
    than the elevation of your current square, but can be any amount lower.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the elevations of the grid squares.
        The default is 'Inputs/Day12_Inputs.txt'.

    Returns
    -------
    shortest_distance : int
        The distance of the shortest possible route between the start and end squares.

    """
    # Parse input file
    elevation, start, end = get_input(input_file)
    # Initialise each point on the grid with an impossibly large distance from the start
    distance = {(y, x): 10000 for x in range(len(elevation[0])) for y in range(len(elevation))}

    # Initialise list of the heads of potential routes, with only the start point
    heads = [start]
    # Set starting distance to 0
    distance[start] = 0
    while len(heads) > 0: # While potential routes are yet to be fully explored
        new_heads = []
        for curr_pos in heads: # For each open route
            # For each adjacent point to the current square
            for next_pos in [(curr_pos[0]+1, curr_pos[1]), (curr_pos[0], curr_pos[1]+1),
                                (curr_pos[0]-1, curr_pos[1]), (curr_pos[0], curr_pos[1]-1)]:
                # Check if point is not beyond the edge of the grid
                if next_pos[0] >= 0 and next_pos[0] < len(elevation) and \
                    next_pos[1] >= 0 and next_pos[1] < len(elevation[0]):
                    # If the elevation of the next point is no more than 1 higher than the current
                    if elevation[next_pos] - elevation[curr_pos] <= 1:
                        # If this is the shortest route so far discovered to this point
                        if distance[curr_pos] + 1 < distance[next_pos]:
                            # Set the distance to the next point to the new value
                            distance[next_pos] = distance[curr_pos] + 1
                            # Add the next point to the new list of open routes
                            new_heads.append(next_pos)
        # Reset heads to new list of open routes
        heads = new_heads.copy()

    # Find final distance to end point
    shortest_distance = distance[end]

    return shortest_distance

def Day12_Part2(input_file: str='Inputs/Day12_Inputs.txt') -> int:
    """
    Calculate the distance of the shortest possible route between any square of lowest elevation
    and a given end square of highest elevation on a grid, where the elevation of each square is
    given in an input file. Routes can only move between adjacent square, and the elevation of the
    destination square can be at most one higher than the elevation of your current square, but
    can be any amount lower.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the elevations of the grid squares.
        The default is 'Inputs/Day12_Inputs.txt'.

    Returns
    -------
    shortest_distance : int
        The distance of the shortest possible route between the a square of lowest elevation and
        the end point.

    """
    ########################################
    #### This is just Part 1 in reverse ####
    ########################################
    # Parse input file
    elevation, start, end = get_input(input_file)
    # Initialise each point on the grid with an impossibly large distance from the end
    distance = {(y, x): 10000 for x in range(len(elevation[0])) for y in range(len(elevation))}

    # Initialise list of the heads of potential routes, with only the end point
    heads = [end]
    # Set distance to end square to 0
    distance[end] = 0
    while len(heads) > 0: # While potential routes are yet to be fully explored
        new_heads = []
        for curr_pos in heads: # For each open route
            # For each adjacent point to the current square
            for next_pos in [(curr_pos[0]+1, curr_pos[1]), (curr_pos[0], curr_pos[1]+1),
                                (curr_pos[0]-1, curr_pos[1]), (curr_pos[0], curr_pos[1]-1)]:
                # Check if point is not beyond the edge of the grid
                if next_pos[0] >= 0 and next_pos[0] < len(elevation) and \
                    next_pos[1] >= 0 and next_pos[1] < len(elevation[0]):
                    # If the elevation of the next point is no less than 1 higher than the current
                    if elevation[curr_pos] - elevation[next_pos] <= 1:
                        # If this is the shortest route so far discovered to this point
                        if distance[curr_pos] + 1 < distance[next_pos]:
                            # Set the distance to the next point to the new value
                            distance[next_pos] = distance[curr_pos] + 1
                            # Add the next point to the new list of open routes
                            new_heads.append(next_pos)
        # Reset heads to new list of open routes
        heads = new_heads.copy()

    # Find shortest distance from end square to any start square with the lowest possible elevation
    shortest_distance = min([distance[point] for point in distance if elevation[point] == 0])

    return shortest_distance
