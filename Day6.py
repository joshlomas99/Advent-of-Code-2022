def get_input(input_file: str='Inputs/Day6_Inputs.txt') -> str:
    """
    Parse an input file containing a string of characters representing the datastream from a
    communication system.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the datastream.
        The default is 'Inputs/Day6_Inputs.txt'.

    Returns
    -------
    data : str
        The extracted datastream.

    """
    # Parse input file
    data = list(open(input_file))[0].strip()

    return data

def Day6_Part1(input_file: str='Inputs/Day6_Inputs.txt') -> int:
    """
    Determine the number of characters from the beginning of a datastream, given in an input file,
    to the end of the first set of four characters which are all different, indicating the start
    of a packet.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the datastream.
        The default is 'Inputs/Day6_Inputs.txt'.

    Returns
    -------
    start_of_packet : int
        The number of characters before the end of the first start-of-packet marker.

    """
    # Parse input file
    data = get_input(input_file)

    i = 0
    # Move throught the string until the set of 4 characters is 4 long (4 different characters)
    while len(set(data[i:i+4])) < 4 and i < len(data):
        i += 1
    
    start_of_packet = i + 4
    return start_of_packet

def Day6_Part2(input_file: str='Inputs/Day6_Inputs.txt') -> int:
    """
    Determine the number of characters from the beginning of a datastream, given in an input file,
    to the end of the first set of fourteen characters which are all different, indicating the
    start of a message.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the datastream.
        The default is 'Inputs/Day6_Inputs.txt'.

    Returns
    -------
    start_of_packet : int
        The number of characters before the end of the first start-of-message marker.

    """
    # Parse input file
    data = get_input(input_file)

    i = 0
    # Move throught the string until the set of 14 characters is 14 long (14 different characters)
    while len(set(data[i:i+14])) < 14 and i < len(data):
        i += 1
    
    start_of_message = i + 14
    return start_of_message
