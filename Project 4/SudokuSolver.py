import math

class SudokuCSP:
    def __init__(self, board):
        self.board = board
        self.variables = []
        self.domain = {}
        self.subgrid_size = int(math.sqrt(len(self.board)))
    
    def setVariables(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    self.variables.append((i,j))

    def setDomains(self):
        for i, j in self.variables:
            values = set(range(1, len(self.board)+1))

            # check values in row
            for k in range(len(self.board[0])):
                if k != j and self.board[i][k] in values:
                    values.remove(self.board[i][k])
            
            # check values in column
            for k in range(len(self.board)):
                if k != i and self.board[k][j] in values:
                    values.remove(self.board[k][j])
                
            # check values in subgrid
            subgrid_i = (i // self.subgrid_size) * self.subgrid_size
            subgrid_j = (j // self.subgrid_size) * self.subgrid_size
            for k in range(subgrid_i, subgrid_i + self.subgrid_size):
                for l in range(subgrid_j, subgrid_j + self.subgrid_size):
                    if (k, l) != (i, j) and self.board[k][l] in values:
                        values.remove(self.board[k][l])

            # add domain to dictionary
            self.domain[(i, j)] = values
    
    # This mehtod uses Minimum Remaining Values(MRV) heuristic in its domain.
    def selectUnassignedVariable(self, assignment):
        unassigned_variables = [var for var in self.variables if var not in assignment]
        if unassigned_variables == []:
            return None
        min_var = unassigned_variables[0]
        for var in unassigned_variables:
            if len(self.domain[var]) < len(self.domain[min_var]):
                min_var = var
        return min_var
    
    def orderDomainValues(self, var):
        if var == None:
            return None
        return sorted(self.domain[var])                 

def isConsistent(var, value, assignment, sudoku):
    # Check row consistency
    for j in range(len(sudoku.board[0])):
        if (var[0], j) in assignment and assignment[(var[0], j)] == value:
            return False

    # Check column consistency
    for i in range(len(sudoku.board)):
        if (i, var[1]) in assignment and assignment[(i, var[1])] == value:
            return False

    # Check subgrid consistency
    subgrid_i = (var[0] // sudoku.subgrid_size) * sudoku.subgrid_size
    subgrid_j = (var[1] // sudoku.subgrid_size) * sudoku.subgrid_size
    for i in range(subgrid_i, subgrid_i + sudoku.subgrid_size):
        for j in range(subgrid_j, subgrid_j + sudoku.subgrid_size):
            if (i, j) in assignment and assignment[(i, j)] == value:
                return False

    return True

def recursiveBacktracking(sudoku: SudokuCSP, assignment: dict, unassigned_variables: list):
    # Check if the assignment is complete
    if len(assignment) == len(sudoku.variables):
        return [[assignment[(i, j)] for j in range(len(sudoku.board[0]))] for i in range(len(sudoku.board))]

    # Select an unassigned variable
    var = sudoku.selectUnassignedVariable(assignment)

    # Order the domain of the variable
    ordered_domain = sudoku.orderDomainValues(var)

    # Try each value in the ordered domain
    for value in ordered_domain:
        # Check if the value is consistent with the current assignment
        if isConsistent(var, value, assignment, sudoku):
            # Add the value to the assignment
            assignment[var] = value
            unassigned_variables.remove(var)
            print(assignment)

            # Recursively call the function with the updated assignment and list of unassigned variables
            result = recursiveBacktracking(sudoku, assignment, unassigned_variables)

            # If the recursion returns a solution, return the solution
            if result != None:
                return result

            # If the recursion does not return a solution, remove the value from the assignment
            del assignment[var]
            unassigned_variables.append(var)

    # If no value in the domain results in a solution, return failure
    return None

def solve(board):
    sudoku = SudokuCSP(board)
    sudoku.setVariables()
    sudoku.setDomains()
    assignment = {}
    unassigned_variables = sudoku.variables
    return recursiveBacktracking(sudoku, assignment, unassigned_variables)

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

# Test
# Initializing a test board, empty cells are initialized with 0.
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
assignment = solve(board)
print(assignment)