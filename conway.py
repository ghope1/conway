import pygame
SCREEN_HEIGHT = 100;
SCREEN_WIDTH = 100;
SCALE = 4;
# pygame setup process
pygame.init()
screenDisplay = pygame.display.set_mode((SCREEN_WIDTH*SCALE, SCREEN_HEIGHT*SCALE))
clock = pygame.time.Clock()
currRunning = True

class pixel:
    def __init__(self, aliveStatus, age):
        self.alive = aliveStatus
        self.age = age
    
    def invertStatus(self):
        self.aliveStatus = not self.aliveStatus;


screenStatus = [pixel(False, 0) for _ in range(SCREEN_WIDTH*SCREEN_HEIGHT)]
print(screenStatus)

paused = False;

while currRunning:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            currRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused;
                print("pause")

    if not paused:

        screenDisplay.fill((255, 255, 255))
    else:
        screenDisplay.fill((0,0,0))

    pygame.display.update()
pygame.quit()