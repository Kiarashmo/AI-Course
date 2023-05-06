import time

def solve_sudoku(board):
    """
    Solves the given Sudoku board using the backtracking algorithm with LCV, MRV, and forward checking heuristics.
    """
    # Find an empty cell with the fewest remaining values in its domain
    row, col = find_empty_cell(board)
    
    # If there are no empty cells, the board is solved
    if row == col == -1:
        return True
    
    # Get the domain of possible values for the empty cell
    domain = get_domain(board, row, col)
    
    # Try all possible values for the empty cell, sorted by increasing conflicts
    for val in sorted(domain, key=lambda val: is_valid_move(board, row, col, val)):
        if is_valid_move(board, row, col, val) == 0:
            # Try this value
            board[row][col] = val
            
            # Propagate the constraints of this assignment to the domains of the remaining empty cells
            if forward_check(board, row, col, val):
                # Recursively solve the rest of the board
                if solve_sudoku(board):
                    return True
                
            # If the recursion didn't succeed, backtrack and undo the constraints propagation
            board[row][col] = 0
            undo_forward_check(board, row, col, val)
    
    # If no value worked, the board is unsolvable
    return False

def forward_check(board, row, col, val):
    """
    Propagates the constraints of the given assignment to the domains of the remaining empty cells.
    Returns True if the propagation is successful, False otherwise.
    """
    # Remove the assigned value from the domains of the empty cells in the same row
    for j in range(9):
        if j != col and board[row][j] == 0:
            domain = get_domain(board, row, j)
            if val in domain:
                domain.remove(val)
                if len(domain) == 0:
                    return False
    
    # Remove the assigned value from the domains of the empty cells in the same column
    for i in range(9):
        if i != row and board[i][col] == 0:
            domain = get_domain(board, i, col)
            if val in domain:
                domain.remove(val)
                if len(domain) == 0:
                    return False
    
    # Remove the assigned value from the domains of the empty cells in the same box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i, j) != (row, col) and board[i][j] == 0:
                domain = get_domain(board, i, j)
                if val in domain:
                    domain.remove(val)
                    if len(domain) == 0:
                        return False
    
    return True

def undo_forward_check(board, row, col, val):
    """
    Undoes the constraints propagation of the given assignment to the domains of the remaining empty cells.
    """
    # Add the assigned value back to the domains of the empty cells in the same row
    for j in range(9):
        if j != col and board[row][j] == 0:
            domain = get_domain(board, row, j)
            if val not in domain:
                domain.add(val)
    
    # Add the assigned value back to the domains of the empty cells in the same column
    for i in range(9):
        if i != row and board[i][col] == 0:
            domain = get_domain(board, i, col)
            if val not in domain:
                domain.add(val)
    
    # Add the assigned value back to the domains of the empty cells in the same box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i, j) != (row, col) and board[i][j] == 0:
                domain = get_domain(board, i, j)
                if val not in domain:
                    domain.add(val)

def get_domain(board, row, col):
    """
    Returns the domain of possible values for the given cell.
    """
    domain = set(range(1, 10))
    # Check row
    for val in board[row]:
        domain.discard(val)
    # Check column
    for i in range(9):
        val = board[i][col]
        if val in domain:
            domain.discard(val)
    # Check box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            val = board[i][j]
            if val in domain:
                domain.discard(val)
    return domain

def find_empty_cell(board):
    """
    Finds the next empty cell in the board with the fewest remaining values in its domain.
    Returns (row, col) of the empty cell or (-1, -1) if no cell is empty.
    """
    min_domain_size = float('inf')
    min_row, min_col = -1, -1
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                domain = get_domain(board, row, col)
                domain_size = len(domain)
                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    min_row, min_col = row, col
    return (min_row, min_col) if min_row != -1 else (-1, -1)

def get_domain(board, row, col):
    """
    Returns the domain of possible values for the given cell.
    """
    domain = set(range(1, 10))
    # Check row
    for val in board[row]:
        domain.discard(val)
    # Check column
    for i in range(9):
        val = board[i][col]
        if val in domain:
            domain.discard(val)
    # Check box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            val = board[i][j]
            if val in domain:
                domain.discard(val)
    return domain

def is_valid_move(board, row, col, val):
    """
    Checks if placing the given value at the given position is valid.
    Returns the number of conflicts that this move would create in the remaining empty cells.
    """
    conflicts = 0
    
    # Check row
    for j in range(9):
        if j != col and board[row][j] == val:
            conflicts += 1
    
    # Check column
    for i in range(9):
        if i != row and board[i][col] == val:
            conflicts += 1
    
    # Check box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i, j) != (row, col) and board[i][j] == val:
                conflicts += 1
    
    return conflicts


def printSudoku(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print(".....................")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            if j == len(board[0])-1:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def setBoard():
    board = list()
    sudokuBoard = '''200080300
060070084
030500209
000105408
000000000
402706000
301007040
720040060
004010003'''
    rows = sudokuBoard.split('\n')
    for row in rows:
        column = list()
        for character in row:
            digit = int(character)
            column.append(digit)
        board.append(column)
    return board

board = setBoard()
printSudoku(board)
print("=============================================")
start_time = time.time()
bool = solve_sudoku(board)
end_time = time.time()
printSudoku(board)
print(end_time - start_time)

