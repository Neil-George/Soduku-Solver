import pygame
from Soduku_solver import *
from pygame.locals import *
pygame.init()

class Table:
    board = [[0, 7, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],  [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def __init__(self, width, height):
        self.rows = 9
        self.columns = 9
        self.width = width
        self.height = height
        self.cells = [[Cell(self.board[r][c], r, c, width, height) for c in range(9)] for r in range(9)]
        self.solverBoard = None
        self.CellToSolve = None

    def draw(self, screen):
        for i in range(10):
            if (i % 3 == 0) and (i != 0):
                lineWidth = 5
            else:
                lineWidth = 2

            pygame.draw.line(screen, (0, 0, 0), (0, i * (self.width / 9)), (self.width, i * (self.width / 9)), lineWidth)
            pygame.draw.line(screen, (0, 0, 0), (i * (self.width / 9), 0), (i * (self.width / 9), self.height), lineWidth)

        for r in range(9):
            for c in range(9):
                self.cells[r][c].draw(screen)
    
    def updateSolverBoard(self):
        self.solverBoard = [[self.cells[r][c].val for c in range(9)] for r in range(9)]
    
    def attempt(self, val):
        r, c = self.CellToSolve
        self.cells[r][c].setCell(val)
    
    def testValue(self,val):
        r, c = self.CellToSolve

        if (self.cells[r][c].val == 0):
            self.cells[r][c].set(val)
            self.updateSolverBoard()

            if (checkNumber(self.solverBoard, val, r, c)) and (solve(self.solverBoard)):
                return True
            else:
                self.cells[r][c].set(0)
                self.cells[r][c].setCell(0)
                self.updateSolverBoard()
                return False

    def choose(self, r, c):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].solvingCell = False
        self.cells[r][c].solvingCell = True
        self.CellToSolve = (r, c)
    
    def clear(self):
        r, c = self.CellToSolve
        if (self.cells[r][c].val == 0):
            self.cells[r][c].setCell(0)

    def click(self, position):
        if (position[0] < self.width) and (position[1] < self.height):
            xPos = position[0] // (self.width / 9)
            yPos = position[1] // (self.width / 9)
            
            return (int(yPos), int(xPos))
        else:
            return None

    def finished(self):
        for r in range(9):
            for c in range(9):
                if (self.cells[r][c].val == 0):
                    return False

        return True

class Cell:

    def __init__(self, row, col, val, height, width):
        self.row = row
        self.col = col
        self.val = val
        self.startVal = 0
        self.height = height
        self.width = width
        self.solvingCell = False

    def draw(self, screen):
        text = pygame.font.SysFont("ariel", 60)
        xPos = self.col * (self.width / 9)
        yPos = self.row * (self.width / 9)

        if (self.startVal != 0) and (self.val == 0):
            startNum = text.render(str(self.startVal), 1, (128, 128, 128))
            screen.blit(startNum, (xPos+5, yPos+5))
        elif (self.startVal != 0):
            startNum = text.render(str(self.val), 1, (0, 0, 0))
            screen.blit(startNum, (xPos + ((self.width / 9) / 2 - startNum.get_width() / 2), yPos + ((self.width / 9) / 2 - startNum.get_height() / 2)))

        if (self.solvingCell == True):
            pygame.draw.rect(screen, (255, 0, 0), (xPos, yPos, (self.width / 9), (self.width / 9)), 3)

    def set(self, val):
        self.val = val

    def setCell(self, val):
        self.startVal = val

def window(screen, board):
    screen.fill((211,211,211))
    board.draw(screen)



def main():
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Soduku Solver")
    board = Table(900, 900)
    play = True
    keyPressed = None
    
    while (play):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_BACKSPACE):
                    board.clear()
                    keyPressed = None
                if (event.key == pygame.K_1):
                    keyPressed = 1
                if (event.key == pygame.K_2):
                    keyPressed = 2
                if (event.key == pygame.K_3):
                    keyPressed = 3
                if (event.key == pygame.K_4):
                    keyPressed = 4
                if (event.key == pygame.K_5):
                    keyPressed = 5
                if (event.key == pygame.K_6):
                    keyPressed = 6
                if (event.key == pygame.K_7):
                    keyPressed = 7
                if (event.key == pygame.K_8):
                    keyPressed = 8
                if (event.key == pygame.K_9):
                    keyPressed = 9
                
                if (event.key == pygame.K_RETURN):
                    (r, c) = board.CellToSolve

                    if (board.cells[r][c].startVal != 0):
                        if (board.testValue(board.cells[r][c].startVal)):
                            print("well done")
                        else:
                            print("not correct")
                        keyPressed = None

                        if (board.finished()):
                            print("Done")
                            play = False
                
            if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
                position = pygame.mouse.get_pos()
                clickPosition = board.click(position)
                if (clickPosition):
                    board.choose(clickPosition[0], clickPosition[1])
                    keyPressed = None
            
            if (event.type == pygame.QUIT):
                play = False

        if (keyPressed != None):
            board.attempt(keyPressed)

        window(screen, board)
        pygame.display.update()

main()
pygame.quit()