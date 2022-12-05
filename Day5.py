def get_input(input_file: str='Inputs/Day5_Inputs.txt') -> tuple:
    """
    Parse an input file giving the initial state of a series of stacks of crates, followed
    by a set of instuctions on how to rearrange the crates, separated by a newline.

    Parameters
    ----------
    input_file : str, optional
        The input file giving the initial stacks and rearrangement instructions.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    stacks : list(list(str))
        List of stacks in order, with stacks arranged such that stack[-1] is the top crate.

    instructions : list(list(int))
        List of instructions for rearranging crates, arranged as:
        [number_to_move, stack_to_move_from, stack_to_move_to].

    """
    # Parse input file
    file = open(input_file)
    stacks, instructions = [], []
    # Flag that the initial stacks haven't been initialised yet
    initial_state = None
    for line in file:
        if len(line.strip()) > 0:
            if initial_state == None: # If initial states aren't initialised yet
                for i in range(0, len(line), 4):
                    # Spaces mean no crates in this position
                    if line[i: i+4].isspace():
                        # Initialise empty stack
                        stacks.append([])
                    else:
                        # Initialise stack with top crate
                        stacks.append([line[i: i+4][1]])
                # Flag that the initial stacks have been initialised,
                # but not finished
                initial_state = False
    
            elif not initial_state: # If initial states have been initialised but not finished
                for n, i in enumerate(range(0, len(line), 4)):
                    # Spaces mean no crates in this position
                    if not line[i: i+4].isspace():
                        # When it reaches the numbers below each stack,
                        # the initial stacks are complete
                        if line[i: i+4][1].isnumeric():
                            # Flag that the initial stacks are finished
                            initial_state = True
                            break
                        else:
                            # Append next highest crate onto stack
                            stacks[n].append(line[i: i+4][1])
    
            else: # Else we are reading instructions
                # Separate numbers from text
                line = line.strip().split('move ')[1].split(' from ')
                instructions.append([int(n) for part in line for n in part.split(' to ')])

    file.close()

    # Reverse stack ordering for tidier code in the next part
    [stack.reverse() for stack in stacks]

    return stacks, instructions

def Day5_Part1(input_file: str='Inputs/Day5_Inputs.txt') -> str:
    """
    Determines the top crates in each of a series of stacks, after a series of instructions for
    rearranging stacks are applied to an initial state of the stacks, where both the initial state
    and rearrangement instructions are given in an input file. Crates are labelled with single
    characters and are moved one at a time between stacks, even if the instruction is to move
    multiple crates between the same two stacks.

    Parameters
    ----------
    input_file : str, optional
        The input file giving the initial stacks and rearrangement instructions.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    top_crates : str
        The labels of the top crates in every stack, listed in a string.

    """
    # Parse input file
    stacks, instructions = get_input(input_file)
    
    for instruction in instructions:
        for i in range(instruction[0]): # For the number of crates specificed, one at a time
            # Add top crate from the specified stack to the other, while removing it from the
            # original stack
            stacks[instruction[2]-1].append(stacks[instruction[1]-1].pop(-1))

    # Join the labels of the top crates in each stack
    top_crates = ''.join([stack[-1] for stack in stacks])
    return top_crates

def Day5_Part2(input_file: str='Inputs/Day5_Inputs.txt') -> str:
    """
    Determines the top crates in each of a series of stacks, after a series of instructions for
    rearranging stacks are applied to an initial state of the stacks, where both the initial state
    and rearrangement instructions are given in an input file. Crates are labelled with single
    characters and are moved as a group between stacks if the instruction is to move multiple
    crates between the same two stacks, preserving their original ordering.

    Parameters
    ----------
    input_file : str, optional
        The input file giving the initial stacks and rearrangement instructions.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    top_crates : str
        The labels of the top crates in every stack, listed in a string.

    """
    # Parse input file
    stacks, instructions = get_input(input_file)

    for instruction in instructions:
        # Get the list of crates which are moving
        moving = stacks[instruction[1]-1][-instruction[0]:]
         # Remove the moving crates from their original stack
        stacks[instruction[1]-1] = stacks[instruction[1]-1][:-instruction[0]]
        # Add the moving crates to their new stack
        stacks[instruction[2]-1] += moving
    
    # Join the labels of the top crates in each stack
    top_crates = ''.join([stack[-1] for stack in stacks])
    return top_crates
