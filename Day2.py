def get_rounds(input_file: str='Inputs/Day2_Inputs.txt') -> list:
    """
    Parse input file containing a strategy guide for each round of a Rock, Paper, Scissors
    tournament.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the strategy guide contents.
        The default is 'Inputs/Day2_Inputs.txt'.

    Returns
    -------
    rounds : list(list(str, str))
        The extracted instructions for each round.

    """
    # Parse input file
    file = open(input_file)
    rounds = []
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            rounds.append(line)
    file.close()

    return rounds

def Day2_Part1(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    """
    Calculates the total score for the player if they play a Rock, Paper, Scissors tournament
    exactly as described in a strategy guide, given in an input file. For each round in the guide,
    the first column is what your opponent is going to play: A for Rock, B for Paper, and C for
    Scissors, and the second column is what you should play in response: X for Rock, Y for Paper
    and Z for Scissors.

    Rock, Paper, Scissors Rules
    ---------------------------
    Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose
    the same shape, the round instead ends in a draw. The score for a single round is the score
    for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for
    the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the strategy guide contents.
        The default is 'Inputs/Day2_Inputs.txt'.

    Returns
    -------
    score : int
        The total score for the player at the end of the tournament.

    """
    # Parse input file
    rounds = get_rounds(input_file)

    # X (1) -> beats C (6), draws with A (3), loses to B (0)
    # Y (2) -> beats A (6), draws with B (3), loses to C (0)
    # Z (3) -> beats B (6), draws with C (3), loses to A (0)
    scores = {'X': {'Score': 1, 'A': 3, 'B': 0, 'C': 6},
              'Y': {'Score': 2, 'A': 6, 'B': 3, 'C': 0},
              'Z': {'Score': 3, 'A': 0, 'B': 6, 'C': 3}}

    score = 0
    # Loop through rounds
    for a, b in rounds:
        # Add shape score and outcome score
        score += scores[b]['Score'] + scores[b][a]

    return score

def Day2_Part2(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    """
    Calculates the total score for the player if they play a Rock, Paper, Scissors tournament
    exactly as described in a strategy guide, given in an input file. For each round in the guide,
    the first column is what your opponent is going to play: A for Rock, B for Paper, and C for
    Scissors, and the second column says how the round needs to end: X means you need to lose,
    Y means you need to end the round in a draw, and Z means you need to win.

    Rock, Paper, Scissors Rules
    ---------------------------
    Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose
    the same shape, the round instead ends in a draw. The score for a single round is the score
    for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for
    the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the strategy guide contents.
        The default is 'Inputs/Day2_Inputs.txt'.

    Returns
    -------
    score : int
        The total score for the player at the end of the tournament.

    """
    # Parse input file
    rounds = get_rounds(input_file)

    # X always loses (0) -> for A play Scissors (3), for B play Rock (1), for C play Paper (2)
    # Y always draws (3) -> for A play Rock (1), for B play Paper (2), for C play Scissors (3)
    # Z always wins (6) -> for A play Paper (2), for B play Scissors (3), for C play Rock (1)
    scores = {'X': {'Score': 0, 'A': 3, 'B': 1, 'C': 2},
              'Y': {'Score': 3, 'A': 1, 'B': 2, 'C': 3},
              'Z': {'Score': 6, 'A': 2, 'B': 3, 'C': 1}}

    score = 0
    # Loop through rounds
    for a, b in rounds:
        # Add outcome score and shape score
        score += scores[b]['Score'] + scores[b][a]

    return score
