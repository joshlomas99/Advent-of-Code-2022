def get_input(input_file: str='Inputs/Day14_Inputs.txt') -> list:
    """
    Parse an input file giving the boundaries of sets of lines of rocks in a cave.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the rock boundaries.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    rock_boundaries : list
        List of the extracted boundaries as tuples.

    """
    # Parse input file
    file = open(input_file)
    rock_boundaries = []
    for line in file:
        line = line.strip().split(' -> ')
        if len(line) > 0:
            # Split up and format the coordinates
            rock_boundaries.append([tuple(int(i) for i in coords.split(',')) for coords in line])

    file.close()

    return rock_boundaries

def Day14_Part1(input_file: str='Inputs/Day14_Inputs.txt') -> int:
    """
    Determine the total number of units of sand which can fall into a cave and come to rest on a
    set of rock walls, the boundaries of which are given in an input file, until every proceeding
    piece of sand falls below the rocks into an abyss. A unit of sand always falls down one step if
    possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts
    to instead move diagonally one step down and to the left. If that tile is blocked, the unit of
    sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as
    long as it is able to do so, at each step trying to move down, then down-left, then down-right.
    If all three possible destinations are blocked, the unit of sand comes to rest and no longer
    moves, at which point the next unit of sand is created back at the source. The sand is pouring
    into the cave from point (500, 0).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the boundaries of the rock walls.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    total_sand : int
        The total number of units of sand which come to rest on the rocks.

    """
    ###############################################################################################
    # This was my original method with sets, although the grid method used in Part 2 would also
    # work way faster for this part, I just left it this way for comparison.
    ###############################################################################################
    # Parse input file
    rock_boundaries = get_input(input_file)
    # Create a set for the rocks and one for the sand
    all_rocks = set()
    all_sand = set()
    for boundary in rock_boundaries:
        # Construct the rock walls, adding each contained rock to the set
        for i in range(len(boundary) - 1):
            if boundary[i][0] == boundary[i+1][0]:
                for k in range(min(boundary[i][1], boundary[i+1][1]),
                               max(boundary[i][1], boundary[i+1][1]) + 1):
                    all_rocks.add((boundary[i][0], k))
            elif boundary[i][1] == boundary[i+1][1]:
                for k in range(min(boundary[i][0], boundary[i+1][0]),
                               max(boundary[i][0], boundary[i+1][0]) + 1):
                    all_rocks.add((k, boundary[i][1]))
    
    # Store the highest y value sand can have before it falls into the abyss
    y_max = max([coord[1] for coord in all_rocks])
    sand_source = (500, 0)
    
    curr_sand = (sand_source[0], sand_source[1])
    while curr_sand[1] < y_max: # While sand is not falling into the abyss
        if (curr_sand[0], curr_sand[1]+1) not in all_rocks.union(all_sand):
            # Attempt to move down
            curr_sand = (curr_sand[0], curr_sand[1]+1)
        elif (curr_sand[0]-1, curr_sand[1]+1) not in all_rocks.union(all_sand):
            # Attempt to instead move diagonally one step down and to the left
            curr_sand = (curr_sand[0]-1, curr_sand[1]+1)
        elif (curr_sand[0]+1, curr_sand[1]+1) not in all_rocks.union(all_sand):
            # Attempt to instead move diagonally one step down and to the right
            curr_sand = (curr_sand[0]+1, curr_sand[1]+1)
        else:
            # Else come to rest, add this sand to the set
            all_sand.add(curr_sand)
            curr_sand = (sand_source[0], sand_source[1])

    # Length of sand set is number of units of sand at rest by the end
    total_sand = len(all_sand)
    return total_sand

def Day14_Part2(input_file: str='Inputs/Day14_Inputs.txt') -> int:
    """
    Determine the total number of units of sand which can fall into a cave and come to rest on a
    set of rock walls, the boundaries of which are given in an input file, until the source of the
    sand becomes blocked. A unit of sand always falls down one step if possible. If the tile
    immediately below is blocked (by rock or sand), the unit of sand attempts to instead move
    diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts
    to instead move diagonally one step down and to the right. Sand keeps moving as long as it is
    able to do so, at each step trying to move down, then down-left, then down-right. If all three
    possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which
    point the next unit of sand is created back at the source. The sand is pouring into the cave
    from point (500, 0). Instead of sand falling into an abyss, there is now an infinite horizontal
    line with a y coordinate equal to two plus the highest y coordinate of the lowest rock in the
    cave.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the boundaries of the rock walls.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    total_sand : int
        The total number of units of sand which come to rest on the rocks before the source is
        blocked.

    """
    # Parse input file
    rock_boundaries = get_input(input_file)
    # Create a grid initially full of air, 200 deep in y and 400 wide in x, since I know the y_max
    # of the cave is less than 200, and the resulting pyramid of sand will be at most 2*y_max wide
    # Also using a shifted coordinate system with the sand source at (200, 0) to allow the grid to
    # be smaller while indexing simply.
    grid = [['AIR' for i in range(400)] for j in range(200)]
    for boundary in rock_boundaries:
        # Construct the rock walls, setting each contained point to a rock in the grid
        for i in range(len(boundary) - 1):
            if boundary[i][0] == boundary[i+1][0]:
                for k in range(min(boundary[i][1], boundary[i+1][1]),
                               max(boundary[i][1], boundary[i+1][1]) + 1):
                    grid[k][boundary[i][0] - 300] = 'ROCK' # (using shifted coordinates)
            elif boundary[i][1] == boundary[i+1][1]:
                for k in range(min(boundary[i][0], boundary[i+1][0]),
                               max(boundary[i][0], boundary[i+1][0]) + 1):
                    grid[boundary[i][1]][k - 300] = 'ROCK' # (using shifted coordinates)
    
    # Create horizontal rock floor 2 rows below lowest rocks
    y_max = max([i for i in range(len(grid)) if 'ROCK' in grid[i]])
    grid[y_max + 2] = ['ROCK' for i in range(400)]

    # Sand source at (200, 0) in this shifted coordinate system
    sand_source = (200, 0)
    
    curr_sand = (sand_source[0], sand_source[1])
    while grid[sand_source[1]][sand_source[0]] == 'AIR': # While the sand source is not blocked
        if grid[curr_sand[1] + 1][curr_sand[0]] == 'AIR':
            # Attempt to move down
            curr_sand = (curr_sand[0], curr_sand[1] + 1)
        elif grid[curr_sand[1] + 1][curr_sand[0] - 1] == 'AIR':
            # Attempt to instead move diagonally one step down and to the left
            curr_sand = (curr_sand[0] - 1, curr_sand[1] + 1)
        elif grid[curr_sand[1] + 1][curr_sand[0] + 1] == 'AIR':
            # Attempt to instead move diagonally one step down and to the right
            curr_sand = (curr_sand[0] + 1, curr_sand[1] + 1)
        else:
            # Else come to rest, set this point to sand to the grid
            grid[curr_sand[1]][curr_sand[0]] = 'SAND'
            curr_sand = (sand_source[0], sand_source[1])

    # Count total number of sand points in the grid at the end
    total_sand = sum([line.count('SAND') for line in grid])
    return total_sand
