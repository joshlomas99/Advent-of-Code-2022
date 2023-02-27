import re

def get_input(input_file: str='Inputs/Day22_Inputs.txt') -> list:
    """
    Parse an input file giving the layout of a board of paths and walls, and a path to take through
    it.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the board layout and path.
        The default is 'Inputs/Day22_Inputs.txt'.

    Returns
    -------
    board_rows : list(str)
        List of the rows of the board from top to bottom with paths marked as dots, walls marked as
        hashes and whitespace being off the board.
    board_cols : list(str)
        List of the columns of the board from left to right with paths marked as dots, walls marked
        as hashes and whitespace being off the board.
    path : list(str)
        The instructions for the path which should be taken.

    """
    # Parse input file
    with open(input_file) as f:
         lines = f.readlines()

    # Extract the board
    raw_board = [line.strip('\n') for line in lines[:-2]]
    max_len = max(len(r) for r in raw_board)
    # Format the rows and columns
    board_rows = [line + ' '*(max_len - len(line)) for line in raw_board]
    board_cols = [''.join(r[c] for r in board_rows) for c in range(len(board_rows[0]))]

    # Extract and format the path
    path = re.findall('\d+|[A-Z]', lines[-1].strip())

    return board_rows, board_cols, path

import numpy as np

def move(pos: tuple, facing: int, move: int, board: tuple) -> tuple:
    """
    Move a given number of places across a board from a given starting position in a given
    direction. If you run into a wall ('#'), you stop moving. If a movement would take you off the
    board, you wrap around to the other side.

    Parameters
    ----------
    pos : tuple(int, int)
        Current coordinates on the board in the form (row, column).
    facing : int
        The direction you are facing in. 0 is right (+row), 1 is down (+column), 2 is left (-row)
        and 3 is up (-column).
    move : int
        The maximum number of places to move.
    board : tuple(list(str))
        Tuple of two orientations of board layout in the form (board_rows, board_cols).

    Returns
    -------
    pos : tuple(int, int)
        Final coordinates on the board in the form (row, column).

    """
    board_rows, board_cols = board
    # Horizontal movement
    if facing in [0, 2]:
        curr_row = board_rows[pos[0]]
        # Find the start and end positions of the current row (between the whitespace)
        try:
            row_start = np.where(np.array(list(curr_row[:max(1, pos[1])])) == ' ')[0][-1]+1
        except IndexError:
            row_start = 0
        try:
            row_end = pos[1] + np.where(np.array(list(curr_row[pos[1]:])) == ' ')[0][0] - 1
        except IndexError:
            row_end = len(curr_row) - 1
        # Find the length of the row
        row_len = row_end - row_start + 1
        # Right movement
        if facing == 0:
            # If the movement won't reach the end of the row
            if pos[1] + move <= row_end:
                # Try and find a wall in the movement path
                try:
                    # If found, stop at the wall
                    pos = (pos[0], pos[1] + curr_row[pos[1]: pos[1] + move + 1].index('#') - 1)
                except ValueError:
                    # Else do the whole movement
                    pos = (pos[0], pos[1] + move)

            # If the movement will go off the board, wrap around
            else:
                # Try and find a wall in the movement path before the first wrap
                try:
                    # If found, stop at the wall
                    pos = (pos[0], pos[1] + curr_row[pos[1]: row_end + 1].index('#') - 1)
                except ValueError:
                    # Else try and find a wall from the row start until the end of the movement
                    try:
                        # If found, stop at the wall
                        pos = (pos[0], row_start + (curr_row[row_start:(pos[1] + move)%row_end + row_start + 1].index('#') - 1)%row_len)
                    except ValueError:
                        # Else do the whole movement
                        pos = (pos[0], (pos[1] + move - row_start)%row_len + row_start)
        # Left movement - same logic as above with opposite movement
        if facing == 2:
            if pos[1] - move >= row_start:
                try:
                    pos = (pos[0], pos[1] - (move - (1 + curr_row[pos[1] - move: pos[1]].rindex('#'))))
                except ValueError:
                    pos = (pos[0], pos[1] - move)

            else:
                try:
                    pos = (pos[0], row_start + curr_row[row_start: pos[1]].rindex('#') + 1)
                except ValueError:
                    try:
                        pos = (pos[0], (pos[1] - move + curr_row[(pos[1] - move - row_start)%row_len + row_start: row_end + 1].rindex('#') + 1 - row_start)%row_len + row_start)
                    except ValueError:
                        pos = (pos[0], (pos[1] - move - row_start)%row_len + row_start)

    # Vertical movement - same logic as above but with columns instead of rows
    else:
        curr_col = board_cols[pos[1]]
        try:
            col_start = np.where(np.array(list(curr_col[:max(1, pos[0])])) == ' ')[0][-1]+1
        except IndexError:
            col_start = 0
        try:
            col_end = pos[0] + np.where(np.array(list(curr_col[pos[0]:])) == ' ')[0][0] - 1
        except IndexError:
            col_end = len(curr_col) - 1
        col_len = col_end - col_start + 1
        if facing == 1:
            if pos[0] + move <= col_end:
                try:
                    pos = (pos[0] + curr_col[pos[0]: pos[0] + move + 1].index('#') - 1, pos[1])
                except ValueError:
                    pos = (pos[0] + move, pos[1])

            else:
                try:
                    pos = (pos[0] + curr_col[pos[0]: col_end + 1].index('#') - 1, pos[1])
                except ValueError:
                    try:
                        pos = (col_start + (curr_col[col_start:(pos[0] + move)%col_end + col_start + 1].index('#') - 1)%col_len, pos[1])
                    except ValueError:
                        pos = ((pos[0] + move - col_start)%col_len + col_start, pos[1])

        if facing == 3:
            if pos[0] - move >= col_start:
                try:
                    pos = (pos[0] - (move - (1 + curr_col[pos[0] - move: pos[0]].rindex('#'))), pos[1])
                except ValueError:
                    pos = (pos[0] - move, pos[1])

            else:
                try:
                    pos = (col_start + curr_col[col_start: pos[0]].rindex('#') + 1, pos[1])
                except ValueError:
                    try:
                        pos = ((pos[0] - move + curr_col[(pos[0] - move - col_start)%col_len + col_start: col_end + 1].rindex('#') + 1 - col_start)%col_len + col_start, pos[1])
                    except ValueError:
                        pos = ((pos[0] - move - col_start)%col_len + col_start, pos[1])

    return pos

# right 0
# down 1
# left 2
# up 3

import unittest

class TestMove(unittest.TestCase):
    """
    Unit tests for different movement cases.

    """
    def testRight_notBlocked(self):
        board = get_input('Inputs/Day22_ExtraTestInputs.txt')[:2]
        self.assertEqual(move((5, 6), 0, 10, board), (5, 4))
        self.assertEqual(move((5, 7), 0, 10, board), (5, 4))
        self.assertEqual(move((5, 4), 0, 10, board), (5, 4))

    def testDown_notBlocked(self):
        board = get_input('Inputs/Day22_ExtraTestInputs.txt')[:2]
        self.assertEqual(move((6, 5), 1, 10, board), (4, 5))
        self.assertEqual(move((7, 5), 1, 10, board), (4, 5))
        self.assertEqual(move((4, 5), 1, 10, board), (4, 5))

    def testLeft_notBlocked(self):
        board = get_input('Inputs/Day22_ExtraTestInputs.txt')[:2]
        self.assertEqual(move((6, 5), 2, 10, board), (6, 7))
        self.assertEqual(move((6, 4), 2, 10, board), (6, 7))
        self.assertEqual(move((6, 7), 2, 10, board), (6, 7))

    def testUp_notBlocked(self):
        board = get_input('Inputs/Day22_ExtraTestInputs.txt')[:2]
        self.assertEqual(move((5, 6), 3, 10, board), (7, 6))
        self.assertEqual(move((4, 6), 3, 10, board), (7, 6))
        self.assertEqual(move((7, 6), 3, 10, board), (7, 6))

    def testRight_blocked(self):
        board = get_input('Inputs/Day22_ExtraTestInputs.txt')[:2]
        self.assertEqual(move((0, 1), 0, 10, board), (0, 3))
        self.assertEqual(move((0, 2), 0, 10, board), (0, 3))
        self.assertEqual(move((0, 3), 0, 10, board), (0, 3))

    def testDown_blocked(self):
        board = get_input('Inputs/Day22_ExtraTestInputs.txt')[:2]
        self.assertEqual(move((1, 0), 1, 10, board), (3, 0))
        self.assertEqual(move((2, 0), 1, 10, board), (3, 0))
        self.assertEqual(move((3, 0), 1, 10, board), (3, 0))

    def testLeft_blocked(self):
        board = get_input('Inputs/Day22_ExtraTestInputs.txt')[:2]
        self.assertEqual(move((3, 2), 2, 10, board), (3, 0))
        self.assertEqual(move((3, 1), 2, 10, board), (3, 0))
        self.assertEqual(move((3, 0), 2, 10, board), (3, 0))

    def testUp_blocked(self):
        board = get_input('Inputs/Day22_ExtraTestInputs.txt')[:2]
        self.assertEqual(move((2, 3), 3, 10, board), (0, 3))
        self.assertEqual(move((1, 3), 3, 10, board), (0, 3))
        self.assertEqual(move((0, 3), 3, 10, board), (0, 3))

def Day22_Part1(input_file: str='Inputs/Day22_Inputs.txt') -> int:
    """
    Find the password given as the sum of 1000 times the row, 4 times the column, and the facing of
    your final position after following a set of instructions to move around a board, the layout
    of which is given in an input file. You begin the path in the leftmost open tile of the top row
    of tiles. Initially, you are facing to the right (from the perspective of how the map is drawn).

    Movement
    --------
    Movement instructions consist of alternating numbers and letters. A number indicates the number
    of tiles to move in the direction you are facing. If you run into a wall, you stop moving
    forward and continue with the next instruction. A letter indicates whether to turn 90 degrees
    clockwise (R) or counterclockwise (L). Turning happens in-place; it does not change your
    current tile. If a movement would take you off of the board, you wrap around to the other side.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the board layout and movement instructions.
        The default is 'Inputs/Day22_Inputs.txt'.

    Returns
    -------
    password : int
        The password generated from your final position.

    """
    # Parse input file to get board layout and path instructions
    board_rows, board_cols, path = get_input(input_file)

    # Set starting position and facing
    pos = (0, board_rows[0].index('.'))
    facing = 0

    # For each instruction
    for instruction in path:
        # If it is a turn, change the facing accordingly
        if instruction.isalpha():
            if instruction == 'R':
                facing = (facing + 1)%4
            elif instruction == 'L':
                facing = (facing - 1)%4

        # Else execute the corresponding move
        else:
            pos = move(pos, facing, int(instruction), (board_rows, board_cols))

    # Calculate the final password
    password = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing
    return password
    
import typing

class Face(typing.NamedTuple):
    """
    Class describing a face of a cube with a given normal and rotation relative to some set
    reference.
    """
    normal: tuple
    rotation: int

# Set of possible directions on a face
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
# +x = right (1, 0, 0)
# -x = left (-1, 0, 0)
# +y = up (0, 1, 0)
# -y = down (0, -1, 0)
# +z = forwards (0, 0, 1)
# -z = backwards (0, 0, -1)

# List of connections between faces, with rotations corresponding to the connected edges on each
# face, on an arbitrary example cube, which we can map our map onto
FACE_CONNECTIONS = {Face((-1, 0, 0), 0): Face((0, -1, 0), 2),
                    Face((-1, 0, 0), 1): Face((0, 0, -1), 3),
                    Face((-1, 0, 0), 2): Face((0, 1, 0), 0),
                    Face((-1, 0, 0), 3): Face((0, 0, 1), 1),
                    Face((0, -1, 0), 0): Face((1, 0, 0), 0),
                    Face((0, -1, 0), 1): Face((0, 0, -1), 0),
                    Face((0, -1, 0), 3): Face((0, 0, 1), 0),
                    Face((0, 0, -1), 1): Face((1, 0, 0), 3),
                    Face((0, 0, -1), 2): Face((0, 1, 0), 1),
                    Face((0, 0, 1), 2): Face((0, 1, 0), 3),
                    Face((0, 0, 1), 3): Face((1, 0, 0), 1),
                    Face((0, 1, 0), 2): Face((1, 0, 0), 2)}

# Add the reverse connections
FACE_CONNECTIONS.update({v: k for k, v in FACE_CONNECTIONS.items()})

def buildCube(board: tuple) -> tuple:
    """
    Find the positions of six faces of a cube within a 2D board and then find the normal of each
    face, and the rotation of each face in this cube, relative to an given arbitrary example cube.

    Parameters
    ----------
    board : tuple(list(str))
        Tuple of two orientations of board layout in the form (board_rows, board_cols).

    Returns
    -------
    found_faces : dict(tuple: Face)
        The faces of the cube, with their corresponding normals and rotations, hashed by the
        positions of their corners in the original board divided by the cube side length.
    found_face_corners : dict(tuple, tuple)
        The positions of the corners of each cube face in the original board divided by the cube
        side length, hashed by the normal of that face.
    cube_side_length : int
        The side length of the final cube.

    """
    # Get the two board layouts
    board_rows, board_cols = board

    # Calculate the cube side length as the count of all points, divided by 6, square rooted
    cube_side_length = int((sum([r.count('.') + r.count('#') for r in board_rows])/6)**0.5)

    # Find the corner of the first face
    first_face_corner = (0, board_rows[0].index('.')//cube_side_length)

    # Initialise found_faces dictionary with first face
    found_faces = {first_face_corner: Face((-1, 0, 0), 0)}

    # Create queue of faces to check
    queue = [first_face_corner]

    # Perform BFS search through the board to find each cube face
    while queue:
        curr_face_corner = queue.pop(0)
        curr_face = found_faces[curr_face_corner]
        # For each face, check in each direction
        for rot, (dx, dy) in enumerate(DIRECTIONS):
            next_face_corner = (curr_face_corner[0] + dx, curr_face_corner[1] + dy)
            # Skip found faces
            if next_face_corner in found_faces:
                continue
            # Do not consider outside the board boundaries
            if not (0 <= next_face_corner[0]*cube_side_length < len(board_rows) and \
                    0 <= next_face_corner[1]*cube_side_length < len(board_rows[0])):
                continue
            # Skip empty sections
            if board_rows[next_face_corner[0]*cube_side_length][next_face_corner[1]*cube_side_length].isspace():
                continue

            # Find the edge we are leaving the current face from
            curr_edge = Face(curr_face.normal, (curr_face.rotation + rot) % len(DIRECTIONS))
            # Find the edge connected to that edge on the example cube
            connected_template_edge = FACE_CONNECTIONS[curr_edge]
            # Calculate the rotation to convert between the cubes: you expect the direction to
            # change by two moving between edges (e.g. right edge (0) -> left edge (2), so find
            # expected new edge as (rot + 2) [+/-2 is irrelavant as will all be mod 4 eventually],
            # then find difference between that and the actual new edge from the example cube
            # (connected_template_edge.rotation). Then modulus as the rotations wrap around.
            extra_rotation = (connected_template_edge.rotation - (rot + 2)) % len(DIRECTIONS)
            # Construct the new face with the extra rotation and add to found_faces
            found_faces[next_face_corner] = Face(connected_template_edge.normal, extra_rotation)
            # Continue BFS
            queue.append(next_face_corner)

    # Build dict of corners from normals
    found_face_corners = {face.normal: corner for corner, face in found_faces.items()}

    return found_faces, found_face_corners, cube_side_length

def move_on_cube(pos: tuple, facing: int, board: tuple, cube_side_length: int, found_faces: dict,
                 found_face_corners: dict) -> tuple:
    """
    Determines the new coordinates on a cube, relative to the 2D net of that cube on a board, after
    moving one place from a given starting position, facing in a given direction. If you run into a
    wall ('#') you stop moving. If a movement would take you off the current cube face, you wrap
    around to the connected face in that direction.

    Parameters
    ----------
    pos : tuple(int, int)
        Current coordinates on the cube in the form (row, column).
    facing : int
        The direction you are facing in. 0 is right (+row), 1 is down (+column), 2 is left (-row)
        and 3 is up (-column).
    board : tuple(list(str))
        Tuple of two orientations of board layout in the form (board_rows, board_cols).
    cube_side_length : int
        The side length of the cube.
    found_faces : dict(tuple: Face)
        The faces of the cube, with their corresponding normals and rotations, hashed by the
        positions of their corners in the original board divided by the cube side length.
    found_face_corners : dict(tuple, tuple)
        The positions of the corners of each cube face in the original board divided by the cube
        side length, hashed by the normal of that face.

    Raises
    ------
    Unknown new facing : Exception
        Next facing calculated not in [0, 1, 2, 3].

    Unknown position type : Exception
        Next position on board is not in ['.', '#'].

    Returns
    -------
    pos : tuple(int, int)
        New coordinates on the cube after movement in the form (row, column).        
    facing : int
        New direction you are facing in. 0 is right (+row), 1 is down (+column), 2 is left (-row)
        and 3 is up (-column).
    """
    # Get the two board layouts
    board_rows, board_cols = board

    # Find the corner number of the cube face corresponding to the current board position
    curr_face_corner = (pos[0]//cube_side_length, pos[1]//cube_side_length)

    # Move one space in the facing direction
    next_pos = (pos[0] + DIRECTIONS[facing][0], pos[1] + DIRECTIONS[facing][1])
    # Find the new corresponding cube face
    next_face_corner = (next_pos[0]//cube_side_length, next_pos[1]//cube_side_length)
    next_facing = facing

    # If the cube face changed, need to apply wrapping conditions to move to the correct new face
    if next_face_corner != curr_face_corner:

        # Find current face and rotation
        curr_face = found_faces[curr_face_corner]
        # Find the edge we are leaving the current face from
        curr_edge = Face(curr_face.normal, (curr_face.rotation + facing) % len(DIRECTIONS))
        # Find the connected edge on the template cube
        connected_template_edge = FACE_CONNECTIONS[curr_edge]
        # Find the corresponding face corner on our cube
        next_face_corner = found_face_corners[connected_template_edge.normal]
        # Find the corresponding face on our cube
        next_face = found_faces[next_face_corner]
        # Find which direction we are entering the new face in
        next_facing = ((connected_template_edge.rotation + 2) - next_face.rotation) % len(DIRECTIONS)
        # Find the current position in the new face relative to the top right corner
        curr_pos_in_face = (pos[0] % cube_side_length, pos[1] % cube_side_length)

        # Find new relative position within new face depending on orientation of old and new faces
        # Only one coordinate is dependant on the old face in each case, with the other fixed given
        # that we must be on a certain edge of the new face, depending on the direction we are
        # facing.
        if facing == 0:
            if next_facing in [1, 2]:
                dep_coord = cube_side_length - 1 - curr_pos_in_face[0]
            else:
                dep_coord = curr_pos_in_face[0]
        if facing == 1:
            if next_facing in [0, 3]:
                dep_coord = cube_side_length - 1 - curr_pos_in_face[1]
            else:
                dep_coord = curr_pos_in_face[1]
        if facing == 2:
            if next_facing in [0, 3]:
                dep_coord = cube_side_length - 1 - curr_pos_in_face[0]
            else:
                dep_coord = curr_pos_in_face[0]
        if facing == 3:
            if next_facing in [1, 2]:
                dep_coord = cube_side_length - 1 - curr_pos_in_face[1]
            else:
                dep_coord = curr_pos_in_face[1]

        # Use the calculated dependant coordinate to construct the relative position in the new
        # face, given the new orientation in that face.
        if next_facing == 0:
            next_pos_in_face = (dep_coord, 0)
        elif next_facing == 1:
            next_pos_in_face = (0, dep_coord)
        elif next_facing == 2:
            next_pos_in_face = (dep_coord, cube_side_length - 1)
        elif next_facing == 3:
            next_pos_in_face = (cube_side_length - 1, dep_coord)
        else:
            raise Exception(f'Unknown next facing {next_facing}')

        # Calculate the corresponding absolute position on the board
        next_pos = (next_face_corner[0]*cube_side_length + next_pos_in_face[0],
                   next_face_corner[1]*cube_side_length + next_pos_in_face[1])

    # If the next space is open, move into it
    if board_rows[next_pos[0]][next_pos[1]] == '.':
        return next_pos, next_facing
    # If the next space is a wall, do not move
    elif board_rows[next_pos[0]][next_pos[1]] == '#':
        return pos, facing
    else:
        raise Exception(f'Unknown position type {board_rows[next_pos[0]][next_pos[1]]}')

class TestMoveOnCube(unittest.TestCase):
    """
    Unit tests for different movement cases on the cube.

    """
    def testRight_notBlocked(self):
        board = get_input('Inputs/Day22_TestInputs.txt')[:2]
        found_faces, found_face_corners, cube_side_length = buildCube(board)
        self.assertEqual(move_on_cube((5, 11), 0, board, cube_side_length, found_faces,
                                      found_face_corners), ((8, 14), 1))

    def testDown_notBlocked(self):
        board = get_input('Inputs/Day22_TestInputs.txt')[:2]
        found_faces, found_face_corners, cube_side_length = buildCube(board)
        self.assertEqual(move_on_cube((11, 10), 1, board, cube_side_length, found_faces,
                                      found_face_corners), ((7, 1), 3))

def Day22_Part2(input_file: str='Inputs/Day22_Inputs.txt') -> int:
    """
    Find the password given as the sum of 1000 times the row, 4 times the column, and the facing of
    your final position after following a set of instructions to move around a board, the layout
    of which is given in an input file. You begin the path in the leftmost open tile of the top row
    of tiles. Initially, you are facing to the right (from the perspective of how the map is drawn).
    However, now the board is not simply a 2D grid but is the net of a 2D cube, and therefore if a
    movement would take you off the board, instead of wrapping to the opposite side of the board,
    you proceed around the 3D cube corresponding to the 2D net.

    Movement
    --------
    Movement instructions consist of alternating numbers and letters. A number indicates the number
    of tiles to move in the direction you are facing. If you run into a wall, you stop moving
    forward and continue with the next instruction. A letter indicates whether to turn 90 degrees
    clockwise (R) or counterclockwise (L). Turning happens in-place; it does not change your
    current tile. If a movement would take you off the board, you proceed around the 3D cube
    corresponding to the 2D net created by the board.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the board layout and movement instructions.
        The default is 'Inputs/Day22_Inputs.txt'.

    Returns
    -------
    password : int
        The password generated from your final position.

    """
    # Parse input file to get board layout and path instructions
    board_rows, board_cols, path = get_input(input_file)

    # Construct the corresponding cube and find the connections between each face
    found_faces, found_face_corners, cube_side_length = buildCube((board_rows, board_cols))

    # Set the starting position and facing
    pos = (0, board_rows[0].index('.'))
    facing = 0

    # For each instruction
    for instruction in path:
        # If it is a turn, change the facing accordingly
        if instruction.isalpha():
            if instruction == 'R':
                facing = (facing + 1)%4
            elif instruction == 'L':
                facing = (facing - 1)%4
    
        # Else execute the corresponding move
        else:
            # Now moving one step at a time with the move_on_cube function
            for i in range(int(instruction)):
                pos, facing = move_on_cube(pos, facing, (board_rows, board_cols), cube_side_length,
                                           found_faces, found_face_corners)
    
    # Calculate the final password
    password = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing
    return password
