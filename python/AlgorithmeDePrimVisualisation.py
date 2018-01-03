import pygame
from pygame.locals import *
import random

# Algorithme de Prim

pygame.init()
clock = pygame.time.Clock()

xMax = 25
yMax = 25

dx = {'N':0,'S':0,'E':2,'O':-2}
dy = {'N':2,'S':-2,'E':0,'O':0}

running = True
endalgo = False
space = False

regenonce = True
delay = 0

def update_size_screen(x, y, maze = None):
    global xWindow, yWindow, window, murs, listCell, rcx, rcy, rx, ry
    xWindow = x*20+10
    yWindow = y*20+10
    window = pygame.display.set_mode( (xWindow, yWindow) )

    listCell = []

    murs = [[0 for x in range(2*xMax+1)] for y in range(2*yMax+1)]

    (rx, ry) = ((2*random.randrange(xMax)+1), (2*random.randrange(yMax)+1))
    murs[ry][rx] = 2

    for d in ['N','S','O','E']:
        nx = rx + dx[d]
        ny = ry + dy[d]
        if nx >= 0 and nx < 2*xMax+1 and ny >= 0 and ny < 2*yMax+1:
            murs[ny][nx] = 1
            listCell.append((nx, ny))

    (rcx, rcy) = (rx, ry)

def breakWall(x1,y1,x2,y2):
    milieu = [ int((x1+x2) /2), int((y1+y2) /2) ]
    murs[milieu[1]][milieu[0]] = 2

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

    for y in range(len(murs)):             # On actualise l'affichage du murs
        for x in range(len(murs[y])):
            if murs[y][x] == 0:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (0,0,0), rect)

            elif murs[y][x] == 2:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (255,255,255), rect)

            elif murs[y][x] == 1:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (128,0,128), rect)

    rect = pygame.Rect(rcx*10, rcy*10, 10, 10)
    pygame.draw.rect(window, (255,0,0), rect)


    if keys[K_RIGHT] or space:
        if endalgo == False:
            if listCell != []:
                (rx, ry) = random.choice(listCell)
                listCell.remove((rx, ry))
                murs[ry][rx] = 2
                voisinsVisite = []
                for d in ['N','S','O','E']:
                    nx, ny = rx + dx[d], ry + dy[d]
                    if nx >= 0 and nx < 2*xMax+1 and ny >= 0 and ny < 2*yMax+1 and murs[ny][nx] == 2:
                        voisinsVisite.append((nx, ny))

                for d in ['N','S','O','E']:
                    nx, ny = rx + dx[d], ry + dy[d]
                    if nx >= 0 and nx < 2*xMax+1 and ny >= 0 and ny < 2*yMax+1 and murs[ny][nx] == 0:
                        murs[ny][nx] = 1
                        listCell.append((nx, ny))

                if len(voisinsVisite) > 0:
                    (nx, ny) = random.choice(voisinsVisite)
                    breakWall(nx,ny,rx,ry)
                    murs[ny][nx] = 2


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