import math

class SudokuCSP:
    def __init__(self, board):
        self.board = board
        self.variables = []
        self.domain = {}
        self.constraints = {}
        self.subgrid_size = int(math.sqrt(len(self.board)))

    def is_consistent(self, assignment):
        for constraint in self.constraints:
            if not constraint(assignment):
                return False
        return True
    
    def set_variables(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    self.variables.append((i,j))

    def set_domains(self):
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
print(board)
csp = SudokuCSP(board)
csp.set_variables()
# print(csp.variables)
print(csp.subgrid_size)
csp.set_domains()
print(csp.domain)
#solve(board)
# printSudoku(board)