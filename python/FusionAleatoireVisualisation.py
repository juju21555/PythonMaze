import pygame
from pygame.locals import *
import random

# Fusion aléatoire

pygame.init()
clock = pygame.time.Clock()

xMax = 25
yMax = 25

directionX = {'N':0,'S':0,'E':1,'O':-1}
directionY = {'N':1,'S':-1,'E':0,'O':0}
colors = []

running = True
endalgo = False
space = False

regenonce = True
delay = 0

def update_size_screen(x, y, maze = None):
    global xWindow, yWindow, window, labyrinthe, murs, randCell, lastCell
    xWindow = x*20+10
    yWindow = y*20+10
    window = pygame.display.set_mode( (xWindow, yWindow) )
    labyrinthe = [[(x+xMax*y) for x in range(xMax)] for y in range(yMax)]

    murs = [[0 for x in range(2*xMax+1)] for y in range(2*yMax+1)]
    for y in range(len(murs)-1):
        for x in range(len(murs[y])-1):
            if x % 2 != 0 and y % 2 != 0:
                murs[y][x] = 1


    randCell = ((random.randrange(xMax)), (random.randrange(yMax)))
    lastCell = [randCell]

def breakWall(x1,y1,x2,y2):
    milieu = [ x1+x2+1, y1+y2+1 ]
    murs[milieu[1]][milieu[0]] = 1

def genColor(idx):
    idxMax = xMax*yMax-1
    intColor = int((idx*(256**3-1))/idxMax)
    blue =  intColor & 255
    green = (intColor >> 8) & 255
    red =   (intColor >> 16) & 255
    rgbColor = red, green, blue

    return rgbColor

update_size_screen(xMax,yMax)


while running:

    # On définit le taux de rafraichissement de l'affichage sur 60 Hz et on remplit le fond d'une couleur blanche
    clock.tick(60)
    window.fill((255,255,255))

    keys = pygame.key.get_pressed()
    if keys[K_r]:
        delay += 1/60
        if delay > 1.5:
            if regenonce == True:
                update_size_screen(xMax,yMax)
                regenonce = False
                endalgo = False
            regenonce = True
            delay = 0

    if not keys[K_r]:
        delay = 0

    for y in range(len(murs)):             # On actualise l'affichage du labyrinthe
        for x in range(len(murs[y])):
            if murs[y][x] == 0:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (0,0,0), rect)

            elif murs[y][x] == 1:
                idx = labyrinthe[int((y-1)/2)][int((x-1)/2)]
                color = genColor(idx)
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, color, rect)
                e = None

    if keys[K_RIGHT] or space:

        if endalgo == False:

            openedWall = 0

            if openedWall < xMax*yMax-1:
                (rx, ry) = ((random.randrange(xMax)), (random.randrange(yMax)))
                direction = random.choice(['N','S','O','E'])
                nx = rx + directionX[direction]
                ny = ry + directionY[direction]
                if nx >= 0 and nx < xMax and ny >= 0 and ny < yMax:

                    if labyrinthe[ny][nx] != labyrinthe[ry][rx]:

                        breakWall(rx, ry, nx, ny)
                        var = labyrinthe[ny][nx]
                        for y in range(yMax):
                            for x in range(xMax):
                                if labyrinthe[y][x] == var:
                                    labyrinthe[y][x] = labyrinthe[ry][rx]
                        rx, ry = nx, ny
                        openedWall += 1
            else:
                endalgo = True




    pygame.display.flip()                       # On affiche les textures mis en mémoire

    for event in pygame.event.get():

       if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
           running = False

       if event.type == KEYDOWN and event.key == K_SPACE:
        if space == False:
            space = True
        else:
            space = False

pygame.quit()