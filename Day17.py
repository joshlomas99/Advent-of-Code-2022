def get_input(input_file: str='Inputs/Day17_Inputs.txt') -> list:
    """
    Parse an input file describing the directions of a series of jets of hot gas in a cave.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the jet directions.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    jets : str
        The extracted string of jet directions.

    """
    # Parse input file
    with open(input_file) as f:
        jets = f.readlines()[0].strip()

    return jets

def draw_cave(stopped, moving={}, max_rows=None):
    """
    Draw a cave and all the rocks currently in it, both stopped and moving.

    Parameters
    ----------
    stopped : set(tuple(int, int))
        Set of the coordinates (x, y) of stopped rocks.
    moving : set(tuple(int, int)), optional
        Set of the coordinates (x, y) of moving rocks.
        The default is {}.
    max_rows : int, str or NoneType, optional
        If int n: n rows from the highest rock in the cave are printed.
        If str 'Bottom': rows will be printed from the top until every column contains at least
        one rock.
        If NoneType None: all rows are printed.
        The default is None.

    Returns
    -------
    None.

    """
    # Calculate the number of rows below the highest rock in the cave
    max_height = max([c[1] for c in stopped.union(moving)])
    # If max_rows == None then print all rows
    if not max_rows:
        max_rows = max_height + 1
    # If max_rows == 'Bottom', find the max row such that every column contains >0 rocks
    elif max_rows == 'Bottom':
        max_rows = max_height + 1 - min(max(c[1] for c in stopped if c[0] == j) for j in range(7))

    # Print the required number rows
    for height in range(max(0, max_height+1-max_rows), max_height+1)[::-1]:
        # Print stopped rocks as '#', moving as '@' and air as '.'
        print_line = ['@' if (width, height) in moving \
                      else '#' if (width, height) in stopped \
                      else '.' for width in range(7)]
        # Add the walls either side of each row
        print('|' + ''.join(print_line) + '|')
    # Add the floor at the bottom
    print('+-------+')

def process_rock_fall(base_rock, stopped, jets, jet_index):
    """
    Simulate a single rock of a given type, falling into a cave containing a given set of stopped
    rocks, which is pushed horizontally as it falls by a given series of jet of hot air and stops
    once it hits another stopped rock (or the floor) vertically.

    Rock Movement
    -------------
    The cave is seven units wide. Each rock appears so that its left edge is two units away from
    the left wall and its bottom edge is three units above the highest rock in the cave (or the
    floor, if there are no rocks).

    Rocks are pushed horizontally as they fall by jets according to a string of '>' and '<' symbols
    which is moved through in order. '<' indicates a movement one unit to the left, '>' indicates
    a movement one unit to the right. If the end of the list is reached, it repeats.

    After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the
    direction indicated by the next symbol in the jet pattern) and then falling one unit down. If
    any movement would cause any part of the rock to move into the walls, floor, or a stopped rock,
    the movement instead does not occur. If a downward movement would have caused a falling rock to
    move into the floor or a stopped rock, the falling rock stops where it is.

    Parameters
    ----------
    base_rock : set(tuple(int, int))
        Set of coordinates describing the type of rock falling into the cave, if there were no
        other rocks in the cave and so it appeared three units above the floor.
    stopped : set(tuple(int, int))
        Set of the coordinates (x, y) of stopped rocks.
    jets : str
        The string of characters giving the direction of each jet acting on the rock, in order.
    jet_index : int
        The index in `jets` of the first jet which should act on the new rock.

    Returns
    -------
    stopped : set(tuple(int, int))
        Set of the coordinates (x, y) of stopped rocks after the new rock has finished falling.
    jet_index : int
        The index in `jets` of the next jet which will occur after the new rock has finished
        falling.
    jets_wrap : bool
        Whether the end of the list of jet directions was reached during the fall of this rock,
        causing the jet_index to wrap back to zero.

    """
    # Calculate the height at which the bottom of the new rock should appear
    spawn_height = max([c[1] for c in stopped]) + 4
    # Calculate the coordinates of the rock where it appears
    rock = {(c[0], c[1] + spawn_height - 3) for c in base_rock}
    # jet_wrap starts as False
    jets_wrap = False
    # Until the rock stops, where a return occurs
    while True:
        ### Horizontal Movement ###
        # Convert the jet direction symbol into a unit of horizontal movement
        horizontal_move = ord(jets[jet_index]) - 61
        # Find the next position of the rock after the horizontal movement
        next_pos = {(c[0] + horizontal_move, c[1]) for c in rock}
        # If this would cause the rock to move into the walls, or a stopped rock, don't perform
        # the movement
        if any(c[0] < 0 or c[0] > 6 for c in next_pos) or next_pos.intersection(stopped):
            pass
        else:
            # Else perform the movement, setting the new rock position
            rock = next_pos.copy()
        # Increment the jet index
        jet_index += 1
        # If the end of the jets list is reached, wrap to the beginning and set jets_wrap to True
        if jet_index >= len(jets):
            jet_index %= len(jets)
            jets_wrap=True

        ### Vertical Movement ###
        # Find the next position of the rock after the vertical movement one unit down
        next_pos = {(c[0], c[1] - 1) for c in rock}
        # If this would cause the rock to move into the floor or a stopped rock:
        if next_pos.intersection(stopped):
            # Add the rock's position before this movement to 'stopped' and return
            stopped = stopped.union(rock)
            return stopped, jet_index, jets_wrap
        else:
            # Else perform the movement, setting the new rock position, and continue
            rock = next_pos.copy()

def Day17_Part1(input_file: str='Inputs/Day17_Inputs.txt', total_rocks=2022) -> int:
    """
    Find the total height of the tower formed by a series of rocks falling into a cave, after a
    given number of rocks have stopped. Rocks appear in the cave and then fall down, and are also
    moved horizontally by a series of jets, whose directions are given in an input file. There are
    five types of rocks, described below, which appear in the order given, which then repeats until
    the given number of rocks have fallen.

    Rock Types
    ----------
    The five different types of rocks are shown below, with ``#`` representing rock and ``.``
    representing air:

    Horizontal line::

        ####

    Cross::

        .#.
        ###
        .#.

    Backwards L::

        ..#
        ..#
        ###

    Vertical line::

        #
        #
        #
        #

    Box::

        ##
        ##

    Rock Movement
    -------------
    The cave is seven units wide. Each rock appears so that its left edge is two units away from
    the left wall and its bottom edge is three units above the highest rock in the cave (or the
    floor, if there are no rocks).

    Rocks are pushed horizontally as they fall by jets according to a string of '>' and '<' symbols
    which is moved through in order. '<' indicates a movement one unit to the left, '>' indicates
    a movement one unit to the right. If the end of the list is reached, it repeats.

    After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the
    direction indicated by the next symbol in the jet pattern) and then falling one unit down. If
    any movement would cause any part of the rock to move into the walls, floor, or a stopped rock,
    the movement instead does not occur. If a downward movement would have caused a falling rock to
    move into the floor or a stopped rock, the falling rock stops where it is.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the jet directions.
        The default is 'Inputs/Day17_Inputs.txt'.
    total_rocks : int, optional
        The total number of rocks which fall into the cave.
        The default is 2022.

    Returns
    -------
    total_height : int
        The total height of the rock tower after the given number of rocks have fallen.

    """
    # Parse input file to get list of jet directions
    jets = get_input(input_file)

    # Set up the five base types of rocks as sets of coordinates describing the rocks as if there
    # are no other rocks in the cave and so they appear three units above the floor
    rocks = [
        # horizontal line
        {(2, 3), (3, 3), (4, 3), (5, 3)},
        # cross
        {(2, 4), (3, 3), (3, 4), (3, 5), (4, 4)},
        # l shape
        {(2, 3), (3, 3), (4, 3), (4, 4), (4, 5)},
        # vertical line
        {(2, 3), (2, 4), (2, 5), (2, 6)},
        # box
        {(2, 3), (3, 3), (2, 4), (3, 4)}
    ]

    # Initialise the set of stopped rocks with the floor coordinates
    stopped = {(width, -1) for width in range(7)}
    # Start the index of the jet directions at 0
    jet_index = 0

    # For each new rock
    for rock_number in range(total_rocks):
        # Simulate the rock falling into the cave and stopping, finding the new set of stopped
        # rocks and the next jet index each time
        stopped, jet_index, _ = process_rock_fall(rocks[rock_number%len(rocks)], stopped, jets,
                                                  jet_index)

    # Find the height of the highest rock in the cave (+1 since the y coordinate starts at zero)
    total_height = max([c[1] for c in stopped]) + 1

    return total_height

def Day17_Part2(input_file: str='Inputs/Day17_Inputs.txt', total_rocks=1000000000000) -> int:
    """
    Find the total height of the tower formed by a series of rocks falling into a cave, after a
    given number of rocks have stopped. Rocks appear in the cave and then fall down, and are also
    moved horizontally by a series of jets, whose directions are given in an input file. There are
    five types of rocks, described below, which appear in the order given, which then repeats until
    the given number of rocks have fallen.

    Now using an estimation to allow enormous number of rocks to be simulated. This takes advantage
    of the fact that the jet directions and rock types both wrap back to the start eventually, so
    a pattern will inevitably form in height gained per rocks added, allowing a large amount of the
    actual simulation to be skipped.

    Rock Types
    ----------
    The five different types of rocks are shown below, with ``#`` representing rock and ``.``
    representing air:

    Horizontal line::

        ####

    Cross::

        .#.
        ###
        .#.

    Backwards L::

        ..#
        ..#
        ###

    Vertical line::

        #
        #
        #
        #

    Box::

        ##
        ##

    Rock Movement
    -------------
    The cave is seven units wide. Each rock appears so that its left edge is two units away from
    the left wall and its bottom edge is three units above the highest rock in the cave (or the
    floor, if there are no rocks).

    Rocks are pushed horizontally as they fall by jets according to a string of '>' and '<' symbols
    which is moved through in order. '<' indicates a movement one unit to the left, '>' indicates
    a movement one unit to the right. If the end of the list is reached, it repeats.

    After a rock appears, it alternates between being pushed by a jet of hot gas one unit (in the
    direction indicated by the next symbol in the jet pattern) and then falling one unit down. If
    any movement would cause any part of the rock to move into the walls, floor, or a stopped rock,
    the movement instead does not occur. If a downward movement would have caused a falling rock to
    move into the floor or a stopped rock, the falling rock stops where it is.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the jet directions.
        The default is 'Inputs/Day17_Inputs.txt'.
    total_rocks : int, optional
        The total number of rocks which fall into the cave.
        The default is 1000000000000.

    Returns
    -------
    total_height : int
        The total height of the rock tower after the given number of rocks have fallen.

    """
    # Parse input file to get list of jet directions
    jets = get_input(input_file)

    # Set up the five base types of rocks as sets of coordinates describing the rocks as if there
    # are no other rocks in the cave and so they appear three units above the floor
    rocks = [
        # horizontal line
        {(2, 3), (3, 3), (4, 3), (5, 3)},
        # cross
        {(2, 4), (3, 3), (3, 4), (3, 5), (4, 4)},
        # l shape
        {(2, 3), (3, 3), (4, 3), (4, 4), (4, 5)},
        # vertical line
        {(2, 3), (2, 4), (2, 5), (2, 6)},
        # box
        {(2, 3), (3, 3), (2, 4), (3, 4)}
    ]

    # Initialise the set of stopped rocks with the floor coordinates
    stopped = {(width, -1) for width in range(7)}
    # Start the index of the jet directions at 0
    jet_index = 0
    # Now using a while loop so initialise rock_number at 0
    rock_number = 0
    # Count the number of times the jet directions have wrapped around
    jet_wraps = 0
    # Track the last rock to fall, current rock_number, total height of the rocks, increase in
    # rock_number and increase in height between times the jet direction wraps around
    last_rocks, rock_nums, heights, rock_diffs, height_diffs = [], [], [], [], []

    # Loop until a pattern is found, where a break occurs
    while True:
        # Simulate the rock falling into the cave and stopping, finding the new set of stopped
        # rocks, the next jet index and whether the jet directions wrapped around each time
        stopped, jet_index, jets_wrap = process_rock_fall(rocks[rock_number%len(rocks)], stopped,
                                                          jets, jet_index)
        # Increment rock_number
        rock_number += 1

        # If the jets wrapped around during the last rock fall
        if jets_wrap:
            # Unless this is the very first jet wrap
            if jet_wraps > 0:
                # Record the current number of rocks that have fallen
                rock_nums.append(rock_number)
                # Record the current height of the rock tower
                heights.append(max([c[1] for c in stopped]) + 1)
                # If this is the second jet wrap, the pattern should now start, since the initial
                # anomalous effect of the floor has now been phased out
                if jet_wraps == 1:
                    # So record the current number of rocks and height of the tower before the
                    # pattern started
                    pre_wrap_rock_number, pre_wrap_height_gain = rock_nums[-1], heights[-1]
            # If there have been at least two jet wraps, so the pattern should have started
            if jet_wraps > 1:
                # Record which type of rock was the last to fall before this jet wrap
                last_rocks.append((rock_number-1)%len(rocks))
                # Record the increase in the number of rocks since the last jet wrap
                rock_diffs.append(rock_nums[-1] - rock_nums[-2])
                # Record the increase in the height of the rock tower since the last jet wrap
                height_diffs.append(heights[-1] - heights[-2])
                # Only worth checking for the pattern to have repeated (happened twice) every two
                # jet wraps
                if len(last_rocks)%2 == 0:
                    # Check if the whole system has repeated twice:
                    # The type and number of rocks falling and the same height increases each
                    # jet wrap
                    if last_rocks[:len(last_rocks)//2] == last_rocks[len(last_rocks)//2:] and \
                       rock_diffs[:len(rock_diffs)//2] == rock_diffs[len(rock_diffs)//2:] and \
                       height_diffs[:len(height_diffs)//2] == height_diffs[len(height_diffs)//2:]:
                        # If these are all the same, we have found the pattern, so record the total
                        # number of rocks and the total height increase for one round of the pattern
                        wrap_rock_number = sum(rock_diffs[:len(rock_diffs)//2])
                        wrap_height_gain = sum(height_diffs[:len(height_diffs)//2])
                        # Break the while loop
                        break
    
            # Increment the number of jet wraps
            jet_wraps += 1

    # Find the number of rocks left to fall at the start of the first pattern
    total_rocks -= pre_wrap_rock_number
    # Find the number of times the pattern can repeat before enough rocks have fallen
    number_of_wraps = total_rocks//wrap_rock_number
    # Find the increase in height from all these wraps of the pattern
    height_gain_from_wraps = (number_of_wraps*wrap_height_gain)
    # Find the number of rocks still to fall at the end of the last pattern
    rocks_left = total_rocks%wrap_rock_number
    # Find the height of the tower before the final rocks are added (since continuing to add to the
    # tower created finding the pattern is equivalent to using the tower at the end of any number
    # of pattern repetitions, so we can just continue adding to 'stopped' here as it is)
    pre_final_loop_height = max([c[1] for c in stopped]) + 1
    # For the rocks that are still to fall
    for i in range(rocks_left):
        # Simulate the final rocks falling
        stopped, jet_index, _ = process_rock_fall(rocks[(rock_number + i)%len(rocks)],
                                                  stopped, jets, jet_index)

    # Find the height added to the tower by the final set of rocks
    final_loop_height_gain = (max([c[1] for c in stopped]) + 1) - pre_final_loop_height

    # Add together the different components to find the final total rock tower height
    total_height = pre_wrap_height_gain + height_gain_from_wraps + final_loop_height_gain

    return total_height
