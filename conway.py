import pygame
import random
import copy

SCREEN_HEIGHT = 100 # game world height
SCREEN_WIDTH = 100 # game world width
SCALE = 4 # scale graphics of game world up by some amount
UPDATES_PER_SEC = 3 # number of times to update game world per second
FPS = 60 

# pygame setup process
pygame.init()
screenDisplay = pygame.display.set_mode((SCREEN_WIDTH*SCALE, SCREEN_HEIGHT*SCALE))
pygame.display.set_caption('conways game of life')
clock = pygame.time.Clock()
currRunning = True

# individual 'living' pixel
class pixel:
    def __init__(self, isAlive, age):
        self.isAlive= isAlive
        self.age = age
    
    def invertStatus(self):
        self.isAlive = not self.isAlive;


# returns the board next frame corresponding with the current board
def updateBoard(currBoard):
    nextBoard = copy.deepcopy(currBoard)
    for i in range(len(currBoard)):
        currPixel = currBoard[i]
        currPixelX = i % SCREEN_WIDTH
        currPixelY = i // SCREEN_HEIGHT
        currPixelStatus = pixelNextFrame(currPixelX, currPixelY, currBoard)
        if currPixel.isAlive and currPixelStatus:
            nextBoard[i].age += 1
        elif currPixel.isAlive and (not currPixelStatus):
            nextBoard[i].age == 0
        nextBoard[i].isAlive = currPixelStatus

    return nextBoard


# returns the status of current pixel at position x,y for the next frame 
def pixelNextFrame(x, y, currBoard):
    currPixel = currBoard[x + y*SCREEN_HEIGHT]
    aliveNextFrame = currPixel.isAlive
    numNeighbors = 0

    # checks all possible combinations x+-1, y+-1 around the current pixel
    for i in range(-1, 2):
        for j in range(-1, 2):
            #checks for any extremes
            if abs(i) + abs(j) != 0 and 0 <= x+i and x+i < SCREEN_WIDTH and 0 <= y+j and y+j < SCREEN_HEIGHT:
                numNeighbors += int(currBoard[x+i + (y+j)*SCREEN_HEIGHT].isAlive)

    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    if currPixel.isAlive and numNeighbors < 2:
        aliveNextFrame = False;

    # Any live cell with two or three live neighbours lives on to the next generation.
    elif currPixel.isAlive and (numNeighbors == 2 or numNeighbors == 3):
        aliveNextFrame = True;
    
    # Any live cell with more than three live neighbours dies, as if by overpopulation.
    elif currPixel.isAlive and numNeighbors > 3:
        aliveNextFrame = False;

    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
    elif (not currPixel.isAlive) and numNeighbors == 3:
        aliveNextFrame = True;
        
    return aliveNextFrame

# returns the color to make a pixel corresponding with the pixel age
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


# stores the current status of every pixel
pixels = [pixel(random.randint(0,1), 0) for _ in range(SCREEN_WIDTH*SCREEN_HEIGHT)]

paused = False

frameCounter = 0 # counts to determine when to update screen

# main game loop
while currRunning:
    clock.tick(FPS) # sets game fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # user quits
            currRunning = False

        if event.type == pygame.KEYDOWN: # users presses 'p', AKA pauses
            if event.key == pygame.K_p:
                paused = not paused;

        if event.type == pygame.MOUSEBUTTONUP: # user clicks somewhere
            clickPos = pygame.mouse.get_pos() # gets current mouse position
            clickedIndex = (clickPos[0]//4)+SCREEN_HEIGHT*(clickPos[1]//4) 
            pixels[clickedIndex].isAlive = True # sets clicked pixel to be alive

            # lines below draw a white rectangle to indicate that something happened and updated display
            pygame.draw.rect(screenDisplay, (255, 255, 255), pygame.Rect((clickPos[0]//4)*SCALE, (clickPos[1]//4)*SCALE, SCALE, SCALE))
            pygame.display.update()


    if not paused and (frameCounter*UPDATES_PER_SEC)%FPS == 0:
        screenDisplay.fill((0, 0, 0)) # erases screen
        
        for pixelNum in range(len(pixels)): 
            currPixel = pixels[pixelNum]
            currPixelX = pixelNum % SCREEN_WIDTH
            currPixelY = pixelNum // SCREEN_HEIGHT

            if currPixel.isAlive: 
                pygame.draw.rect(screenDisplay, ageToColor(currPixel.age), pygame.Rect(currPixelX*SCALE, currPixelY*SCALE, SCALE, SCALE))
        pixels = updateBoard(pixels)
    frameCounter = (frameCounter + 1) % FPS
    pygame.display.update()
pygame.quit()