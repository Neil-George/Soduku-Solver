

def displayBoard():
    for i in range(9):
        if (i != 0) and (i % 3 == 0):
            print("- - - - - - - - - - -")

        for j in range(9):
            if (j != 0) and (j % 3 == 0):
                print("| ", end = "" )
            if (j == 8):
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end = "")

def emptyCells():
    for i in range(9):
        for j in range(9):
            if (board[i][j] == 0):
                return (i, j)
    return None

def checkNumber(number, row, col):
    for i in range(9):
        if (board[row][i] == number) and (col != i):
            return False

    for j in range(9):
        if (board[j][col] == number) and (row != j):
            return False

    for i in range(row - (row % 3), (row - (row % 3)) + 3):
        for j in range(col - (col % 3), (col - (col % 3)) + 3):
            if (board[i][j] == number) and row != i and col != j:
                return False

    return True

def solve():
    if not (emptyCells()):
        return True
    else:
        row, col = emptyCells()
    
    for i in range(1, 10):
        if (checkNumber(i, row, col)):
            board[row][col] = i

            if (solve()):
                return True
                
            board[row][col] = 0
    return False


solve()
displayBoard()