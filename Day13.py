def get_input(input_file: str='Inputs/Day13_Inputs.txt', group_pairs: bool=True) -> list:
    """
    Parse an input file containing pairs of data packets, which consist of nested lists and
    integers. Pairs are separated by a blank line.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the data packets.
        The default is 'Inputs/Day13_Inputs.txt'.
    group_pairs : bool, optional
        Whether to group each pair or just return a list of all data packets.
        The default is True.

    Returns
    -------
    pairs : list
        The extracted list of pairs of data packets.

    """
    # Parse input file
    file = open(input_file)
    if group_pairs:
        # If grouping pairs, initialise nested list for first pair
        pairs = [[]]
    else:
        # Else just need one list
        pairs = []
    for line in file:
        line = line.strip().split()
        if len(line) == 0:
            if group_pairs:
                # If grouping pairs, make a new list for each pair on blank lines
                pairs.append([])
        else:
            if group_pairs:
                # If grouping pairs, append packet to latest pair
                pairs[-1].append(eval(line[0]))
            else:
                # Else just append packet to list
                pairs.append(eval(line[0]))

    file.close()

    return pairs

import numpy as np

def compare_order(a, b):
    """
    Recursively compares two items, both can be either an integer or a list, to determine which
    order they should go in. If ``a`` should come first -1 is returned, if ``b`` should come first 1 is
    returned and if ``a == b`` then 0 is returned (to work with ``sorted`` function).

    Comparison Rules
    ----------------
    If both values are integers, the lower integer should come first. Otherwise, the inputs are
    the same integer; continue checking the next part of the input.

    If both values are lists, compare the first value of each list, then the second value, and so
    on. If these are all the same then the shorter list should come first. If the lists are the
    same length and no comparison makes a decision about the order, continue checking the next
    part of the input.

    If exactly one value is an integer, convert the integer to a list which contains that integer
    as its only value, then retry the comparison. For example, if comparing ``[0,0,0]`` and ``2``,
    convert the right value to ``[2]`` (a list containing ``2``); the result is then found by
    instead comparing ``[0,0,0]`` and ``[2]``.

    Parameters
    ----------
    a : list or int
        First item to be compared.
    b : list or int
        Second item to be compared.

    Returns
    -------
    comparison : int
        The result of the comparison.

    """
    # If both inputs are integers
    if type(a) == int and type(b) == int:
        # Return sign of difference -> -1 if a < b, 1 if a > b and 0 if a == b; as required
        return np.sign(a - b)

    # Else if both inputs are lists
    elif type(a) == list and type(b) == list:
        # Loop through contents of list up to length of shorter list
        for i in range(min([len(a), len(b)])):
            # Recursively compare list components
            check = compare_order(a[i], b[i])
            if not check:
                # If no decision has been made by these components, move on to the next
                continue
            else:
                # Else return the result
                return check
        # If the end of the shorter list is reached, return the comparison of the list lengths
        return np.sign(len(a) - len(b))

    # Else the inputs must be one integer and one list
    else:
        if type(a) == int:
            # If a is integer, convert to a list
            return compare_order([a], b)
        else:
            # Else convert b to a list
            return compare_order(a, [b])

def Day13_Part1(input_file: str='Inputs/Day13_Inputs.txt') -> int:
    """
    Determines the sum of the indicies of the pairs of data packets, given in an input file, which
    are in the correct order according to a set of rules. Data packets consist of nested lists and
    integers and pairs are separated by a blank line. The index of the first pair is 1, then 2...

    Comparison Rules
    ----------------
    If both values are integers, the lower integer should come first. If the left integer is lower
    than the right integer, the inputs are in the right order. If the left integer is higher than
    the right integer, the inputs are not in the right order. Otherwise, the inputs are the same
    integer; continue checking the next part of the input.

    If both values are lists, compare the first value of each list, then the second value, and so
    on. If the left list runs out of items first, the inputs are in the right order. If the right
    list runs out of items first, the inputs are not in the right order. If the lists are the same
    length and no comparison makes a decision about the order, continue checking the next part of
    the input.

    If exactly one value is an integer, convert the integer to a list which contains that integer
    as its only value, then retry the comparison. For example, if comparing ``[0,0,0]`` and ``2``,
    convert the right value to ``[2]`` (a list containing ``2``); the result is then found by
    instead comparing ``[0,0,0]`` and ``[2]``.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the pairs of data packets.
        The default is 'Inputs/Day13_Inputs.txt'.

    Returns
    -------
    right_order_sum : int
        The sum of the indices of all pairs in the input which are in the correct order.

    """
    # Parse input file
    pairs = get_input(input_file)
    
    right_order_sum = 0
    for index, pair in enumerate(pairs): # For each pair
        if compare_order(pair[0], pair[1]) < 0: # Comparison returns -1 for the correct order
            # If the order is correct, add the index (add 1 since enumerate starts with index 0
            # instead of 1)
            right_order_sum += index + 1
    
    return right_order_sum

from functools import cmp_to_key

def Day13_Part2(input_file: str='Inputs/Day13_Inputs.txt') -> int:
    """
    Determines decoder key of a distress signal, which is given by the product of the indices of
    divider packets [[2]] and [[6]] when they are inserted into a set of data packets, given in an
    input file, and the set is sorted according to a set of rules. Data packets consist of nested
    lists and integers. The index of the first pair is 1, then 2...

    Comparison Rules
    ----------------
    If both values are integers, the lower integer should come first. Otherwise, the inputs are
    the same integer; continue checking the next part of the input.

    If both values are lists, compare the first value of each list, then the second value, and so
    on. If these are all the same then the shorter list should come first. If the lists are the
    same length and no comparison makes a decision about the order, continue checking the next
    part of the input.

    If exactly one value is an integer, convert the integer to a list which contains that integer
    as its only value, then retry the comparison. For example, if comparing ``[0,0,0]`` and ``2``,
    convert the right value to ``[2]`` (a list containing ``2``); the result is then found by
    instead comparing ``[0,0,0]`` and ``[2]``.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the pairs of data packets.
        The default is 'Inputs/Day13_Inputs.txt'.

    Returns
    -------
    decoder_key : int
        The the product of the indices of the divider packets ([[2]] and [[6]]) in the sorted list
        of data packets.

    """
    # Parse input file
    pairs = get_input(input_file, group_pairs=False)
    # Add the divider packets
    pairs.append([[2]])
    pairs.append([[6]])

    # Sort the packets according to the comparison rules implemented in the compare_order function
    # Apparently cmp_to_key is only intended for compatibility with Python 2, where sorted() also
    # had a cmp option which would accept a function like compare_order. Supposedly it should be
    # possible to write a lambda for the key parameter of sorted() which would achieve the same,
    # but this way is much easier.
    sorted_pairs = sorted(pairs, key=cmp_to_key(compare_order))

    # Calculate the decoder key with the indices of the divider packets
    decoder_key = (sorted_pairs.index([[2]]) + 1) * (sorted_pairs.index([[6]]) + 1)
    
    return decoder_key
