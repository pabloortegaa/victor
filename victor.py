from functools import reduce
from copy import copy, deepcopy
import json
import random
import time


class Game:
    def __init__(self, state, status, player):
        self.state = state
        self.status = status
        self.player = player

    def is_waiting(self):
        return self.status == 'waiting'

    def is_end(self):
        return self.status == 'complete'
    
    def get_board(self):
        return json.loads(self.state)

    def get_winner(self):
        return None

    def actions(self):
        return []

    def print(self):
        print(self.state)


class ConnectFour(Game):
    def __init__(self, state, status, player):
        Game.__init__(self, state, status, player)

    def actions(self):
        return [] # this should return the possible actions

    def get_winner(self):
        return '.' # this should return the actual winner

    def other_player(self):
        if self.player == 'O': return 'X'
        if self.player == 'X': return 'O'

    def print_game(self):
        print(self.state)


# ----------- HELPER FUNCTIONS ----------- #

def update_board(board, col, player):
    """Updates a board with a new move.
    
    Args:
        board: a list of lists representing the board
        col: the column to place the piece
        player: the player making the move
    
    Returns:
        A new board with the move made."""

    new_board = deepcopy(board)
    for i in range(5, -1, -1):
        if new_board[i][col] == '.':
            new_board[i][col] = player
        return new_board
    return None

def board_flip(board):
    """Returns a new board with the board flipped vertically.
    This allows accessing the lower row as the first item in the list."""

    new_board = deepcopy(board)
    new_board.reverse()
    return new_board

def possible_actions(board):
    """Returns a list of all directly playable actions (row, col) on a board."""
    actions = []
    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] == '.':
                actions.append((row,col))
                break
    # playable_cols = [x[1] for x in actions]
    return actions

def is_true_threat(threat):
    """Checks if the threat coordinates are true.
    
    Args:
        threat: a tuple of 2 tuples representing the threat coordinates of the start and end of the threat.
    """
    threat_start = threat[0]
    threat_end = threat[1]

    # Filter out squares further than 3 positions apart.
    row_diff = threat_start[0] - threat_end[0]
    if abs(row_diff) > 3:
        return False
    col_diff = threat_start[1] - threat_end[1]
    if abs(col_diff) > 3:
        return False
    
    # If the two squares are in the same row or column, it is possible for them to be connected.
    # The two squares can be connected diagonally only if row_diff and col_diff are the same.
    if row_diff == 0 or col_diff == 0:
        return True
    if abs(row_diff) == abs(col_diff):
        return True
    return False



# ----------- GAME RULES ----------- #

def find_claimevens(board):
    """Finds all the claimable evens on a board. Can be used to determine a winner or draw.

    Required: 2 squares directly above each other. Both squares must be empty. The upper square must be even.
    
    Returns:
        List with all the claimevens.
        Claimeven represented with (row, col) of the lower (odd) square.
    """
    claimevens = []
    for row in range(0, len(board), 2): # Steps of 2 to reach only even rows
        for col in range(len(board[0])):
            if board[row][col] == '.':
                claimevens.append((row, col))

    return claimevens

def find_baseinverses(board):
    """Finds all the baseinverses on a board.

    Required: 2 directly playable squares.
    
    Returns:
        List with all the tuples that contain both squares
    """
    baseinverses = []
    playable_actions = possible_actions(board)

    # Try all different combinations of directly playable squares.
    for square1 in playable_actions:
        for square2 in playable_actions:
            if square1 != square2 and is_true_threat((square1, square2)):
                # Note threats are only checked if coords are viable.
                # Checking whether the threat is real with current board state could benefit the algorithm.
                inverted_baseinverse = (square2, square1)
                if inverted_baseinverse not in baseinverses: # Avoid duplicates
                    baseinverses.append((square1, square2))

    return baseinverses

def find_verticals(board):
    """Finds all the verticals on a board. Function that replaces the claimeven when necessary.

    Required: 2 squares directly above each other. Both squares must be empty. The upper square must be odd.
    
    Returns:
        List with all the verticals.
        Vertical represented with (row, col) of the lower (even) square.
    """
    verticals = []
    for row in range(1, len(board)-1, 2): # Steps of 2 to reach only odd rows
        for col in range(len(board[0])):
            if board[row][col] == '.':
                verticals.append((row, col))
    return verticals

def find_after_evens():
    """Finds all the after evens on a board.

    Required: 
        A group which can be completed by the controller of the Zugzwang, using only the even
        squares of a set of Claimevens. This group is called the Aftereven group. 
        The columns in which the empty squares lie are called the Aftereven columns.
    
    Returns:
        TBD
    """
    afterevens = []
    pass


def find_low_inverses(verticals):
    """Finds all the low_inverses on a board. Returns all combinations made by 2 verticals that are possible threats.
    
    Required:
        2 different columns, each with 2 squares lying above each other.
        All for squares must be empty.
        Both columns, the upper square is odd (as in verticals).
    
    Returns:
        List with tuples of low_inverses that are possible threats.
    """
    low_inverses = []

    # Try all different combinations of verticals.
    for vertical1 in verticals:
        for vertical2 in verticals:
            if vertical1 != vertical2 and is_true_threat((vertical1, vertical2)):
                inverted_low_inverse = (vertical2, vertical1)
                if inverted_low_inverse not in low_inverses: # Avoid duplicates
                    low_inverses.append((vertical1, vertical2))
    return low_inverses

def find_high_inverses(board):
    """Finds all the high_inverses on a board. Could be seen as combinations of Claimeven + Lowinverse (with claimeven at the top).
    
    Required:
        Two different columns, each with 3 squares lying directly above each other.
        All six squares are empty.
        In both columns the upper square is even
    
    Returns:
        List with tuples of high_inverses that are possible threats.
        Inside each tuple, 2 coords that represent lowest square of the group in each column.
    """
    columns = [] # List of columns that have 3 squares above each other (with even top square)
    for row in range(1, len(board)-2, 2):
        for col in range(len(board[0])):
            # If lower square of the highinverse is empty
            if board[row][col] == '.' and col not in columns:
                columns.append(col)

    high_inverses = []
    for i in range(len(columns)):
        col1 = columns[i]
        for col2 in columns[i+1:]:
            for row_col1 in range(1, len(board)-2, 2):
                for row_col2 in range(1, len(board)-2, 2):
                    if board[row_col1][col1] == '.' and board[row_col2][col2] == '.' and is_true_threat(((row_col1, col1), (row_col2, col2))):
                        inverted_highinverse = ((row_col2, col2), (row_col1, col1))
                        if inverted_highinverse not in high_inverses: # Avoid duplicates
                            high_inverses.append(((row_col1, col1), (row_col2, col2)))
    return high_inverses



# ----------- TESTING ----------- #

initial_board = board_flip([
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."]])

diagram6_1 = board_flip([
    [".", ".", ".", "X", ".", ".", "."], 
    [".", ".", ".", "O", ".", ".", "."], 
    [".", ".", ".", "X", ".", ".", "."], 
    [".", ".", ".", "O", ".", ".", "."], 
    [".", ".", ".", "X", ".", ".", "."], 
    [".", ".", "X", "O", "O", ".", "."]])

test_diagram = diagram6_1

print("Board:")
for row in board_flip(test_diagram):
    print(row)
print("Possible actions: ", possible_actions(test_diagram))

start = time.time()
claimevens = find_claimevens(test_diagram)
baseinverses = find_baseinverses(test_diagram)
verticals = find_verticals(test_diagram)
low_inverses = find_low_inverses(verticals)
high_inverses = find_high_inverses(test_diagram)
end = time.time()

print("Seconds taken: ", end - start)
print("Claimevens: ", claimevens)
print("Baseinverses: ", baseinverses)
print("Verticals: ", verticals)
print("Low_inverses: ", low_inverses)
print("High_inverses: ", high_inverses)