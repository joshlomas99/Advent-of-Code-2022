def get_input(input_file: str='Inputs/Day4_Inputs.txt') -> list:
    """
    Parse input file containing the section assignment IDs for pairs of elves.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the section assignment for each pair.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    pairs : list(list(set(int)))
        List of extracted assigned sections for each elf in the pair, for each pair.

    """
    # Parse input file
    file = open(input_file)
    pairs = []
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            pair = []
            for task in line[0].split(','): # Split elves up
                # Split start and end IDs
                start, stop = [int(i) for i in task.split('-')]
                # Create set of all sections for each elf
                elf = set(range(start, stop+1))
                pair.append(elf)
            pairs.append(pair)

    file.close()

    return pairs

def Day4_Part1(input_file: str='Inputs/Day4_Inputs.txt') -> int:
    """
    Calculate the total number of pairs of elves where one section assignment fully contains the
    other, where section assignments for each pair of elves are given as ranges, e.g. 1-3 means
    sections 1, 2 and 3 and 2-3 means sections 2 and 3, which is fully contained by the first
    range.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the section assignment for each pair.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    subset_count : int
        The number of pairs where one elf's section assignment fully contains the other's.

    """
    # Parse input file
    pairs = get_input(input_file)

    subset_count = 0
    for pair in pairs:
        # If the first pair is a subset/superset of the other, increase count by 1
        if pair[0].issubset(pair[1]) or pair[0].issuperset(pair[1]):
            subset_count += 1

    # I've since seen that this can be done way more efficiently by just comparing the start and
    # end points of each elf's section assignment, without needing to generate the full list, but
    # since the input is small this works fine and is probably easier to read.

    return subset_count

def Day4_Part2(input_file: str='Inputs/Day4_Inputs.txt') -> int:
    """
    Calculate the total number of pairs of elves whose section assignments overlap, where section
    assignments for each pair of elves are given as ranges, e.g. 1-3 means sections 1, 2 and 3 and
    2-4 means sections 2, 3 and 4, which overlaps with the first range.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the section assignment for each pair.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    overlap_count : int
        The number of pairs of elves whose section assignments overlap.

    """
    # Parse input file
    pairs = get_input(input_file)

    overlap_count = 0
    for pair in pairs:
        # If there is any intersection between pairs, increase the count by one
        if len(pair[0].intersection(pair[1])) > 0:
            overlap_count += 1

    # Again, this could be done more efficiently by just comparing start/end points, but this is
    # definitely easier to read

    return overlap_count
