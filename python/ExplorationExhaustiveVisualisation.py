import pygame
from pygame.locals import *
import random

# Exploration exhaustive

pygame.init()
clock = pygame.time.Clock()

xMax = 25
yMax = 25

directionX = {'N':0,'S':0,'E':1,'O':-1}
directionY = {'N':1,'S':-1,'E':0,'O':0}

running = True
endalgo = False
space = False

regenonce = True
delay = 0

def update_size_screen(x, y, maze = None):
    global xWindow, yWindow, window, labyrinthe, murs, lastCell, randCell
    xWindow = x*20+10
    yWindow = y*20+10
    window = pygame.display.set_mode( (xWindow, yWindow) )

    labyrinthe = [[0 for x in range(xMax)] for y in range(yMax)]

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

def speWall(x1,y1,x2,y2):
    milieu = [ x1+x2+1, y1+y2+1 ]
    murs[milieu[1]][milieu[0]] = 4

update_size_screen(xMax,yMax)



while running:

    # On définit le taux de rafraichissement de l'affichage sur 60 Hz et on remplit le fond d'une couleur blanche
    clock.tick(60)
    window.fill((255,255,255))

    (rcx, rcy) = randCell
    rcx, rcy = 2*rcx+1, 2*rcy+1

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
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (255,255,255), rect)

            elif murs[y][x] == 4:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (128,0,128), rect)

    rect = pygame.Rect(rcx*10, rcy*10, 10, 10)
    pygame.draw.rect(window, (255,0,0), rect)


    if keys[K_RIGHT] or space:
        if endalgo == False:

            if lastCell != []:
                (rx, ry) = lastCell[-1]
                labyrinthe[ry][rx] = 1
                lVoisins = []
                for direction in ['N','S','O','E']:
                    nx = rx + directionX[direction]
                    ny = ry + directionY[direction]
                    if nx >= 0 and nx < xMax and ny >= 0 and ny < yMax:

                        if labyrinthe[ny][nx] == 0:

                            lVoisins.append(direction)


                if len(lVoisins) > 0:
                    var = random.choice(lVoisins)
                    breakWall(rx, ry, (rx+directionX[var]), (ry+directionY[var]))
                    rx, ry = rx + directionX[var], ry + directionY[var]
                    lastCell.append((rx, ry))
                else:
                    (px, py) = lastCell[-1]
                    if len(lastCell) > 1:
                        (bx, by) = lastCell[-2]
                        speWall(bx,by,px,py)
                    px, py = 2*px+1, 2*py+1
                    murs[py][px] = 4
                    lastCell.pop()
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