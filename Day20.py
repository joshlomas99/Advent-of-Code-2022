def get_input(input_file: str='Inputs/Day20_Inputs.txt', key: int=1) -> list:
    """
    Parse an input file to extract a list of numbers, and multiply each number by a given key.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the numbers.
        The default is 'Inputs/Day20_Inputs.txt'.
    key : int, optional
        Key by which to multiply every number.
        The default is 1.

    Returns
    -------
    values : list
        List of extracted values multiplied by the key.

    """
    # Parse input file
    with open(input_file) as f:
        # Convert each value to int and multiply by key
        values = [int(line.strip())*key for line in f.readlines()]

    return values

def mixing(values: list, rounds: int=1) -> list:
    """
    Apply a mixing procedure to a list of numbers, whereby each number is moved forward or backward
    in the list a number of positions equal to the value of the number being moved. The list is
    circular, so moving a number off one end of the list wraps back around to the other end as if
    the ends were connected. The numbers are moved in the order they originally appear in the list.

    Parameters
    ----------
    values : list
        The list of values to mix.
    rounds : int, optional
        The number of times the mixing procedure should be applied to the list from start to finish,
        although the order in which the numbers are mixed does not change between rounds.
        The default is 1.

    Returns
    -------
    new_values : list
        The list of values after mixing.

    """
    # Create list of the original positions of values
    positions = list(range(len(values)))
    # For each round
    for i in range(rounds):
        # For each initial position, in order
        for pos in range(len(values)):
            # Find the current position of that value
            curr_pos = positions.index(pos)
            # Apply mixing to find the new position of the value
            new_pos = (curr_pos + values[pos] - 1)%(len(values) - 1) + 1
            # Rebuild the list, removing the value from its current positions and inserting it in
            # the new position
            if new_pos > curr_pos:
                positions = positions[:curr_pos] + positions[curr_pos+1: new_pos+1] + [pos] + positions[new_pos+1:]
            elif new_pos < curr_pos:
                positions = positions[:new_pos] + [pos] + positions[new_pos:curr_pos] + positions[curr_pos+1:]

    # Rerieve the values corresponding to each initial position
    new_values = [values[p] for p in positions]

    return new_values

def Day20_Part1(input_file: str='Inputs/Day20_Inputs.txt') -> int:
    """
    Find the sum of the grove coordinates extracted from a list of values, after it has been
    decrypted through the application of a mixing prodedure. Once decrypted, the grove coordinates
    can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0, wrapping
    around the list as necessary.

    Mixing Procedure
    ----------------
    Each number in the list is moved forward or backward a number of positions equal to the value
    of the number being moved. The list is circular, so moving a number off one end of the list
    wraps back around to the other end as if the ends were connected. The numbers are moved in the
    order they originally appear in the list.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the encrypted list of values.
        The default is 'Inputs/Day20_Inputs.txt'.

    Returns
    -------
    number_sum : int
        The sum of the grove coordinates extracted from the decrypted list of values.

    """
    # Parse input file to extract values
    values = get_input(input_file)

    # Apply one round of the mixing procedure
    values = mixing(values)

    # Find current position of the value 0 and sum the corresponding grove coordinates
    zero_index = values.index(0)
    number_sum = sum(values[(zero_index + add)%len(values)] for add in [1000, 2000, 3000])

    return number_sum

def Day20_Part2(input_file: str='Inputs/Day20_Inputs.txt', key: int=811589153) -> int:
    """
    Find the sum of the grove coordinates extracted from a list of values, after it has been
    decrypted by multiplying every value by a given decryption key and applying 10 rounds of a
    mixing prodedure. Once decrypted, the grove coordinates can be found by looking at the 1000th,
    2000th, and 3000th numbers after the value 0, wrapping around the list as necessary.

    Mixing Procedure
    ----------------
    Each number in the list is moved forward or backward a number of positions equal to the value
    of the number being moved. The list is circular, so moving a number off one end of the list
    wraps back around to the other end as if the ends were connected. The numbers are moved in the
    order they originally appear in the list.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the encrypted list of values.
        The default is 'Inputs/Day20_Inputs.txt'.
    key : int, optional
        The decryption key by which to multiply every number.
        The default is 811589153.

    Returns
    -------
    number_sum : int
        The sum of the grove coordinates extracted from the decrypted list of values.

    """
    # Parse input file to extract values, multiplied by the given key
    values = get_input(input_file, key)

    # Apply ten rounds of the mixing procedure
    values = mixing(values, 10)

    # Find current position of the value 0 and sum the corresponding grove coordinates
    zero_index = values.index(0)
    number_sum = sum(values[(zero_index + add)%len(values)] for add in [1000, 2000, 3000])
    
    return number_sum
