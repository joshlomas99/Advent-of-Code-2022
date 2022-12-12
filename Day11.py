class Monkey:
    """
    Class for describing a Monkey with a set of properties.
    """
    def __init__(self, number: int) -> None:
        """
        Initialise the Monkey with a number.

        Parameters
        ----------
        number : int
            The number of the monkey.

        Returns
        -------
        None.

        """
        self.number = number
        # Initialise properties as None
        self.items = None
        self.operation = None
        self.test = None
        self.true = None
        self.false = None
        # Inspections number starts at 0
        self.inspections = 0

def get_input(input_file: str='Inputs/Day11_Inputs.txt') -> list:
    """
    Parse an input file containing the properties of a set of monkeys.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the monkey properties.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    monkeys : list(Monkey)
        DESCRIPTION.

    """
    # Parse input file
    file = open(input_file)
    monkeys = []
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            # Switch to extract each property for each monkey
            if line[0] == 'Monkey':
                monkeys.append(Monkey(int(line[1][:-1])))
            elif line[0] == 'Starting':
                monkeys[-1].items = [int(n.replace(',', '')) for n in line[2:]]
            elif line[0] == 'Operation:':
                monkeys[-1].operation = ' '.join(line[3:])
            elif line[0] == 'Test:':
                monkeys[-1].test = int(line[-1])
            elif line[1] == 'true:':
                monkeys[-1].true = int(line[-1])
            elif line[1] == 'false:':
                monkeys[-1].false = int(line[-1])
            else:
                print(f'ERROR: Unknown property "{line}"')

    file.close()

    return monkeys

def Day11_Part1(input_file: str='Inputs/Day11_Inputs.txt') -> int:
    """
    Calculate the level of monkey business after 20 rounds of a group of monkeys passing around a
    set of items, where each item has a worry level associated with it and each monkey has a subset
    of the items in its possession. The monkeys take turns each round to inspect their items one at
    a time, in the order they appear in their list of items. Each monkey performs an operation on
    the worry level of the item it is currently inspecting, which then drops by a factor of three
    (rounded down) once the monkey gets bored of the item. It then performs a test on the object
    and passes the item to a different monkey depending on the outcome of the test. The level of
    monkey business is then calculated as the product of the two highest numbers of items
    interacted with for each monkey.

    Monkey Properties
    -----------------
    number : int
        The number of the Monkey.

    items : list(int)
        List of the worry levels of the different items a Monkey holds, in the order they are
        inpected.

    operation : str
        How a Monkey changes the worry level of the item it is inspecting from the current level
        (old) to the new one, e.b. "old + 3".

    test : int
        The test a Monkey performs on the current item, to decide which Monkey to pass it to next.
        The test returns True if the worry level of the item is divisible by the test number and
        False if not.

    true : int
        The number of the Monkey to pass the current item to if the test returns True.

    false : int
        The number of the Monkey to pass the current item to if the test returns False.    

    Parameters
    ----------
    input_file : str, optional
        Input file containing the Monkey proporties.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    monkey_business : int
        The level of monkey business after 20 rounds have passed.

    """
    # Parse input file
    monkeys = get_input(input_file)

    for round_num in range(20): # For 20 rounds
        for monkey in monkeys: # For each Monkey
            for i in range(len(monkey.items)): # For each item the current Monkey holds, in order
                # Get old worry level
                old = monkey.items[i]
                # Determine new worry level
                new = eval(monkey.operation)
                # Divide by 3 when the Monkey gets bored
                new = int(new/3)
                # Perform test on new worry level and pass item to corresponding Monkey
                if new % monkey.test == 0:
                    monkeys[monkey.true].items.append(new)
                else:
                    monkeys[monkey.false].items.append(new)
                # Increment inspection counter for current Monkey
                monkey.inspections += 1
            # At the end of its turn, a Monkey will have no items
            monkey.items = []

    # Get number of inspections for each Monkey and sort in ascending order
    inspections = [m.inspections for m in monkeys]
    inspections.sort()
    # Calculate product of highest two
    monkey_business = inspections[-1] * inspections[-2]

    return monkey_business

def Day11_Part2(input_file: str='Inputs/Day11_Inputs.txt') -> int:
    """
    Calculate the level of monkey business after 10,000 rounds of a group of monkeys passing
    around a set of items, where each item has a worry level associated with it and each monkey
    has a subset of the items in its possession. The monkeys take turns each round to inspect their
    items one at a time, in the order they appear in their list of items. Each monkey performs an
    operation on the worry level of the item it is currently inspecting, which no longer drops once
    the monkey gets bored of the item. It then performs a test on the object and passes the item to
    a different monkey depending on the outcome of the test. The level of monkey business is then
    calculated as the product of the two highest numbers of items interacted with for each monkey.

    Monkey Properties
    -----------------
    number : int
        The number of the Monkey.

    items : list(int)
        List of the worry levels of the different items a Monkey holds, in the order they are
        inpected.

    operation : str
        How a Monkey changes the worry level of the item it is inspecting from the current level
        (old) to the new one, e.b. "old + 3".

    test : int
        The test a Monkey performs on the current item, to decide which Monkey to pass it to next.
        The test returns True if the worry level of the item is divisible by the test number and
        False if not.

    true : int
        The number of the Monkey to pass the current item to if the test returns True.

    false : int
        The number of the Monkey to pass the current item to if the test returns False.    

    Parameters
    ----------
    input_file : str, optional
        Input file containing the Monkey proporties.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    monkey_business : int
        The level of monkey business after 10,000 rounds have passed.

    """
    # Parse input file
    monkeys = get_input(input_file)

    # Calculate product of all Monkeys' test integers
    test_product = 1
    for m in monkeys:
        test_product *= m.test

    for round_num in range(10000): # For 10,000 rounds
        for monkey in monkeys: # For each Monkey
            for i in range(len(monkey.items)): # For each item the current Monkey holds, in order
                # Get old worry level
                old = monkey.items[i]
                # Determine new worry level
                new = eval(monkey.operation)
                # Perform modulus on worry level by the product of all test values
                # Does not change result of test -> limits worry level to manageable amount
                new %= test_product
                # Perform test on new worry level and pass item to corresponding Monkey
                if new % monkey.test == 0:
                    monkeys[monkey.true].items.append(new)
                else:
                    monkeys[monkey.false].items.append(new)
                # Increment inspection counter for current Monkey
                monkey.inspections += 1
            # At the end of its turn, a Monkey will have no items
            monkey.items = []

    # Get number of inspections for each Monkey and sort in ascending order
    inspections = [m.inspections for m in monkeys]
    inspections.sort()
    # Calculate product of highest two
    monkey_business = inspections[-1] * inspections[-2]

    return monkey_business
