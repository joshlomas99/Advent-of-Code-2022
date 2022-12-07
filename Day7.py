"""
I realise this could all be done more simply with just nested lists of file sizes instead of
dictionaries, as the directory and file names are not relevant, but it's much easier to visualise
what's happening with the dictionary, so I think it was worth doing it this way anyway.
"""

def get_input(input_file: str = 'Inputs/Day7_Inputs.txt') -> dict:
    """
    Parse an input file containing Linux commands and their outputs, used to move around a file
    system and list the contents of each directory, and construct a dictionary representing the
    full file system, with sizes of file given.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the commands and their outputs.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    file_system : dict
        Dictionary representing the file system, where entries can be str: dict for subdirectories
        or str: int for files, where the ineteger is the size of the file.

    """
    # Parse input file
    file = open(input_file)
    file_system = {}
    # Track the current directory using a string
    curr_dir = 'file_system'
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            if line[0] == '$': # If command
                if line[1] == 'cd': # Only need to consider cd commands, not ls
                    if line[2] == '..':
                        # Set the current directory to one level higher
                        curr_dir = '['.join(curr_dir.split('[')[:-1])
                    elif line[2] == '/':
                        # Reset to the highest directory
                        curr_dir = 'file_system'
                    else:
                        # Move into the subdirectory
                        curr_dir += f'["{line[2]}"]'

            # Else must be the output from ls:
            elif line[0] == 'dir': # If directory
                # Add the new subdirectory to the current directory
                eval(curr_dir)[line[1]] = {}

            else: # Else must be file
                # Add file and its size to the current directory
                eval(curr_dir)[line[1]] = int(line[0])

    file.close()

    return file_system

def total_size(file_system: dict, total_sizes: dict={}, curr_dir: str='file_system') -> int:
    """
    Recursively calculates the size of the given directory and all subdirectories.

    Parameters
    ----------
    file_system : dict
        The given directory to calculate sizes for.
    total_sizes : dict, optional
        The sizes of subdirectories measured so far (required for recursion).
        The default is {}.
    curr_dir : str, optional
        The current directory as a string (required for recursion).
        The default is 'file_system'.

    Raises
    ------
    Exception
        Raises exception if two directories with the same path are found.

    Returns
    -------
    curr_size : int
        The total size of the given directory.

    total_sizes : dict(str: int)
        The sizes of all subdirectories, by name.

    """
    curr_size = 0
    for key in file_system: # Loop through directory contents
        if type(file_system[key]) == dict: # If subdirectory
            # Recursively perform the same operation for the subdirectory
            sub_size, total_sizes = total_size(file_system[key], total_sizes,
                                               '/'.join([curr_dir, key]))
            # Add size of subdirectory
            curr_size += sub_size
            # Check if subdirectory has been counted before
            if key in total_sizes:
                raise Exception(f'Directory "{key}" size has already been measured as \
                                {total_sizes[key]}!\nAttempting to overwrite with {sub_size}')
            # Add subdirectory to total_sizes dictionary
            total_sizes['/'.join([curr_dir, key])] = sub_size
        else: # Else must be a file
            # Add size of file
            curr_size += file_system[key]

    return curr_size, total_sizes

def Day7_Part1(input_file: str='Inputs/Day7_Inputs.txt', size_limit: int=100000) -> int:
    """
    Calculate the total size of all subdirectories in a file system with an individual total size
    less than or equal to the given size limit. The file system is given in an input file as the
    outputs of Linux commands, moving through and listing the contents of every contained
    subdirectory.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the commands and their outputs.
        The default is 'Inputs/Day7_Inputs.txt'.
    size_limit : int, optional
        The maximum size of files to be considered.
        The default is 100,000.

    Returns
    -------
    total_size_sum : int
        The total size of all subdirectories in the file system smaller than or equal to the
        given size limit.

    """
    # Parse input file
    file_system = get_input(input_file)
    # Get size of file system and all subdirectories
    file_system_size, total_sizes = total_size(file_system)
    # Add full file system to dictionary
    total_sizes['/'] = file_system_size

    # Sum sizes of subdirectories at or below the size limit
    total_size_sum = sum([total_sizes[k] for k in total_sizes if total_sizes[k] <= size_limit])

    return total_size_sum

def Day7_Part2(input_file: str='Inputs/Day7_Inputs.txt', total_space: int=70000000,
               space_required: int=30000000) -> int:
    """
    Calculate the size of the smallest single subdirectory which can be deleted from a file
    system, of a given total storage capacity, to free up enough extra space to meet the given
    space required to install updates. The file system is given in an input file as the outputs
    of Linux commands, moving through and listing the contents of every contained subdirectory.

    Parameters
    ----------
    input_file : str, optional
        The input file containing the commands and their outputs.
        The default is 'Inputs/Day7_Inputs.txt'.
    total_space : int, optional
        The total storage capacity of the file system.
        The default is 70,000,000.
    space_required : int, optional
        The total free space required to install updates.
        The default is 30,000,000.

    Returns
    -------
    smallest_sufficient_directory : int
        The size of the smallest single subdirectory which can be deleted from the file system
        to free up enough space to install updates.

    """
    # Parse input file
    file_system = get_input(input_file)
    # Get size of file system and all subdirectories
    file_system_size, total_sizes = total_size(file_system)
    # Add full file system to dictionary
    total_sizes['/'] = file_system_size

    curr_free_space = total_space - file_system_size # Current free space
    new_space_required = space_required - curr_free_space # Extra space required
    # Get smallest subdirectory with size at or above the extra space required
    smallest_sufficient_directory = min([total_sizes[k] for k in total_sizes \
                                         if total_sizes[k] >= new_space_required])

    return smallest_sufficient_directory
