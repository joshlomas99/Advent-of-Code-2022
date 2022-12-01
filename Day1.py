def Day1_Part1(filename='Inputs/Day1_Inputs.txt'):
    """
    Calculates the maximum total number of Calories carried by a single elf, where the calories
    of each item of food carried by each elf are given in an input file.

    Parameters
    ----------
    filename : str, optional
        Input file giving the calories of the food carried by each elf.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    max_calories : int
        The maximum total number of Calories carried by a single elf.

    """
    # Parse input file
    file = open(filename)
    elves = [[]]
    for line in file:
        line = line.strip().split()
        if len(line) == 0:
            elves.append([])
        else:
            elves[-1].append(int(line[0]))
    file.close()

    # Total up the calories of each elf and find the maximum
    max_calories = max(sum(e) for e in elves)

    return max_calories

def Day1_Part2(filename='Inputs/Day1_Inputs.txt'):
    """
    Calculates the total number of Calories carried by the three elves carrying the largest
    individual amounts of Calories, where the calories of each item of food carried by each elf
    are given in an input file.

    Parameters
    ----------
    filename : str, optional
        Input file giving the calories of the food carried by each elf.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    max_calories : int
        The total number of Calories carried by the three elves carrying the largest individual
        amounts of Calories.

    """
    # Parse input file
    file = open(filename)
    elves = [[]]
    for line in file:
        line = line.strip().split()
        if len(line) == 0:
            elves.append([])
        else:
            elves[-1].append(int(line[0]))
    file.close()

    # Total up the calories of each elf
    totals = [sum(e) for e in elves]
    # Sort them in ascending order
    totals.sort()
    # Find the sum of the top three values
    max_calories = sum(totals[-3:])

    return max_calories
