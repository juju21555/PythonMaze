import pygame
from pygame.locals import *
import ExplorationExhaustive
import FusionAleatoire
import AlgorithmeDePrim
import random
import time

pygame.init()
clock = pygame.time.Clock()

gen = 2

directionX = {'N':0,'S':0,'E':1,'O':-1}
directionY = {'N':1,'S':-1,'E':0,'O':0}

running = True
endalgo = False

regenonce = True
delay = 0

def update_size_screen(x, y, maze = None):
    global liste, xWindow, yWindow, window, mazebase
    if gen == 0:
        liste = FusionAleatoire.generate_labyrinthe(x,y)
    elif gen == 1:
        liste = ExplorationExhaustive.generate_labyrinthe(x,y)
    elif gen == 2:
        liste = AlgorithmeDePrim.generate_labyrinthe(x,y)
    xWindow = x*20+10
    yWindow = y*20+10
    window = pygame.display.set_mode( (xWindow, yWindow) )

update_size_screen(25,25)


while running:

    # On définit le taux de rafraichissement de l'affichage sur 60 Hz et on remplit le fond d'une couleur blanche
    clock.tick(60)
    window.fill((255,255,255))

    keys = pygame.key.get_pressed()
    if keys[K_r]:
        delay += 1/60
        if delay > 1.5:
            if regenonce == True:
                update_size_screen(25,25)
                regenonce = False
                endalgo = False
                time.sleep(0.1)
            regenonce = True
            delay = 0

    if not keys[K_r]:
        delay = 0

    if keys[K_KP0]:
        gen = 0

    if keys[K_KP1]:
        gen = 1

    if keys[K_KP2]:
        gen = 2

    for y in range(len(liste)):             # On actualise l'affichage du labyrinthe
        for x in range(len(liste[y])):
            if liste[y][x] == 2:
                playerloc = (x, y)
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (0,128,0), rect)

            elif liste[y][x] == 3:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (255,0,0), rect)

            elif liste[y][x] == 0:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (0,0,0), rect)

            elif liste[y][x] == 1:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (255,255,255), rect)

            elif liste[y][x] == 4:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (128,0,128), rect)

            elif liste[y][x] == 5:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (255,255,0), rect)




    if endalgo == False:

        (px, py) = playerloc
        voisins = []

        if liste[py][px] != 3:                                                  # Tant que l'on ne trouve pas la case de fin on continue
            for directions in ['N','S','O','E']:                                # A chaque etape, on verifie les cases alentours
                nx = px + directionX[directions]
                ny = py + directionY[directions]
                if nx >= 0 and nx < xWindow/10 and ny >= 0 and ny < yWindow/10:
                    if liste[ny][nx] == 1:                                      # Si une n'a jamais été visité et est vide (1) on l'ajoute en tant que case possible
                        voisins.append((nx, ny))
                    if liste[ny][nx] == 3:                                      # Si une case est la case de fin on termine l'algorithme
                        endalgo = True
                        break


            if len(voisins) > 0:                                                # Si on a au moins une case jamais visité et vide on se déplace dessus (ou on tire au hasard)
                (nx, ny) = random.choice(voisins)
                liste[py][px] = 4
                liste[ny][nx] = 2


            else:                                                               # Sinon on recule d'une case et on définit la case précédente comme deja visité mais vide (5)
                for directions in ['N','S','O','E']:
                    nx = px + directionX[directions]
                    ny = py + directionY[directions]
                    if nx >= 0 and nx < xWindow/10 and ny >= 0 and ny < yWindow/10:
                        if liste[ny][nx] == 4:
                            liste[py][px] = 5
                            liste[ny][nx] = 2




    pygame.display.flip()                       # On affiche les textures mis en mémoire

    for event in pygame.event.get():

       if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):

           running = False

pygame.quit()
