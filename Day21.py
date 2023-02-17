def get_input(input_file: str='Inputs/Day21_Inputs.txt') -> list:
    """
    Parse an input file containing a list of monkeys and expressions describing the number each one
    will yell.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the monkeys and expressions.
        The default is 'Inputs/Day21_Inputs.txt'.

    Returns
    -------
    equations : dict(str, str)
        Dictionary containing the expressions for each monkey in the form {monkey_name: expression}.

    """
    # Parse input file
    with open(input_file) as f:
        # Split equations into a dictionary
         equations = {line.strip().split(': ')[0]: line.strip().split(': ')[1] for line in f.readlines()}

    return equations

def Day21_Part1(input_file: str='Inputs/Day21_Inputs.txt') -> int:
    """
    Find the number that the monkey named 'root' will yell, given a list of all monkeys and
    expressions describing the numbers each monkey will yell in an input file. Some monkeys'
    expressions are just numbers, so they already know what to yell, but some expressions are math
    operations which require the numbers yelled by other monkeys to be known.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the monkeys and expressions.
        The default is 'Inputs/Day21_Inputs.txt'.

    Returns
    -------
    root : int
        The number which will eventually be yelled by the monkey named root.

    """
    # Parse input file to extract the monkeys and expressions
    equations = get_input(input_file)

    # Determine which equations are solved (already have a number) and which are still unknown
    # expressions
    solved = {variable: int(equation) for variable, equation in equations.items() if equation.isnumeric()}
    to_solve = {variable: equation for variable, equation in equations.items() if not equation.isnumeric()}
    # While 'root' is still unsolved
    while 'root' in to_solve:
        # Initialise container for still unsolvable expressions
        new_to_solve = {}
        # For each unsolved equation
        for variable, equation in to_solve.items():
            try:
                # Try to evaluate the expression and add the solution to solved
                solved[variable] = int(eval('solved["{0}"]{1}solved["{2}"]'.format(*equation.split())))
            except KeyError:
                # If KeyError then the required variables are not yet known, so add the equation
                # to the currently unsolvable container
                new_to_solve[variable] = equation
    
        to_solve = new_to_solve.copy()

    # Extract the solved value for root
    root = solved['root']

    return root

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.interactive import printing
printing.init_printing(use_latex=(False))

def Day21_Part2(input_file: str='Inputs/Day21_Inputs.txt') -> int:
    """
    Find the number that you (named 'humn') must yell, such that the expression for the monkey
    named 'root' with the operation replaced for '==' evaluates to True, given a list of all
    monkeys and expressions describing the numbers each monkey will yell in an input file. Some
    monkeys' expressions are just numbers, so they already know what to yell, but some expressions
    are math operations which require the numbers yelled by other monkeys to be known.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the monkeys and expressions.
        The default is 'Inputs/Day21_Inputs.txt'.

    Returns
    -------
    humn : int
        The number which you must yell for 'root' to be True.

    """
    # Parse input file to extract the monkeys and expressions
    equations = get_input()
    
    # Determine which equations are solved (already have a number) and which are still unknown
    # expressions
    solved = {variable: int(equation) for variable, equation in equations.items() if equation.isnumeric() and variable != 'humn'}
    to_solve = {variable: equation for variable, equation in equations.items() if not equation.isnumeric()}
    # While there are still unsolved expressions
    while to_solve:
        # Initialise container for still unsolvable expressions
        new_to_solve = {}
        # For each unsolved equation
        for variable, equation in to_solve.items():
            # Ignore the 'humn' expression
            if 'humn' in equation:
                new_to_solve[variable] = equation
                continue
            try:
                # Try to evaluate the expression and add the solution to solved
                solved[variable] = int(eval('solved["{0}"]{1}solved["{2}"]'.format(*equation.split())))
            except KeyError:
                # If KeyError then the required variables are not yet known, so add the equation
                # to the currently unsolvable container
                new_to_solve[variable] = equation

        # If no expressions were solved in the last round, we have reached a dead end, so break
        if new_to_solve == to_solve:
            break
        to_solve = new_to_solve.copy()

    # For each solved value, substitute that value into the remaining unsolved expressions
    for variable, value in solved.items():
        for v in to_solve:
            if variable in to_solve[v]:
                to_solve[v] = to_solve[v].replace(variable, str(value))
    
    # Set up the remaining equations as a set of simulataneous equations in Sympy
    simultaneous_equations = []
    for variable, equation in to_solve.items():
        # For the 'root' expression, replace the operation for '-' so this should evaluate to
        # 0 when LHS == RHS
        if variable == 'root':
            simultaneous_equations.append(parse_expr(equation.split()[0] + ' - ' + equation.split()[2]))
        # For all other expressions, change from var = expr to var - expr so it evaluates to 0
        else:
            simultaneous_equations.append(parse_expr(variable + ' - (' + equation + ')'))

    # Solve the set of equations
    solution = sp.solve(simultaneous_equations)

    # Extract the solve value of humn
    humn = solution[sp.symbols('humn')]

    return humn
