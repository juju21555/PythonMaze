import pygame
from pygame.locals import *
from algorithmeGeneration import ExplorationExhaustive
from algorithmeGeneration import FusionAleatoire
from algorithmeGeneration import AlgorithmeDePrim
from algorithmeGeneration import LabyrintheEntrelacee
import random
import time

pygame.init()
clock = pygame.time.Clock()

gen = 3

directionX = {'N':0,'S':0,'E':1,'O':-1}
directionY = {'N':-1,'S':1,'E':0,'O':0}

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

    elif gen == 3:
        liste = LabyrintheEntrelacee.generate_labyrinthe(x,y)

    xWindow = x*20+10
    yWindow = y*20+10
    window = pygame.display.set_mode( (xWindow, yWindow) )

update_size_screen(25,25)

# Fonction pour se déplacer en haut

def move_up(x,y):
    global liste
    global finish
    if y-1 >= 0:
        if liste[y-1][x] in [1,4]:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 4
            liste[y-1][x] = 2
            playerloc.append((x,y-1))
        elif liste[y-1][x] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True
        elif liste[y-1][x] in [4,6]:
            liste[y][x] = 4
            liste[y-4][x] = 2
            playerloc.append((x,y-4))

# Fonction pour se déplacer en bas

def move_down(x,y):
    global liste
    global finish
    if y+1 < yWindow / 10:
        if liste[y+1][x] in [1,4]:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 4
            liste[y+1][x] = 2
            playerloc.append((x,y+1))
        elif liste[y+1][x] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True
        elif liste[y+1][x] in [4,5]:
            liste[y][x] = 4
            liste[y+4][x] = 2
            playerloc.append((x,y+4))

# Fonction pour se déplacer à droite

def move_right(x,y):
    global liste
    global finish
    if x+1 < xWindow / 10:
        if liste[y][x+1] in [1,4]:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 4
            liste[y][x+1] = 2
            playerloc.append((x+1,y))
        elif liste[y][x+1] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True
        elif liste[y][x+1] in [4,7]:
            liste[y][x] = 4
            liste[y][x+4] = 2
            playerloc.append((x+4,y))

# Fonction pour se déplacer à gauche

def move_left(x,y):
    global liste
    global finish
    if x-1 >= 0:
        if liste[y][x-1] in [1,4]:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 4
            liste[y][x-1] = 2
            playerloc.append((x-1,y))
        elif liste[y][x-1] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True
        elif liste[y][x-1] in [4,8]:
            liste[y][x] = 4
            liste[y][x-4] = 2
            playerloc.append((x-4,y))

doonce = True

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
                doonce = True
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
                if doonce == True:
                    playerloc = [(x, y)]
                    doonce = False
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

            elif liste[y][x] == 9:
                rect = pygame.Rect(x*10, y*10, 10, 10)
                pygame.draw.rect(window, (255,255,0), rect)

            elif liste[y][x] == 5:
                rect = pygame.Rect(x*10, y*10+8, 10, 2)
                pygame.draw.rect(window, (0,0,0), rect)

            elif liste[y][x] == 6:
                rect = pygame.Rect(x*10, y*10, 10, 2)
                pygame.draw.rect(window, (0,0,0), rect)

            elif liste[y][x] == 7:
                rect = pygame.Rect(x*10+8, y*10, 2, 10)
                pygame.draw.rect(window, (0,0,0), rect)

            elif liste[y][x] == 8:
                rect = pygame.Rect(x*10, y*10, 2, 10)
                pygame.draw.rect(window, (0,0,0), rect)

    if endalgo == False:

        if playerloc != []:                                                  # Tant que l'on ne trouve pas la case de fin on continue
            (px, py) = playerloc[-1]
            voisins = []                                                 # Tant que l'on ne trouve pas la case de fin on continue
            for directions in ['N','S','O','E']:                                # A chaque etape, on verifie les cases alentours
                nx = px + directionX[directions]
                ny = py + directionY[directions]
                if nx >= 0 and nx < xWindow/10 and ny >= 0 and ny < yWindow/10:
                    if liste[ny][nx] == 1:                                      # Si une n'a jamais été visité et est vide (1) on l'ajoute en tant que case possible
                        voisins.append(directions)

                    if liste[ny][nx] == 3:                                      # Si une case est la case de fin on termine l'algorithme
                        endalgo = True
                        break

                    else:
                        ax = px + 3*directionX[directions]
                        ay = py + 3*directionY[directions]
                        bx = px + 4*directionX[directions]
                        by = py + 4*directionY[directions]
                        if ax >= 0 and ax < xWindow/10 and ay >= 0 and ay < yWindow/10:
                            if liste[ny][nx] in [5,6,7,8] and liste[ay][ax] in [5,6,7,8] and liste[by][bx] == 1:
                                voisins.append(directions)


            if len(voisins) > 0:                                                # Si on a au moins une case jamais visité et vide on se déplace dessus (ou on tire au hasard)
                d = random.choice(voisins)
                if d == 'N':
                    move_up(px, py)
                elif d == 'S':
                    move_down(px, py)
                elif d == 'O':
                    move_left(px, py)
                elif d == 'E':
                    move_right(px, py)

            else:                                                               # Sinon on recule d'une case et on définit la case précédente comme deja visité mais vide (5)
                (tx, ty) = playerloc.pop()
                liste[ty][tx] = 9




    pygame.display.flip()                       # On affiche les textures mis en mémoire

    for event in pygame.event.get():

       if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):

           running = False

pygame.quit()
