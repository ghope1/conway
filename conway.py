import pygame
import random
SCREEN_HEIGHT = 100;
SCREEN_WIDTH = 100;
SCALE = 4;
UPDATES_PER_SEC = 3;
FPS = 60;
# pygame setup process
pygame.init()
screenDisplay = pygame.display.set_mode((SCREEN_WIDTH*SCALE, SCREEN_HEIGHT*SCALE))
clock = pygame.time.Clock()
currRunning = True

class pixel:
    def __init__(self, aliveStatus, age):
        self.aliveStatus= aliveStatus
        self.age = age
    
    def invertStatus(self):
        self.aliveStatus = not self.aliveStatus;


def updateBoard(currBoard):
    nextBoard = [pix for pix in currBoard]
    for i in range(len(currBoard)):
        currPixel = currBoard[i]
        currPixelX = i % SCREEN_WIDTH
        currPixelY = i // SCREEN_HEIGHT
        currPixelStatus = pixelSt(currPixelX, currPixelY, currBoard)
        if currPixel.aliveStatus and currPixelStatus:
            nextBoard[i].age += 1
        elif currPixel.aliveStatus and not currPixelStatus:
            nextBoard[i].age == 0
        nextBoard[i].aliveStatus = currPixelStatus

    return nextBoard

# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction

def pixelSt(x, y, currBoard):
    currPixel = currBoard[x + y*SCREEN_HEIGHT]
    aliveNextFrame = currPixel.aliveStatus
    numNeighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) + abs(j) != 0 and 0 <= x+i and x+i < SCREEN_WIDTH and 0 <= y+j and y+j < SCREEN_HEIGHT:
                numNeighbors += int(currBoard[x+i + (y+j)*SCREEN_HEIGHT].aliveStatus)

    if currPixel.aliveStatus and numNeighbors < 2:
        aliveNextFrame = False;
    elif currPixel.aliveStatus and numNeighbors == 2 or numNeighbors == 3:
        aliveNextFrame = True;
    elif currPixel.aliveStatus and numNeighbors > 3:
        aliveNextFrame = False;
    elif not currPixel.aliveStatus and numNeighbors == 3:
        aliveNextFrame = True;
        
    return aliveNextFrame

def ageToColor(age):
    if age == 0:
        return (255, 0 , 0)
    elif age == 1:
        return (255, 127, 0)
    elif age == 2:
        return (255, 255, 0)
    elif age == 3:
        return (0, 255, 0)
    elif age == 4:
        return (0, 0, 255)
    elif age == 5:
        return (75, 0, 130)
    return (148, 0, 211)

pixelStatus = [pixel(False, 0) for _ in range(SCREEN_WIDTH*SCREEN_HEIGHT)]

paused = False
frameCounter = 0
while currRunning:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            currRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused;
        if event.type == pygame.MOUSEBUTTONUP:
            clickPos = pygame.mouse.get_pos()
            print(clickPos)
            clickedIndex = (clickPos[0]//4)+SCREEN_HEIGHT*(clickPos[1]//4)
            pixelStatus[clickedIndex].aliveStatus = True 
            pygame.draw.rect(screenDisplay, (255, 255, 255), pygame.Rect((clickPos[0]//4)*SCALE, (clickPos[1]//4)*SCALE, SCALE, SCALE))
            pygame.display.update()

    if not paused and (frameCounter*UPDATES_PER_SEC)%FPS == 0:
        screenDisplay.fill((0, 0, 0))
        
        for pixelNum in range(len(pixelStatus)):
            currPixel = pixelStatus[pixelNum]
            currPixelX = pixelNum % SCREEN_WIDTH
            currPixelY = pixelNum // SCREEN_HEIGHT

            if currPixel.aliveStatus:
                pygame.draw.rect(screenDisplay, ageToColor(currPixel.age), pygame.Rect(currPixelX*SCALE, currPixelY*SCALE, SCALE, SCALE))
        pixelStatus = updateBoard(pixelStatus)
    frameCounter = (frameCounter + 1) % FPS
    pygame.display.update()
pygame.quit()