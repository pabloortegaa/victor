initial_board = [
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."]]

other_board = [
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", "O", ".", ".", ".", ".", "."], 
    [".", "O", ".", ".", ".", ".", "."]]

#ee
def square_to_groups(board,player):
    groups = []
    # first we need to find the possible groups in the board
    
    # Check for vertical
    for i in range(3):
        for j in range(7):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j] == player or board[i+1][j]== ".":
                    if board[i+2][j] == player or board[i+2][j]== ".":
                        if board[i+3][j] == player or board[i+3][j]== ".":
                            groups.append([(i,j),(i+1,j),(i+2,j),(i+3,j)])
    
    # Check for horizontal
    for i in range(6):
        for j in range(4):
            if board[i][j] == player or board[i][j]== ".":
                if board[i][j+1] == player or board[i][j+1]== ".":
                    if board[i][j+2] == player or board[i][j+2]== ".":
                        if board[i][j+3] == player or board[i][j+3]== ".":
                            groups.append([(i,j),(i,j+1),(i,j+2),(i,j+3)])

    # Check for diagonal right
    for i in range(3):
        for j in range(4):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j+1] == player or board[i+1][j+1]== ".":
                    if board[i+2][j+2] == player or board[i+2][j+2]== ".":
                        if board[i+3][j+3] == player or board[i+3][j+3]== ".":
                            groups.append([(i,j),(i+1,j+1),(i+2,j+2),(i+3,j+3)])
    # Check for diagonal left
    for i in range(3):
        for j in range(3,7):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j-1] == player or board[i+1][j-1]== ".":
                    if board[i+2][j-2] == player or board[i+2][j-2]== ".":
                        if board[i+3][j-3] == player or board[i+3][j-3]== ".":
                            groups.append([(i,j),(i+1,j-1),(i+2,j-2),(i+3,j-3)])
    print(len(groups))

    square_to_group={}
    for group in groups:
        for coord in group:
            square_to_group[coord] = group
    print(square_to_group)
    return square_to_group


square_to_groups=square_to_groups(initial_board,"X")

# Convert each application of each rule into a Solution.
solutions=set()
group_to_solution={}
       
#Claimeven
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
claimevens=find_claimevens(initial_board)

def from_claimeven(claimeven,square_to_groups):
    rule="claimeven"
    groups= claimeven[0] # claimeven.upper
    if groups:
        return{"squares":claimeven,"groups":groups,"rule":rule}
    
for claimeven in claimevens:
    solution=from_claimeven(claimeven,square_to_groups)
    if solution:
        solutions.add(solution)
        if solution["groups"] not in group_to_solution:
            group_to_solution[solution["groups"]]=set()
        group_to_solution[solution["groups"]].add(solution)
    
        





            
