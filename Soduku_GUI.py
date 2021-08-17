import pygame
from Soduku_solver import *
from pygame.locals import *
pygame.init()

class Table:
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],  [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]


    def __init__(self, width, height):
        self.rows = 9
        self.columns = 9
        self.width = width
        self.height = height
        self.cells = [[Cell(r, c, self.board[r][c], height, width) for c in range(9)] for r in range(9)]
        self.solverBoard = None
        self.CellToSolve = None

    def draw(self, screen):
        for i in range(10):
            if (i % 3 == 0) and (i != 0):
                lineWidth = 4
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
            xPos = (position[0] * 9) // self.width
            yPos = (position[1] * 9) // self.width
            
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
        text = pygame.font.SysFont("ariel", 40)
        xPos = self.col * (self.width / 9)
        yPos = self.row * (self.width / 9)

        if (self.startVal != 0) and (self.val == 0):
            startNum = text.render(str(self.startVal), 1, (0, 0, 0))
            screen.blit(startNum, (xPos + ((self.width / 9) / 2 - startNum.get_width() / 2), yPos + ((self.width / 9) / 2 - startNum.get_height() / 2)))
        elif (self.val != 0):
            startNum = text.render(str(self.val), 1, (0, 0, 0))
            screen.blit(startNum, (xPos + ((self.width / 9) / 2 - startNum.get_width() / 2), yPos + ((self.width / 9) / 2 - startNum.get_height() / 2)))

        if (self.solvingCell == True):
            pygame.draw.rect(screen, (255,255,153), (xPos, yPos, (self.width / 9), (self.width / 9)), 7)

    def set(self, val):
        self.val = val

    def setCell(self, val):
        self.startVal = val


class Button:

    def __init__(self, width, height, label, position, colour, hoverColour):
        self.distance = 5
        self.position = position
        self.topColour = colour
        self.bottomColour = hoverColour
        self.topButton = pygame.Rect(position, (width, height))
        self.bottomButton = pygame.Rect(position, (width, height))
        self.font = pygame.font.Font(None, 30)
        self.label = self.font.render(label, True, (255, 255, 255))
        self.labelButton = self.label.get_rect(center = self.topButton.center)
        self.clicked = False

    def draw(self, screen):
        self.labelButton.center = self.topButton.center
        self.topButtonPosition = self.position[1] - self.distance
        self.bottomButton.midtop = self.topButton.midtop
        self.bottomButton.height = self.topButton.height + self.distance
        
        pygame.draw.rect(screen, self.bottomColour, self.bottomButton, border_radius = 10)
        pygame.draw.rect(screen, self.topColour, self.topButton, border_radius = 10)
        
        screen.blit(self.label, self.labelButton)
        self.click(self.topColour, self.distance)

    def click(self, topColour, distance):
        mouse = pygame.mouse.get_pos()
        
        if (self.topButton.collidepoint(mouse)):
            self.topColour = self.bottomButton

            if (pygame.mouse.get_pressed()[0]):
                self.distance = 0
                self.clicked = True
            else:
                self.distance = distance

                if (self.clicked):
                    self.clicked = False
        else:
            self.distance = distance
            self.topColour = topColour



def window(screen, board, button):
    screen.fill((211,211,211))
    board.draw(screen)
    button.draw(screen)



def main():
    size = 600
    screen = pygame.display.set_mode((size, size+60))
    pygame.display.set_caption("Soduku Solver")
    solveButton = Button(200, 40, "Solve", (size-210, size+10), (153,50,204), (100,149,237))
    board = Table(size, size)
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

            if (event.type == pygame.QUIT):
                play = False
                
            if (event.type == pygame.MOUSEBUTTONDOWN):
                position = pygame.mouse.get_pos()
                if (board.click(position) != None):
                    r, c = board.click(position)
                    board.choose(r, c)
                    keyPressed = None
            

        if (board.CellToSolve) and (keyPressed != None):
            board.attempt(keyPressed)

        window(screen, board, solveButton)
        pygame.display.update()

main()
pygame.quit()