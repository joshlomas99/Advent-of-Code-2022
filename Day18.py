def get_input(input_file: str='Inputs/Day18_Inputs.txt') -> list:
    """
    Parse an input file containing the coordinates of 1x1x1 cubes making up a lava droplet.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the cube coordinates.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    cubes: list(tuple(int, int, int))
        List of cube coordinates as tuples of integers.

    """
    # Parse input file
    with open(input_file) as f:
        # Convert coordinates to tuples of ints
        cubes = [tuple(int(i) for i in line.strip().split(',')) for line in f.readlines()]

    return cubes

from itertools import combinations

def Day18_Part1(input_file: str='Inputs/Day18_Inputs.txt') -> int:
    """
    Calculates the number of cube faces which are not immediately connected to another cube in a
    lava droplet made up of a series of individual 1x1x1 cubes, whose coordinates are given in an
    input file.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the cube coordinates.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    exposed_faces : int
        The number of exposed (not connected to another cube) faces in the lava droplet.

    """
    # Parse input file to get coordinates of every cube
    cubes = get_input()

    # Find the total number of faces across every cube
    all_faces = len(cubes)*6

    # Find dx, dy and dz between each cube and every other cube, if one of these values is +/-1 and
    # the other two are 0 (sum of absolute values == 1) then the two cubes share a face, so add one
    # to the total common_faces
    common_faces = sum(sum(abs(cube_1[i] - cube_2[i]) for i in range(3)) == 1 \
                        for cube_1, cube_2 in combinations(cubes, 2))

    # Find number of exposed faces (need to double count common_faces since we are considering
    # every cube separately
    exposed_faces = all_faces - (common_faces*2)
    
    return exposed_faces

import numpy as np

def next_cubes(cube: tuple, bounds: tuple) -> list:
    """
    Find the coordinates of every immediately adjacent cube to a given cube, within set boundaries.

    Parameters
    ----------
    cube : tuple(int, int, int)
        The 3D coordinates of the cube to find the neighbours of, int the form (x, y, z).
    bounds : tuple(int, int)
        Tuple giving the boundaries of the cubes in the form tuple(min, max), i.e. the minimum and
        maximum possible cube coordinates in each axis.

    Returns
    -------
    next_cubes : list(tuple(int, int, int))
        List of coordinates of the neighbouring cubes to the given cube.

    """
    next_cubes = []

    # For each axis
    for i in range(3):
        # Create array of starting cube coordinates
        next_cube = np.array(cube)
        # Create array with 1 unit shift in current axis
        delta = np.zeros(3)
        delta[i] += 1
        # Check bounds for shift in positive direction
        if cube[i] + 1 <= bounds[1]:
            # If within bounds, append the new coordinates to output list
            next_cubes.append(tuple(int(i) for i in next_cube + delta))
        # Repeat for shift in negative direction
        if cube[i] - 1 >= bounds[0]:
            next_cubes.append(tuple(int(i) for i in next_cube - delta))

    return next_cubes

def Day18_Part2(input_file: str='Inputs/Day18_Inputs.txt') -> int:
    """
    Calculates the exterior surface area of a lava droplet made up of a series of individual 1x1x1
    cubes, whose coordinates are given in an input file. Air pockets entirely contained within the
    droplet are not included.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the cube coordinates.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    exterior_faces : int
        The exterior surface area of the lava droplet.

    """
    # Parse input file to get coordinates of every cube
    filled_cubes = get_input()

    # Find the minimum and maximum bounds required to encompass the entire lava droplet with a
    # layer of air around the outside
    bounds_min = min(c[i] for c in filled_cubes for i in range(3)) - 1
    bounds_max = max(c[i] for c in filled_cubes for i in range(3)) + 1

    # Use a breadth-first search to visit every cube of air around the outside of the droplet
    # Start at the minimum boundary corner of the cube
    start = (bounds_min, bounds_min, bounds_min)
    # Initialise queue and list of visited cubes
    queue, visited = [start], [start]
    
    bounds = (bounds_min, bounds_max)
    exterior_faces = 0

    # While there are cubes still to visit
    while queue:
        # Take the item at the front of the queue
        curr_cube = queue.pop(0)

        # For each of its neighbours, within the boundaries
        for next_cube in next_cubes(curr_cube, bounds):
            # If a neighbour is lava, add one to the number of exterior faces
            if next_cube in filled_cubes:
                exterior_faces += 1
            # Otherwise, add the new outer air cube to the queue and record as visited
            elif next_cube not in visited:
                visited.append(next_cube)
                queue.append(next_cube)

    return exterior_faces
