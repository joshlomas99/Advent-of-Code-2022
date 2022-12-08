import numpy as np

def get_input(input_file: str='Inputs/Day8_Inputs.txt') -> np.ndarray:
    """
    Parse an input file containing the heights of trees in a 100 x 100 grid.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the tree heights.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    trees : np.ndarray
        2D numpy array of the tree heights.

    """
    # Parse input file
    file = open(input_file)
    trees = []
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            # Split up each row and convert tree heights to integers
            trees.append([int(height) for height in line[0]])

    file.close()

    return np.array(trees)

def Day8_Part1(input_file: str='Inputs/Day8_Inputs.txt') -> int:
    """
    Calculates the number of trees in a grid, whose heights are given in an input file, which are
    visible from outside the grid.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the tree heights.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    visible : int
        The number of trees visible from outside the grid.

    """
    # Parse input file
    trees = get_input(input_file)

    # Count all edge trees first (-4 to avoid double counting corners)
    visible = 2*(len(trees)+len(trees[0])) - 4
    # For all interior trees
    for y in range(1, len(trees)-1):
        for x in range(1, len(trees[0])-1):
            # Check if, in any of the four directions, the tallest of the trees until the edge are
            # smaller than the current tree, meaning the current tree is visible
            visible += any(trees[y, x] > max(i) \
                           for i in [trees[:y, x], trees[y+1:, x], trees[y, :x], trees[y, x+1:]])
    
    return visible


def Day8_Part2(input_file: str='Inputs/Day8_Inputs.txt') -> int:
    """
    Calculates the highest scenic score possible for any tree in a 100 x 100 grid, whose heights
    are given in an input file, where the scenic score for a given is calculated as the product
    of the number of trees visible in each direction from that tree, i.e. the number of trees
    in a given direction until a tree the same height as or taller than the current tree is found.
    (If a tree is right on the edge, at least one of its viewing distances will be zero.)

    Parameters
    ----------
    input_file : str, optional
        Input file containing the tree heights.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    max_score : int
        The highest possible scenic score for any tree in the grid.

    """
    # Parse input file
    trees = get_input(input_file)
    scenic_score = []
    # For each tree
    for y in range(len(trees)):
        for x in range(len(trees[0])):
            # Find indices of trees in a given direction whose heights are >= the current tree's
            ind_left = np.where(trees[y, :x] >= trees[y, x])[0]
            if len(ind_left) > 0:
                # If any trees are found, find the number of trees until the closest one is reached
                left = x - max(ind_left)
            else:
                # Else find the number of trees until the edge of the grid
                left = 1*x

            # Repeat for the other three directions...
            ind_right = np.where(trees[y, x+1:] >= trees[y, x])[0]
            if len(ind_right) > 0:
                right = min(ind_right) + 1
            else:
                right = len(trees[y, :]) - 1 - x

            ind_up = np.where(trees[:y, x] >= trees[y, x])[0]
            if len(ind_up) > 0:
                up = y - max(ind_up)
            else:
                up = 1*y

            ind_down = np.where(trees[y+1:, x] >= trees[y, x])[0]
            if len(ind_down) > 0:
                down = min(ind_down) + 1
            else:
                len(trees[:, x]) - 1 - y

            # Calculate corresponding score
            scenic_score.append(left*right*up*down)

    # Find the maximum score
    max_score = max(scenic_score)

    return max_score
