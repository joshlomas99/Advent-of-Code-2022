class Valve:
    """
    Class describing a Valve, with a given flow rate, which is connected to other specified
    valves via tunnels.
    """
    def __init__(self, name, flow_rate, tunnels):
        """
        Initialise the class with 3 parameters.

        Parameters
        ----------
        name : str
            Name of the valve.
        flow_rate : int
            Pressure flow rate per minute of the valve.
        tunnels : dict(str: int)
            Dictionary of the form (valve_name: travel_time) giving the names of the other valves
            connected to this one via tunnels, and the time in minutes required to travel to a
            given valve.

        Returns
        -------
        None.

        """
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels

    def __repr__(self):
        """
        Return the representation of an Valve object.

        Returns
        -------
        str
            Representation.

        """
        return '{}({}, {}, {})'.format(self.__class__.__name__, self.name,
                                       self.flow_rate, self.tunnels)

import re

def get_input(input_file: str='Inputs/Day16_Inputs.txt') -> list:
    """
    Parse an input file containing a list of Valves, their flow rates and the other valves they are
    connected to via tunnels which take 1 minute to cross.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the Valves and their properties.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    valves: dict(str, Valve)
        Dictionary of the form (valve_name: Valve object) containing every Valve object given in
        the input file.

    """
    # Parse input file
    with open(input_file) as f:
        # Extract only Valve names and flow_rate
        valve_props = [re.findall('[A-Z]{2}|\d+', line) for line in f.readlines()]
        # Build valve objects and add to dictionary
        valves = {v[0]: Valve(v[0], int(v[1]), {nv:1 for nv in v[2:]}) for v in valve_props}

    return valves

def compress_valves(all_valves, start_valve='AA'):
    """
    Compress a system of Valves down to only useful ones by removing all Valves with zero flow rate
    and adjusting the travel times between the remaining Valves accordingly. e.g. if AA is directly
    connected to BB (travel time 1) and BB is directly connected to CC, but BB has zero flow rate,
    while AA and CC do not, remove BB from the system and set the travel time between AA and CC to
    2.

    Parameters
    ----------
    all_valves : dict(str, Valve)
        Dictionary of the form (valve_name: Valve object) containing every Valve object in the
        initial system.
    start_valve : str, optional
        The starting valve within the system of valves, since even if this has zero flow rate we
        want it to remain in the system.
        The default is 'AA'.

    Returns
    -------
    compressed_valves : dict(str, Valve)
        Compressed system of Valves with zero flow rate Valves removed.

    """
    for valve in all_valves:
        # If the current valve has non-zero flow rate (or is the starting valve)
        if all_valves[valve].flow_rate != 0 or valve == start_valve:
            # Copy the current tunnels
            new_tunnels = all_valves[valve].tunnels.copy()
            # Find flow rates of all currently connected Valves
            next_valve_flow_rates = [all_valves[v].flow_rate if v != start_valve else 1 \
                                     for v in new_tunnels]
            # Track which valves are removed
            removed = []
            # While any connected Valves have zero flow_rate
            while not all(next_valve_flow_rates):
                # Find the next Valve with zero flow_rate
                next_valve = [v for v in new_tunnels][next_valve_flow_rates.index(0)]
                # Add Valves connected to the next Valve to the tunnels for the current Valve,
                # calculating the new travel time for each one
                new_tunnels.update({v: new_tunnels[next_valve] + all_valves[next_valve].tunnels[v] \
                                    for v in all_valves[next_valve].tunnels if v not in removed})
                # Remove the next valve (which has zero flow rate) from the new list of connected
                # Valves, and add to list of removed Valves
                new_tunnels.pop(next_valve)
                removed.append(next_valve)
                # Remove the current valve if it has been added
                if valve in new_tunnels:
                    new_tunnels.pop(valve)
                # Update flow rates of all currently connected Valves
                next_valve_flow_rates = [all_valves[v].flow_rate if v != start_valve else 1 \
                                         for v in new_tunnels]
            # Update connected Valves for current Valve with new list
            all_valves[valve].tunnels = new_tunnels

    # Build new dict with only positive flow rate valves (and starting valve)
    compressed_valves = {v: all_valves[v] for v in all_valves \
                         if all_valves[v].flow_rate > 0 or v == start_valve}

    return compressed_valves

def find_max_route(curr_path, valves, minutes_left, curr_max_pressure=0, open_valves=['AA'],
                   max_route=(0, ['AA'])):
    """
    Performs a recursive depth-first search to find the route through a system of valves which
    maximises the total pressure released after a given number of minutes have passed. As each
    closed valve is reached it can be either opened, taking an additional 1 minute of time, or it
    can be left closed. All valves start closed. Once opened a valve will release a pressure equal
    to its flow rate each following minute. Valves are connected to each other via a system of
    tunnels, and the valves directly connected to a given valve are specified for each valve,
    alongside the travel time in minutes between them.

    Parameters
    ----------
    curr_path : list(str)
        List of valves visited in the current route. Must start as [start_valve].
    valves : dict(str, Valve)
        Dictionary of the form (valve_name: Valve object) containing every valve in the system,
        with the properties of each valve contained in the corresponding Valve object.
    minutes_left : int
        The number of minutes remaining to interact with valves and release pressure.
    curr_max_pressure : int, optional
        The maximum total pressure released for any route checked so far on the current branch of
        the search.
        The default is 0.
    open_valves : list(str)
        List of all opened valves so far in the current route.
        The default is [].
    max_route : tuple(int, list(str))
        Tuple of the form (total_pressure_released, path=[valve1, valve2,...]), giving the route
        which releases the most total pressure of any route checked so far.
        The default is (0, ['AA']), where 'AA' is the starting valve.

    Returns
    -------
    max_route : tuple(int, list(str))
        Tuple of the form (total_pressure_released, path=[valve1, valve2,...]), giving the route
        which releases the most total pressure of any possible route.

    """
    # If all valves are opened then there are no more options, so return the current max route
    if sorted(open_valves) == sorted([v for v in valves]):
        return curr_max_pressure, open_valves
    else:
        # Else make a rough estimate of the potential pressure to still be released on this route
        # by assuming the remaining unopened valves can be visited in descending order of flow rate,
        # with each travel time at 1 minute (impossible to exceed this pressure for a given route)
        # Find the flow rates of the unopened valves
        remaining_flow_rates = [valves[v].flow_rate for v in valves if v not in open_valves]
        # Add to the current pressure the pressure released by each valve in the time remaining
        rough_max = curr_max_pressure + sum([(minutes_left - 2*i)*remaining_flow_rates[i-1] \
                                             # for all unopened valves
                                             for i in range(1, len(remaining_flow_rates) + 1) \
                                             # if the time doesn't run out for a given valve
                                             if (minutes_left - 2*i) > 0])
        # If this rough estimate is less than the current max, no point continuing with this route
        if rough_max < max_route[0]:
            return max_route

    # For each possible next valve from the current one
    for next_valve, travel_time in valves[curr_path[-1]].tunnels.items():
        # Find the time remaining after travelling to this valve
        next_minutes_left = minutes_left - travel_time
        # If there isn't enough time, the route is over
        if next_minutes_left <= 0:
            # Check if the pressure for this route exceeds the current max, recording it if so
            if curr_max_pressure > max_route[0]:
                max_route = curr_max_pressure, open_valves
            # Move onto the next potential route
            continue

        # Else if there is enough time:
        # If the current valve isn't open yet, can either open it now or leave it
        if next_valve not in open_valves:
            # Find the maximum possible route from here if this valve is opened
            max_open = find_max_route(curr_path + [next_valve], valves,
                                      # Remove an extra minute for opening the valve
                                      next_minutes_left - 1,
                                      # Add the total pressure released across the remaining time
                                      # by the newly opened valve
                                      curr_max_pressure + ((next_minutes_left - 1)*\
                                                              valves[next_valve].flow_rate),
                                      # Add this valve to the opened valves list
                                      open_valves + [next_valve],
                                      max_route)

            # Find the maximum possible route from here if this valve isn't opened
            max_no_open = find_max_route(curr_path + [next_valve], valves, next_minutes_left,
                                         curr_max_pressure, open_valves, max_route)

            # Find which option is optimal between opening/not opening the valve
            if max_open[0] > max_no_open[0]:
                next_max_route = max_open
            else:
                next_max_route = max_no_open

        else:
            # Else if the current valve is already open, just move past it and find the optimal
            # route from here
            next_max_route = find_max_route(curr_path + [next_valve], valves, next_minutes_left,
                                            curr_max_pressure, open_valves, max_route)

        # If the maximum possible pressure released for moving to this next valve exceeds the
        # current max, record it
        if next_max_route[0] > max_route[0]:
            max_route = next_max_route

    return max_route

def Day16_Part1(input_file: str='Inputs/Day16_Inputs.txt') -> int:
    """
    Finds the maximum possible pressure released at the end of 30 minutes by a system of valves,
    which all start closed and have a given flow rate when opened and are connected to each other
    via tunnels as specified in an input file. The tunnels between valves take 1 minute to cross
    and valves take 1 minute to open. You start at Valve AA and have 30 minutes to move around and
    open valves.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the valves, their flow rates and the other valves they are directly
        connected to via tunnels.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    max_pressure : int
        The maximum possible pressure which can be released in 30 minutes.

    """
    # Parse input file to get list of Valves and their properties
    all_valves = get_input(input_file)

    # Compress valve system down to only valves with non zero flow rates (and the starting valve),
    # adjusting valve connections accordingly
    compressed_valves = compress_valves(all_valves, 'AA')

    # Use a recursive depth-first search to find the optimal route through the valve system,
    # starting at Valve AA
    max_pressure, optimal_route = find_max_route(['AA'], compressed_valves, 30, 0, ['AA'],
                                                 (0, ['AA']))

    return max_pressure

def Day16_Part2_Cheating(input_file: str='Inputs/Day16_Inputs.txt') -> int:
    """
    Finds the maximum possible pressure released at the end of 26 minutes by a system of valves,
    which all start closed and have a given flow rate when opened and are connected to each other
    via tunnels as specified in an input file. The tunnels between valves take 1 minute to cross
    and valves take 1 minute to open. You and an elephant both start at Valve AA and have 26
    minutes to seperately move around and open valves.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the valves, their flow rates and the other valves they are directly
        connected to via tunnels.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    max_pressure : int
        The maximum possible pressure which can be released in 26 minutes by the two-member team.

    """
    ###############################################################################################
    # This happens to work for this specific input, such that the optimal route for two people
    # includes one of the people following exactly the optimal route for one person, and the
    # second just following the optimal route for opening valves which the first never opens.
    # However, this won't always work (and failed for the sample input where the first person can
    # open every valve within the time) so I consider it cheating a bit, hence the proper solution
    # that follows afterwards...
    ###############################################################################################
    # Parse input file to get list of Valves and their properties
    all_valves = get_input(input_file)

    # Compress valve system down to only valves with non zero flow rates (and the starting valve),
    # adjusting valve connections accordingly
    compressed_valves = compress_valves(all_valves, 'AA')

    # Use a recursive depth-first search to find the optimal route through the valve system for one
    # person, starting at Valve AA
    max_pressure_you, optimal_route_you = find_max_route(['AA'], compressed_valves, 26, 0,
                                                         ['AA'], (0, 'AA'))
    # Use the same process to find the optimal route for the second person, without opening any
    # of the valves opened in the optimal route for one person
    max_pressure_elephant, _ = find_max_route(['AA'], compressed_valves, 26, 0,
                                              # Avoid opening valves opened by the first person by
                                              # providing them as already opened at the start for
                                              # the second person
                                              optimal_route_you,
                                              (0, 'AA'))

    # Find the total pressure release by both members
    max_pressure = max_pressure_you + max_pressure_elephant

    return max_pressure

from itertools import permutations

def Floyd_Warshall(valves, distances):
    """
    Implements the Floyd-Warshall algorithm on a system of valves, to find the minimum possible
    distance between every valve and every other valve.

    Parameters
    ----------
    valves : dict(str, Valve)
        Dictionary of the form (valve_name: Valve object) containing every valve in the system,
        with the properties of each valve - flow rates and directly connected valves - contained
        in the corresponding Valve object.
    distances : dict(tuple(str, str): int)
        Dictionary of the form (tuple(valve1, valve2): distance_between_valves_1_and_2) which gives
        the minimum distance currently found between every combination of valves. Valves for which
        a connection has not yet been found are given a default value of 1000 (impossibly high).

    Returns
    -------
    distances : dict(tuple(str, str): int)
        Dictionary of the form (tuple(valve1, valve2): distance_between_valves_1_and_2) which gives
        the minimum possible distance between every combination of valves. Valves for which
        a connection cannot be found will have a default value of 1000 (impossibly high).

    """
    # For every possible combination of a pair of valve (i and j) plus an intermediate valve (k)
    for k, i, j in permutations(valves, 3):
        # Check if the distance between valves i and j via k is shorter than the current shortest
        # distance between i and j, and if it is then set it as the new shortest distance
        distances[i, j] = min(distances[i, j], distances[i, k] + distances[k, j])

    return distances

def find_max_route_all_comb(curr_valve, open_valves, minutes_left, curr_max_pressure,
                            flows, distances, opt_all_comb):
    """
    Performs a recursive depth-first search to find the route through a system of valves which
    maximises the total pressure released after a given number of minutes have passed. As each
    closed valve is reached it can be either opened, taking an additional 1 minute of time, or it
    can be left closed. All valves start closed. Once opened a valve will release a pressure equal
    to its flow rate each following minute. Valves are connected to each other via a system of
    tunnels, and the valves directly connected to a given valve are specified for each valve,
    alongside the travel time in minutes between them.

    Parameters
    ----------
    curr_valve : str
        The name of the current valve which has been reached in the route.
    open_valves : list(str)
        The names of the valves which have been opened so far in the current route.
    minutes_left : int
        The number of minutes remaining to interact with valves and release pressure.
    curr_max_pressure : int
        The maximum total pressure released for any route checked so far on the current branch of
        the search.
    flows : dict(str: int)
        Dictionary of the form (valve_name: flow_rate) giving the flow rate of each valve.
    distances : dict(tuple(str, str): int)
        Dictionary of the form (tuple(valve1, valve2): distance_between_valves_1_and_2) which gives
        the minimum possible distance between every combination of valves.
    opt_all_comb : dict(list(str): int)
        Dictionary of the form (opened_valves: max_pressure_released) giving the maximum possible
        pressure released for all routes checked so far with a given set of valves opened.

    Returns
    -------
    opt_all_comb : dict(list(str): int)
        Dictionary of the form (opened_valves: max_pressure_released) giving the maximum possible
        pressure released for a given set of opened valves.

    """
    ###############################################################################################
    # This method works for Part 2, whereas my original function find_max_route doesn't work,
    # because this method records the max possible pressure for every combination of opened valves,
    # whereas my original method cannot do this without removing the 'rough esimtate' optimisation,
    # which results in it running incredibly slowly.
    ###############################################################################################
    # If the current pressure found is higher than the current max for this combination of opened
    # valves, set it to the new value.
    # The keys of opt_all_comb are lists of opened valves, which are sorted() to avoid duplication
    # and tuple() so they are hashable for the dictionary. This could also be done with bitmasking.
    opt_all_comb[tuple(sorted(open_valves))] = max(curr_max_pressure,
                                                   # dict.get() allows a defult value of 0 to be
                                                   # assigned if no value has been recorded for
                                                   # this combination yet
                                                   opt_all_comb.get(tuple(sorted(open_valves)), 0))
    # For every valve
    for next_valve, flow in flows.items():
        # Find the time remaining after travelling to this valve
        next_minutes_left = minutes_left - distances[curr_valve, next_valve] - 1
        # If there isn't enough time or this valve is already open, move onto the next valve
        if next_minutes_left < 0 or next_valve in open_valves:
            continue
        else:
            # Else process all possible routes after opening this valve
            find_max_route_all_comb(next_valve,
                                    # Add this valve to open_valves
                                    open_valves + [next_valve], next_minutes_left,
                                    # Add the total pressure released across the remaining time
                                    # by the newly opened valve
                                    curr_max_pressure + flow*next_minutes_left,
                                    flows, distances, opt_all_comb)

    return opt_all_comb

def Day16_Part2(input_file: str='Inputs/Day16_Inputs.txt') -> int:
    """
    Finds the maximum possible pressure released at the end of 26 minutes by a system of valves,
    which all start closed and have a given flow rate when opened and are connected to each other
    via tunnels as specified in an input file. The tunnels between valves take 1 minute to cross
    and valves take 1 minute to open. You and an elephant both start at Valve AA and have 26
    minutes to seperately move around and open valves.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the valves, their flow rates and the other valves they are directly
        connected to via tunnels.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    max_pressure : int
        The maximum possible pressure which can be released in 26 minutes by the two-member team.

    """
    # Parse input file
    all_valves = get_input(input_file)

    # Compress valve system down to only valves with non zero flow rates (and the starting valve),
    # adjusting valve connections accordingly
    compressed_valves = compress_valves(all_valves, 'AA')

    # Create dictionary of distances between every combination of valves, fill with known
    # distances from compressed_valves and assign a default impossiblly large value to unknown
    # distances
    distances = {(v, nv): compressed_valves[v].tunnels[nv] if nv in compressed_valves[v].tunnels \
                 else 0 if v == nv else 1000 for nv in compressed_valves for v in compressed_valves}

    # Find minimum distance between every combination of valves using Floyd-Warshall
    distances = Floyd_Warshall(compressed_valves, distances)

    # Create dictionary of flow rates of every valve
    flows = {v: valve.flow_rate for v, valve in compressed_valves.items() if valve.flow_rate > 0}
    
    # Find the maximum possible pressure for every combination of opened valves within 26 minutes
    opt_all_comb = find_max_route_all_comb('AA', [], 26, 0, flows, distances, {})

    # Find the maximum total pressure for two orthogonal combinations of opened valves
    max_pressure = max(dist_1 + dist_2 for route_1, dist_1 in opt_all_comb.items() \
                                      for route_2, dist_2 in opt_all_comb.items() \
                                      # Check the two sets of opened valves are orthogonal
                                      if all(v1 not in route_2 for v1 in route_1))

    return max_pressure
