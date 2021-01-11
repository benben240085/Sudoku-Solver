import pprint

def backTrack(board):
    location = findEmptySpace(board)
    if location:
        #sets row and column if a location that's empty is found
        row, col = location
    else:
        #otherwise no empty spots were found and the board is a viable solution
        return True
    
    for i in range(1,10):
        #checks if the current number between 1-9 is a valid move for the current board state
        if validMove(board, (row,col), i):
            #if it is then set the row and column to that number and call backTrack again
            board[row][col] = i
            if backTrack(board):
                #if this returns true that means that this specific solution was true
                #and the board is correct
                return True
            #otherwise it isn't and it sets this iteration's empty location back to zero 
            #and tries a different number
            board[row][col] = 0
    return False


def validMove(board, pos, num):
    row, col = pos
    #checks the corresponding rows and columns to set if it's a valid move
    for i in range(0,9):
        if board[row][i] == num:
            #this means that the number is already in this row and 
            #therefore isn't a valid sudoku move
            return False
    for i in range(0,9):
        if board[i][col] == num:
            #this means that the number is already in this column and 
            #therefore isn't a valid sudoku move
            return False
    
    #checks the 3X3 box it's in

    x = col//3
    y = row//3

    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if board[i][j] == num:
                #this means that the number is already placed in the 3X3 box
                #and isn't a valid sudoku move
                return False
    return True

def findEmptySpace(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i, j
    return False


board = [
        [0,0,0,0,9,0,0,0,0],
        [0,1,8,7,0,0,0,0,0],
        [4,0,0,8,0,0,0,0,1],
        [0,6,0,0,0,8,0,0,0],
        [1,0,0,4,0,0,3,0,0],
        [0,7,0,0,0,0,8,2,9],
        [0,2,0,0,1,0,0,0,0],
        [0,0,0,9,0,4,2,7,0],
        [6,0,0,0,5,0,1,0,0]
        ]

prettyFormat = pprint.PrettyPrinter(width=35,compact=True)
backTrack(board)
prettyFormat.pprint(board)
