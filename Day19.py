import re

def get_input(input_file: str='Inputs/Day19_TestInputs.txt') -> list:
    """
    Parse an input file giving a set of blueprints detailling the resources required for building
    a series of robots.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the blueprints.
        The default is 'Inputs/Day19_TestInputs.txt'.

    Returns
    -------
    blueprints : dict(int :(dict(str: dict(str: int))))
        Dictionary of extracted blueprints in the form dict(id, blueprint), with individual
        blueprints in the form dict(robot_type: dict(resource: cost)).

    """
    # Parse input file
    with open(input_file) as f:
        lines = f.readlines()

    blueprints = {}
    for line in lines:
        # Extract and format numbers
        numbers = [int(i) for i in re.findall('\d+', line.strip())]
        # Build blueprint dictionary
        blueprints[numbers[0]] = {'ore': {'ore': numbers[1], 'clay': 0, 'obsidian': 0, 'geode': 0},
                                  'clay': {'ore': numbers[2], 'clay': 0, 'obsidian': 0, 'geode': 0},
                                  'obsidian': {'ore': numbers[3], 'clay': numbers[4], 'obsidian': 0, 'geode': 0},
                                  'geode': {'ore': numbers[5], 'clay': 0, 'obsidian': numbers[6], 'geode': 0}}

    return blueprints

import math

def find_max_geodes(robot_costs: dict, robots: dict={'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0},
                    remaining_minutes: int=24, resources: dict={'ore': 0, 'clay': 0, 'obsidian': 0},
                    curr_geodes: int=0, max_geodes: int=0, max_costs: dict=None) -> int:
    """
    Uses a recursive depth-first search to find the maximum possible number of geodes which can be
    collected in a given number of minutes by a series of robots, given specified starting robots
    and resources.

    Robots
    ------
    There are four types of robot: ore, clay, obsidian and geode; which each produce 1 unit of
    their correpsonding resource per minute once built.
    Only one robot can be built per turn, and they take one minute to be built.

    Parameters
    ----------
    robot_costs : dict(str: dict(str: int))
        Blueprint in the form dict(robot_type: dict(resource: cost)) giving the build costs of
        different types of robots.
    robots : dict(str: int), optional
        The number of each type of robot currently built.
        The default is {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}.
    remaining_minutes : int, optional
        The number of minutes remaining to build robots and collect resources.
        The default is 24.
    resources : dict(str: int), optional
        The number of each type of resource currently held, apart from geodes.
        The default is {'ore': 0, 'clay': 0, 'obsidian': 0}.
    curr_geodes : int, optional
        The number of geodes currently held. The default is 0.
    max_geodes : int, optional
        The maximum possible total number of geodes so far found.
        The default is 0.
    max_costs : dict(str: int) or NoneType, optional
        The maximum amount of each resource required to build a robot across every robot type,
        for the given blueprint.
        The default is None.

    Returns
    -------
    max_geodes : int
        The maximum possible total number of geodes which can be collected for the given blueprint,
        in the given amount of time.

    """
    # Calculate max_costs if it hasn't been calculated yet - pass this between recursive calls
    # to avoid recalculating it repeatedly
    if not max_costs:
        max_costs = {resource: max(robot_costs[robot][resource] for robot in robots) for resource in resources}

    # If we built one geode per minute from now until the end, would the final total exceed the
    # highest amount found so far? If not then no point continuing so stop here
    if curr_geodes + sum(g for g in range(remaining_minutes)) <= max_geodes:
        return max_geodes

    # If there is 1 minute or less then we can no longer gain from building any more geode robots,
    # so stop here
    if remaining_minutes <= 1:
        # Check if current branch geode number exceeds current max
        if curr_geodes > max_geodes:
            return curr_geodes
        return max_geodes

    # For each type of robot
    for new_robot, num in robots.items():
        # Check if we have at least one robot producing each resource needed for the current robot,
        # if not we canot build this yet
        if not all(robots[resource] for resource, quantity in robot_costs[new_robot].items() \
                   if quantity > 0):
            continue

        # Except for geode robots
        if new_robot != 'geode':
            # If we have at least as many robots of this type as the maximum amount of that
            # resource required to build any single robot, then there is no point building any more
            # of these robots, since we can only build one robot per second
            if num >= max_costs[new_robot]:
                continue

            # If the maximum number of the current resource that we will have by the end of the
            # time exceeds the amount required to build the most expensive robot for that resource
            # every minute until time runs out, then there is no point building any more of this
            # robot as we will never need more of this resource
            if remaining_minutes*num + resources[new_robot] >= remaining_minutes*max_costs[new_robot]:
                continue

        # Find the minimum amount of full minutes required to build up the resources required to
        # build the next robot, given the current robots, plus 1 minute to build it
        minutes_to_build = math.ceil(max((quantity - resources[resource])/robots[resource] \
                                         if quantity > resources[resource] else 0 \
                                         for resource, quantity in robot_costs[new_robot].items() \
                                         if quantity > 0)) + 1

        # If there will be at least 1 minute left after building this robot, so it can produce
        # at least one resource, then build it
        if minutes_to_build < remaining_minutes:
            # Create copy of robots and add one to the current robot's count
            new_robots = robots.copy()
            new_robots[new_robot] += 1

            # Calculate the number of resources after the time taken to build this next robot
            # passes, minus the resources taken to build it
            new_resources = {resource: quantity + (minutes_to_build*robots[resource]) \
                             - robot_costs[new_robot][resource] \
                             for resource, quantity in resources.items()}

            # For new geode robots
            if new_robot == 'geode':
                # Calculate the total number of geodes that will be produced across the entire
                # remaining time by this new robot
                curr_geodes += (remaining_minutes - minutes_to_build)

            # Recursively find the maximum possible number of geodes having built this robot here
            max_geodes_here = find_max_geodes(robot_costs, new_robots, remaining_minutes - minutes_to_build,
                                              new_resources, curr_geodes, max_geodes, max_costs)

        else:
            # If there was no time left to benefit from building this extra robot, the max for this
            # branch is the current geode total
            max_geodes_here = 1*curr_geodes

        # If this branch exceeds the current max, change the max accordingly
        if max_geodes_here > max_geodes:
            max_geodes = max_geodes_here

    return max_geodes

def Day19_Part1(input_file: str='Inputs/Day19_Inputs.txt') -> int:
    """
    Find the sum of the quality levels of every blueprint given in an input file, where the
    quality of a blueprint is the product of the id number of the blueprint and the maximum
    possible number of geodes which can be produced in 24 minutes by a series of robots, where the
    cost of each type of robot is given in the blueprint.

    Robots
    ------
    There are four types of robot: ore, clay, obsidian and geode; which each produce 1 unit of
    their correpsonding resource per minute once built.
    Only one robot can be built per turn, and they take one minute to be built.
    You start with just 1 ore robot, and no additional resources.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the blueprints.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    quality_level : int
        The sum of the quality levels of all blueprints given in the input file.

    """
    # Parse the input file and extract the blueprints
    blueprints = get_input(input_file)

    quality_level = 0
    # For each blueprint
    for id_num, blueprint in blueprints.items():
        # Use a recurive depth-first search to find the maximum possible number of geodes that be
        # collected using that blueprint, and calculate the corresponding quality level
        quality_level += id_num*find_max_geodes(blueprint)
    
    return quality_level

def Day19_Part2(input_file: str='Inputs/Day19_Inputs.txt') -> int:
    """
    Find the product of the maximum possible numbers of geodes which can be produced in 32 minutes
    by a series of robots, for the first three blueprints given in an input file, where the cost
    of each type of robot is given in the blueprint.

    Robots
    ------
    There are four types of robot: ore, clay, obsidian and geode; which each produce 1 unit of
    their correpsonding resource per minute once built.
    Only one robot can be built per turn, and they take one minute to be built.
    You start with just 1 ore robot, and no additional resources.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the blueprints.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    quality_level : int
        The product of the maximum possible numbers of geodes which can be produced in 32 minutes
        for the first 3 blueprints in the input file.

    """
    # Parse the input file and extract the blueprints
    blueprints = get_input(input_file)

    geode_product = 1
    # For the first 3 blueprints
    for blueprint in list(blueprints.values())[:3]:
        # Use a recurive depth-first search to find the maximum possible number of geodes that be
        # collected using that blueprint
        geode_product *= find_max_geodes(blueprint, remaining_minutes=32)
    
    return geode_product
