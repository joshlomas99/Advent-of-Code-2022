class RangeSet:
    """
    Class representing a set of integer ranges which do not overlap, including when within 1 space
    of each other, e.g. (1, 3) and (4, 7) would become (1, 7), while (1, 3) and (5, 7) would stay
    that way.
    """
    def __init__(self, ranges: list=[]):
        """
        Initialise the set with a list of ranges, can be empty, which must not be overlapping
        according to the rule above, and which are immediately sorted in ascending order.

        Parameters
        ----------
        ranges : list of tuples, optional
            List of ranges to initialise the set with, should not overlap.
            The default is [].

        Returns
        -------
        None.

        """
        self.ranges = ranges
        # Sort the ranges to make adding easier
        self.ranges.sort()

    def __repr__(self):
        """
        Return the representation of an RangeSet object.

        Returns
        -------
        str
            Representation.

        """
        return '{}{}'.format(self.__class__.__name__, tuple(self.ranges))

    def __iadd_tuple__(self, new_range: tuple):
        """
        In place addition of a single tuple range 'new_range' to this RangeSet.
        The new range can overlap with existing ranges in the set.

        Parameters
        ----------
        new_range : tuple of int
            Tuple representing the new range to be added in the form (lower_limit, upper_limit).

        Returns
        -------
        self : RangeSet
            Modified RangeSet with new range included.

        """
        try:
            # Find the first range in the set where the upper limit is higher than the lower limit
            # of the new range
            index = [curr_range[1] - new_range[0] >= -1 for curr_range in self.ranges].index(True)
        except ValueError:
            # If no such range is found, just add the new range to the end of the set
            self.ranges.append(new_range)
            self.ranges.sort()
            return self

        if new_range[1] < self.ranges[index][0]:
            # Check if the new range overlaps with the first possible range, if not then just add
            # it to the set
            self.ranges.append(new_range)
            self.ranges.sort()
        else: # Else it overlaps with at least one current range in the set
            # Create new set of ranges with all ranges lower than new range, and new_range to be
            # added
            new_ranges = self.ranges[:index] + [new_range]
            while index < len(self.ranges) and new_range[1] - self.ranges[index][0] >= -1:
                # While not at the end of the set and while the new_range overlaps with the next
                # current range
                # Change the highest range in the new set to cover both itself and the next current
                # range in the current set
                new_ranges[-1] = (min(self.ranges[index][0], new_ranges[-1][0]),
                                  max(self.ranges[index][1], new_ranges[-1][1]))
                # Continue to the next current range
                index += 1
            if index < len(self.ranges): # If it hasn't reached the end of the current set
                # Add the rest onto the end of the new set and assign to self
                self.ranges = new_ranges + self.ranges[index:]
            else:
                # Else just assign the new ranges to self
                self.ranges = new_ranges.copy()

        return self

    def __iadd__(self, new_range):
        """
        Augmented assignment '+=' for adding a range 'new_range' to this RangeSet. The new range
        can be either a single range or a range set and can overlap with existing ranges in the set.

        Parameters
        ----------
        new_range : tuple or RangeSet
            Single range or set of ranges representing the new range to be added.

        Returns
        -------
        self : RangeSet
            Modified RangeSet with new range included.

        """
        if type(new_range) == tuple:
            self.__iadd_tuple__(new_range)

        elif type(new_range) == RangeSet:
            for new_tuple in new_range.ranges:
                self.__iadd_tuple__(new_tuple)

        return self

    def __add__(self, new_range):
        """
        Returns a new RangeSet combining the ranges of this RangeSet and 'new_range'.

        Parameters
        ----------
        new_range : tuple or RangeSet
            Single range or set of ranges representing the new range to be added.

        Returns
        -------
        copy : RangeSet
            New RangeSet with new range included.

        """
        # Create copy of this RangeSet
        copy = self.__class__([r for r in self.ranges])
        copy += new_range
        return copy

    def __eq__(self, other_set):
        """
        Returns True if this RangeSet and "other_set" are identical, False otherwise.

        Parameters
        ----------
        other_set : RangeSet
            Other RangeSet to compare to this one.

        Returns
        -------
        bool
            True if the two RangeSets are identical, else False.

        """
        # Perform elementwise comparison
        return all([i == j for i, j in zip(self.ranges, other_set.ranges)])

    def __neq__(self, other_set):
        """
        Returns False if this RangeSet and "other_set" are identical, True otherwise.

        Parameters
        ----------
        other_set : RangeSet
            Other RangeSet to compare to this one.

        Returns
        -------
        bool
            False if the two RangeSets are identical, else True.

        """
        # Perform elementwise comparison
        return any([i != j for i, j in zip(self.ranges, other_set.ranges)])

    def __len__(self):
        """
        Returns the total length of all ranges in the set, inclusively, i.e. (1, 3) has length 3.

        Returns
        -------
        length : int
            Total inclusive length of all ranges in set.

        """
        return sum([curr_range[1] - curr_range[0] + 1 for curr_range in self.ranges])

def get_input(input_file: str='Inputs/Day15_Inputs.txt') -> list:
    """
    Parse an input file and extract the coordinates of a set of sensors, along with the coordinates
    of each sensor's closest beacon.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the sensor and beacon coordinates.
        The default is 'Inputs/Day15_Inputs.txt'.

    Returns
    -------
    sensors : list of tuples
        List of sensor coordinates as tuples.

    beacons : list of tuples
        List of beacon coordinates as tuples.

    """
    # Parse input file
    file = open(input_file)
    sensors, beacons = [], []
    for line in file:
        line = line.strip().split()
        if len(line) > 0:
            # Extract coordinates and convert to integers
            sensors.append((int(line[2].split('=')[1].split(',')[0]),
                            int(line[3].split('=')[1].split(':')[0])))
            beacons.append((int(line[8].split('=')[1].split(',')[0]),
                            int(line[9].split('=')[1])))

    file.close()

    return sensors, beacons

def Day15_Part1(input_file: str='Inputs/Day15_Inputs.txt', row_of_interest: int=2000000) -> int:
    """
    Calculate how many positions in a specified row of a grid cannot contain a beacon, given the
    coordinates of a set of sensors and their closest beacons in an input file. Distance between
    sensors and beacons is calculated using "Manhattan distance".

    Parameters
    ----------
    input_file : str, optional
        Input file containing the sensor and beacon coordinates.
        The default is 'Inputs/Day15_Inputs.txt'.

    row_of_interest : int, optional
        The row to check.
        The default is 2000000.

    Returns
    -------
    number_excluded : int
        The number of positions in the specified row which cannot contain a beacon.

    """
    # Parse input file
    sensors, beacons = get_input(input_file)

    # Initialise empty RangeSet for exlcuded coordinates
    excluded_coordinates = RangeSet()
    for s, b in zip(sensors, beacons): # For each sensor and its closest beacon
        # Find the Manhattan distance between them --> corresponds to max vertical distance from
        # sensor of exlcuded region around sensor
        y_range = abs(s[0] - b[0]) + abs(s[1] - b[1])
        if s[1] - y_range <= row_of_interest <= s[1] + y_range:
            # If row of interest intersects with region excluded by sensor
            # Find max distance in row of interest from the vertical axis containing the sensor,
            # which is excluded by the sensor
            width = y_range - (abs(row_of_interest - s[1]))
            # Add excluded section of row to RangeSet
            excluded_coordinates += (s[0] - width, s[0] + width)

    # Number exluced is length of RangeSet minus the number of beacons in the row
    number_excluded = len(excluded_coordinates) - sum([b[1] == row_of_interest for b in set(beacons)])

    return number_excluded

from tqdm import tqdm

def Day15_Part2(input_file: str='Inputs/Day15_Inputs.txt',
                possible_coords: RangeSet=RangeSet([(0, 4000000)])) -> int:
    """
    Calculates the tuning frequency of the distress beacon which is located at the only point in a
    grid from 0 to 4000000 in each axis which is not excluded by a set of sensors, where the
    coordinates of each sensor and its closest beacon are given in an input file, which excludes
    any other beacons existing closer to the sensor. Distances are measured using Manhattan
    distance. The tuning frequency is found by multiplying the x coordinate of the distress beacon
    by 4000000 and then adding its y coordinate.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the sensor and beacon coordinates.
        The default is 'Inputs/Day15_Inputs.txt'.

    possible_coords : RangeSet, optional
        The range of possible coordinates in each axis for the distress beacon.
        The default is RangeSet([(0, 4000000)]).

    Returns
    -------
    tuning_frequency : int
        The tuning frequency of the distress beacon.

    """
    ###############################################################################################
    # This could definitely be done faster by rotating the diamonds created by the exlcusion
    # regions of the sensors by 45 degrees and then just comparing their boundaries, but this will
    # likely be quite complicated so maybe another time, since this brute force works in ~2 minutes
    # (or 30 seconds with the loop reversed!)
    ###############################################################################################
    # Parse input file
    sensors, beacons = get_input(input_file)
    # Loop over every row in the grid of possible coordinates and perform the same check as
    # Part 1
    for row_of_interest in tqdm(range(possible_coords.ranges[-1][1] + 1)[::-1]):
        excluded_coordinates = RangeSet([])
        for s, b in zip(sensors, beacons): # For each sensor and its closest beacon
            # Find the Manhattan distance between them --> corresponds to max vertical distance from
            # sensor of exlcuded region around sensor
            y_range = abs(s[0] - b[0]) + abs(s[1] - b[1])
            if s[1] - y_range <= row_of_interest <= s[1] + y_range:
                # If row of interest intersects with region excluded by sensor
                # Find max distance in row of interest from the vertical axis containing the sensor,
                # which is excluded by the sensor
                width = y_range - (abs(row_of_interest - s[1]))
                # Add excluded section of row to RangeSet
                excluded_coordinates += (s[0] - width, s[0] + width)

        if excluded_coordinates + possible_coords != excluded_coordinates:
            # If the full range of possible coordinates are excluded, adding the range to the
            # RangeSet does nothing, so if it changes we have found the row with available points
            # Then the column must be 1 more than the upper limit of the lower range
            tuning_frequency = (excluded_coordinates.ranges[0][1] + 1)*4000000 + row_of_interest
            return tuning_frequency
