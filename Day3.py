def get_input(input_file: str='Inputs/Day3_Inputs.txt') -> list:
    """
    Parse input file containing the contents of the rucksacks carried by a group of elves.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the rucksack contents.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    rucksacks : list(str)
        List of extracted rucksack contents.

    """
    # Parse input file
    file = open(input_file)
    rucksacks = []
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            rucksacks.append(line[0])
    file.close()

    return rucksacks

def Day3_Part1(input_file: str='Inputs/Day3_Inputs.txt') -> int:
    """
    Calculate the total priority score for all elves based on the single shared item between the
    two compartments of their rucksacks, the total contents of which is given in an input file.
    Each item is represented by a different upper or lower case character, and each compartment
    holds half of the total items, split down the middle as given in the input. The priority score
    is 1-26 for items 'a'-'z' and 27-52 'A'-'Z'.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the contents of the elves rucksacks.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    total : int
        The total priority score across all the elves.

    """
    # Parse input file
    data = get_input(input_file)
    
    total = 0
    for rucksack in data: # For each rucksack
        # Make sets of each compartment contents
        c1 = set(rucksack[:int(len(rucksack)/2)])
        c2 = set(rucksack[int(len(rucksack)/2):])
        # Find the single common item using intersection()
        common = c1.intersection(c2).pop()
        # Calculate prioity score by shifting ord() values
        if common.islower():
            p = ord(common) - 96
        else:
            p = ord(common) - 38
        total += p
    
    return total

def Day3_Part2(input_file: str='Inputs/Day3_Inputs.txt') -> int:
    """
    Calculate the total priority score across all groups of three elves based on the single shared
    item between their rucksacks, the total contents of which is given in an input file. Elves are
    arranged in their groups as givenin the input file. Each item is represented by a different
    upper or lower case character. The priority score is 1-26 for items 'a'-'z' and 27-52 'A'-'Z'.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the contents of the elves rucksacks.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    total : int
        The total priority score across all the groups of elves.

    """
    # Parse input file
    data = get_input(input_file)

    total = 0
    for n in range(0, len(data), 3): # For each group of three
        # Make sets of each rucksack contents
        c1 = set(data[n])
        c2 = set(data[n+1])
        c3 = set(data[n+2])
        # Find the common item using intersection()
        common = c1.intersection(c2).intersection(c3).pop()
        # Calculate prioity score by shifting ord() values
        if common.islower():
            p = ord(common) - 96
        else:
            p = ord(common) - 38
        total += p
    
    return total
