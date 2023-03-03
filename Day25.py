def get_input(input_file: str='Inputs/Day25_Inputs.txt') -> list:
    """
    Parse an input file and extract a list of numbers written in SNAFU format.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the numbers.
        The default is 'Inputs/Day25_Inputs.txt'.

    Returns
    -------
    numbers : list
        Extracted list of SNAFU numbers.

    """
    # Parse input file
    with open(input_file) as f:
        numbers = [line.strip() for line in f.readlines()]

    return numbers

# Set up list of SNAFU units
S_UNITS = ["=", "-", "0", "1", "2"]

def snafu_to_dec(n: str) -> int:
    """
    Converts a number written in SNAFU format into the correpsonding decimal integer.

    SNAFU
    -----
    SNAFU numbers use powers of five at each digit instead of ten like in decimal. Starting from
    the right, you have a 1s place, a 5s place, a 25s place, a 125s place, and so on. Also, instead
    of using digits 4 through 0, the digits are 2, 1, 0, minus (written -), and double-minus
    (written =). Minus is worth -1, and double-minus is worth -2 of the corresponding power of 5.

    Parameters
    ----------
    n : str
        SNAFU number to be converted.

    Returns
    -------
    dec : int
        Converted decimal integer.

    """
    # Sum components of SNAFU number as the multiple of the corresponding power of 5, correpsonding
    # to the symbol at that position
    dec = sum((S_UNITS.index(c) - 2)*5**i for i, c in enumerate(n[::-1]))

    return dec

import math

def dec_to_snafu(n: int) -> str:
    """
    Converts a decimal integer into SNAFU format.

    SNAFU
    -----
    SNAFU numbers use powers of five at each digit instead of ten like in decimal. Starting from
    the right, you have a 1s place, a 5s place, a 25s place, a 125s place, and so on. Also, instead
    of using digits 4 through 0, the digits are 2, 1, 0, minus (written -), and double-minus
    (written =). Minus is worth -1, and double-minus is worth -2 of the corresponding power of 5.

    Parameters
    ----------
    n : str
        Decimal integer to be converted.

    Returns
    -------
    snafu : int
        Converted SNAFU number.

    """
    # Initialise list of the multiples of the powers of 5 corresponding to each position
    bits = []
    # For each power of 5 less than the given number, from highest to lowest
    for i in range(int(math.log(n, 5)) + 1)[::-1]:
        # If the required multiple of this power is 0, 1 or 2, add this multiple as normal
        if n//5**i < 3:
            bits.append(n//5**i)
            n %= 5**i
        # Else it is 3 or 4 which should be shifted to -2 or -1 respectively, so we need to add
        # 1 extra multiple of the next power of 5 up from here
        else:
            # Add the shifted multiple to the list
            bits.append((n//5**i) - 5)
            # Then starting from the power of 5 which is 1 higher than the one just added
            ind = len(bits) - 2
            # If there is a number at this position, and adding 1 to this takes it above 2 (which
            # must make it 3), we need to apply the shifting again at this power
            while ind >=0 and bits[ind] + 1 > 2:
                # Apply shifting to convert this multiple from 3 -> -2
                bits[ind] = -2
                # Then move to the next highest power
                ind -= 1
            # If we have reached the end of the while loop, either there were no higher powers to
            # alter, so we need to add an extra power one higher than the current max to the start
            # of the list
            if ind == -1:
                bits = [1] + bits
            # Else we can add one to the current power without going above 2, so just do this
            else:
                bits[ind] += 1

            # Remove the factor that was just handled from n
            n %= 5**i

    # Finally, join all the symbols correponding to each multiple together to form the SNAFU number
    snafu = ''.join(S_UNITS[i+2] for i in bits)

    return snafu

import unittest

class TestConversions(unittest.TestCase):
    """
    Test cases for conversions between decimal and SNAFU.
    """

    def test_snafu_to_dec(self):
        # Extract test cases
        with open('Inputs/Day25_TestCases.txt') as f:
            lines = [line.strip().split() for line in f.readlines() if line.strip()[0].isnumeric()]
        dec = [int(line[0]) for line in lines]
        snafu = [line[1] for line in lines]
        # Execute tests
        for d, s in zip(dec, snafu):
            self.assertEqual(snafu_to_dec(s), d)

    def test_dec_to_snafu(self):
        with open('Inputs/Day25_TestCases.txt') as f:
            lines = [line.strip().split() for line in f.readlines() if line.strip()[0].isnumeric()]
        dec = [int(line[0]) for line in lines]
        snafu = [line[1] for line in lines]
        for d, s in zip(dec, snafu):
            self.assertEqual(dec_to_snafu(d), s)

def Day25_Part1(input_file: str='Inputs/Day25_Inputs.txt') -> str:
    """
    Find the SNAFU number which corresponds to the sum of a list of SNAFU numbers given in an input
    file.

    SNAFU
    -----
    SNAFU numbers use powers of five at each digit instead of ten like in decimal. Starting from
    the right, you have a 1s place, a 5s place, a 25s place, a 125s place, and so on. Also, instead
    of using digits 4 through 0, the digits are 2, 1, 0, minus (written -), and double-minus
    (written =). Minus is worth -1, and double-minus is worth -2 of the corresponding power of 5.

    Parameters
    ----------
    filename : str, optional
        Input file giving the SNAFU numbers.
        The default is 'Inputs/Day25_Inputs.txt'.

    Returns
    -------
    snafu_sum : str
        The sum of the input numbers, in SNAFU format.

    """
    # Parse input file to extract SNAFU numbers
    numbers = get_input(input_file)

    # Convert each number to decimal and perform the sum
    dec_sum = sum(snafu_to_dec(n) for n in numbers)

    # Convert the sum back to SNAFU format
    snafu_sum = dec_to_snafu(dec_sum)#

    return snafu_sum
