def get_input(input_file: str='Inputs/Day10_Inputs.txt') -> list:
    """
    Parse an input file giving a list of instructions being sent to a CPU.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the instructions.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    instructions : list
        The extracted list of instructions.

    """
    # Parse input file
    file = open(input_file)
    instructions = []
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            instructions.append(line)

    file.close()

    return instructions

def Day10_Part1(input_file: str='Inputs/Day10_Inputs.txt') -> int:
    """
    Calculate the sum of the strengths of the signals to a CPU during the 20, 60, 100, 140, 180 and
    220th clock cycles, where the CPU operates according to a set of instructions given in an input
    file to change the value of a register X, which starts at 1, and is driven by a clock circuit
    for which each tick is called a cycle. Signal strength is calculated as the cycle number
    multiplied by the value of the X register for a given cycle.

    CPU Instructions
    ----------------
    ``addx V``: takes two cycles to complete. After two cycles, the X register is increased by the
    value V. (V can be negative.)

    ``noop``: takes one cycle to complete. It has no other effect.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the CPU instructions.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    important_signal_strength_sum : int
        The sum of the 'important' signal strengths during the 20, 60, 100, 140, 180 and 220th
        clock cycles.

    """
    # Parse input file
    instructions = get_input(input_file)
    # X and cycle number both start at 1
    X, cycle = 1, 1
    important_signal_strength_sum = 0
    for instruction in instructions: # For each instruction
        # Always process at least 1 cycle
        if (cycle - 20)%40 == 0: # If it is an 'important' cycle, add the signal strength to total
            important_signal_strength_sum += cycle*X
        cycle += 1
        if instruction[0] == 'addx': # If adding to X
            # Process additional cycle
            if (cycle - 20)%40 == 0:
                important_signal_strength_sum += cycle*X
            cycle += 1
            # Then change X according to instruction
            X += int(instruction[1])
    
    return important_signal_strength_sum

def Day10_Part2(input_file: str='Inputs/Day10_Inputs.txt') -> None:
    """
    Prints the output of a cathode-ray tube (CRT) with a 40 x 6 grid of pixels, which is operated
    by a CPU according to a set of instructions given in an input file which change the value of a
    register X, which starts at 1. The CPU is driven by a clock circuit for which each tick is
    called a cycle. The CRT works by drawing pixels from left to right, one row at a time, based on
    the position of a 3 pixel wide sprite, where the position of the central pixel in the current
    row is given by the current value of X. If the sprite is positioned such that one of its three
    pixels is the pixel currently being drawn, the screen produces a lit pixel (#); otherwise, the
    screen leaves the pixel dark (.).

    CPU Instructions
    ----------------
    ``addx V``: takes two cycles to complete. After two cycles, the X register is increased by the
    value V. (V can be negative.)

    ``noop``: takes one cycle to complete. It has no other effect.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the CPU instructions.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    None

    """
    # Parse input file
    instructions = get_input(input_file)
    # X and cycle number both start at 1
    X, cycle = 1, 1
    # Initialise empty row
    current_line = ''
    for instruction in instructions: # For each instruction
        # Always process at least 1 cycle
        if abs((cycle-1)%40 - X) <= 1: # If sprite overlaps with current pixel, light it up
            current_line += '#'
        else: # Else leave it dark
            current_line += '.'
        if cycle%40 == 0: # If reached the end of the row
            # Print the row
            print(current_line)
            # And reset the row to empty
            current_line = ''
        cycle += 1
        if instruction[0] == 'addx': # If adding to X
            # Process additional cycle
            if abs((cycle-1)%40 - X) <= 1:
                current_line += '#'
            else:
                current_line += '.'
            if cycle%40 == 0:
                print(current_line)
                current_line = ''
            cycle += 1
            # Change X according to instruction
            X += int(instruction[1])
