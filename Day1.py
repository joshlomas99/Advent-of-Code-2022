def get_elf_totals(input_file: str='Inputs/Day1_Inputs.txt') -> list:
    """
    Parse input file containing the Calories of each item of food carried by each of a group of
    elves, where different elves are separated by newlines.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the calories of the food carried by each elf.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    elves : list(int)
        List of the total Calories carried by each elf.

    """
    # Parse input file
    file = open(input_file)
    elves = [0]
    for line in file:
        line = line.strip().split()
        if len(line) == 0:
            elves.append(0)
        else:
            # Add up calories for each elf
            elves[-1] += int(line[0])
    file.close()

    return elves

def Day1_Part1(input_file: str='Inputs/Day1_Inputs.txt') -> int:
    """
    Calculates the maximum total number of Calories carried by a single elf, where the calories
    of each item of food carried by each elf are given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the calories of the food carried by each elf.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    max_calories : int
        The maximum total number of Calories carried by a single elf.

    """
    # Parse input file
    elves = get_elf_totals(input_file)

    # Total up the calories of each elf and find the maximum
    max_calories = max(elves)

    return max_calories

def Day1_Part2(input_file: str='Inputs/Day1_Inputs.txt') -> int:
    """
    Calculates the total number of Calories carried by the three elves carrying the largest
    individual amounts of Calories, where the calories of each item of food carried by each elf
    are given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the calories of the food carried by each elf.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    max_calories : int
        The total number of Calories carried by the three elves carrying the largest individual
        amounts of Calories.

    """
    # Parse input file
    elves = get_elf_totals(input_file)

    # Sort them in ascending order
    elves.sort()
    # Find the sum of the top three values
    max_calories = sum(elves[-3:])

    return max_calories

def Day1_Part1_one_line(input_file='Inputs/Day1_Inputs.txt'):
    return max([sum([int(c) for c in e.strip().split('\n')]) for e in open(input_file).read().split('\n\n')])

import numpy as np

def Day1_Part2_one_line(input_file='Inputs/Day1_Inputs.txt'):
    return sum(np.sort([sum([int(c) for c in e.strip().split('\n')]) for e in open(input_file).read().split('\n\n')])[-3:])
