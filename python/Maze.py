# On importe les librairies

import pygame
import csv
from pygame.locals import *
import mazeGen
import time

# On initialise pygame et la police d'écriture

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 24)

# On initialise les listes

mazes, listreplay, mazes, texts = [[]] * 4

# On initialise les fichiers images

wall = pygame.image.load("mur.png")
empty = pygame.image.load("empty.png")
player = pygame.image.load("start.png")
end = pygame.image.load("end.png")

# On initialise les variables booléennes

finish = False
play = False
replay = False
chooseDifficult = False

blockR = False
running = True

t0once = True
t1once = True
saveonce = True
regenonce = True

# Autres variables

playerloc = None
delay = 0

# Fonction qui transforme un labyrinthe en une chaine de caractère pour le sauvegarder

def maze_to_string(maze):
    stringfin = []
    for i in maze:
        string = ''.join([str(x) for x in i])
        stringfin.append(string)
    return stringfin


# On définit la taille de l'écran

def update_size_screen(x, y):
    global liste, xWindow, yWindow, window, mazebase
    liste = mazeGen.generate_labyrinthe(x,y)
    xWindow = x*20+10
    yWindow = y*20+10
    window = pygame.display.set_mode( (xWindow, yWindow) )
    mazebase = maze_to_string(liste)

update_size_screen(25,25)

# Fonction qui transforme les labyrinthes compactés en labyrinthe pouvant être utilisé par le programme

def string_to_maze(string):
    mazefin = []
    maze = []
    for i in string:
        if i in ['0','1','2','3']:
            maze.append(int(i))
        if i == ',':
            mazefin.append(maze)
            maze = []
    mazefin.append(maze)
    return mazefin

# Fonction qui sauvegarde le labyrinthe compacté dans le fichier 'save.csv'

def save_maze(maze, score):
    date = time.asctime()
    db = open('save.csv', 'a')
    newrow = str(maze) + ';' + str(date) + ';' + str(score) + ';' + str(((xWindow-10)/20,(yWindow-10)/20)) + '\n'
    db.write(newrow)
    db.close()

# Fonction qui affiche les sauvegardes précédentes sous formes de boutons (pour rejouer)

def draw_csv():
    global listreplay, buttonPlay, buttonReplay
    listreplay.clear()
    with open('save.csv') as save:
        saveread = csv.reader(save, delimiter=';')
        i=0
        for row in saveread:
            rect = pygame.Rect(25, (60 * i), 460, 50)
            text = font.render( str(row[1])+'     '+str(row[2]), 1, (255,255,255) )
            pygame.draw.rect(window, [128, 128, 0], rect)
            window.blit(text, (50, (60 * i)))
            listreplay.append([row[0],row[3],rect])
            i+=1
    buttonPlay, buttonReplay = [None] * 2



# Fonction pour se déplacer en haut

def move_up():
    global liste
    global finish
    if y-1 >= 0:                        #On vérifie si la futur position existe
        if liste[y-1][x] == 1:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 1
            liste[y-1][x] = 2
        elif liste[y-1][x] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True

# Fonction pour se déplacer en bas

def move_down():
    global liste
    global finish
    if y+1 < (yWindow / 10):            #On vérifie si la futur position existe
        if liste[y+1][x] == 1:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 1
            liste[y+1][x] = 2
        elif liste[y+1][x] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True

# Fonction pour se déplacer à droite

def move_right():
    global liste
    global finish
    if x+1 < (xWindow / 10):            #On vérifie si la futur position existe
        if liste[y][x+1] == 1:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 1
            liste[y][x+1] = 2
        elif liste[y][x+1] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True

# Fonction pour se déplacer à gauche

def move_left():
    global liste
    global finish
    if x-1 >= 0:                        #On vérifie si la futur position existe
        if liste[y][x-1] == 1:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 1
            liste[y][x-1] = 2
        elif liste[y][x-1] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True



# On lance une boucle qui modifiera l'affichage pygame

while running:


    # On définit le taux de rafraichissement de l'affichage sur 60 Hz et on remplit le fond d'une couleur blanche
    clock.tick(60)
    window.fill((255,255,255))

    # De base, on se trouve sur le menu avec deux choix : Jouer un nouveau niveau ou rejouer un ancien pour battre son score

    if play == False and replay == False:
        buttonPlay = pygame.Rect((xWindow/2-125), (yWindow/2-125), 250, 50)
        buttonReplay = pygame.Rect((xWindow/2-125), (yWindow/2-25), 250, 50)

        buttonEasy, buttonNormal, buttonNormal = [None] * 3

        pygame.draw.rect(window, [255, 0, 0], buttonPlay)
        playtxt = font.render('Play',1,(255,255,255))
        window.blit(playtxt, (230,130) )

        pygame.draw.rect(window, [255, 0, 0], buttonReplay)
        replaytxt = font.render('Replay',1,(255,255,255))
        window.blit(replaytxt, (215,230) )

    # Menu pour choisir la difficulté (Facile, Moyen, Difficile)

    if chooseDifficult == True:
        buttonEasy = pygame.Rect((xWindow/2-125), (yWindow/2-125), 250, 50)
        buttonNormal = pygame.Rect((xWindow/2-125), (yWindow/2-25), 250, 50)
        buttonHard = pygame.Rect((xWindow/2-125), (yWindow/2+75), 250, 50)

        buttonPlay, buttonReplay = [None] * 2

        pygame.draw.rect(window, [255, 0, 0], buttonEasy)
        easytxt = font.render('Easy',1,(255,255,255))
        window.blit(easytxt, (230,130) )

        pygame.draw.rect(window, [255, 0, 0], buttonNormal)
        normaltxt = font.render('Normal',1,(255,255,255))
        window.blit(normaltxt, (215,230) )

        pygame.draw.rect(window, [255, 0, 0], buttonHard)
        hardtxt = font.render('Hard',1,(255,255,255))
        window.blit(hardtxt, (230,330) )


    # Si on choisit de jouer

    if play == True:                            # On lance le timer
        if t0once == True:
            t0 = time.monotonic()
            t0once = False

        for y in range(len(liste)):             # On actualise l'affichage du labyrinthe
            for x in range(len(liste[y])):
                if liste[y][x] == 2:
                    playerloc = (x, y)
                    e = player
                elif liste[y][x] == 3:
                    e = end
                elif liste[y][x] == 0:
                    e = wall
                elif liste[y][x] == 1:
                    e = empty
                window.blit( e, (x*10,y*10) )

    # Fonction pour génerer un nouveau labyrinthe en maintenant la touche R

    if blockR == False:
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            delay += 1/60
            if delay > 1.5:
                if regenonce == True:
                    liste = mazeGen.generate_labyrinthe(xMax,yMax)
                    mazebase = maze_to_string(liste)
                    regenonce = False
                regenonce = True
                delay = 0

        if not keys[K_r]:
            delay = 0

    if replay == True:
        draw_csv()

    # Si on a finit le niveau

    if finish == True:                    # On arrête le timer
        if t1once == True:
            t1 = time.monotonic()
            t1once = False

        t = int(t1 - t0)

        if saveonce == True:              # On sauvegarde le labyrinthe ( avec la fonction save_maze() )
            save_maze(mazebase, t)
            saveonce = False

        window.fill(0)                                                          # On efface l'affichage sur l'écran
        play, replay, finish, chooseDifficult = [False] * 4                     # On remet les variables à faux
        update_size_screen(25,25)                                               # On remet la taille de l'écran à la normale


    pygame.display.flip()                       # On affiche les textures mis en mémoire

    # Ici, on gère les touches pressées

    for event in pygame.event.get():
        if playerloc is not None:
            (x, y) = playerloc

        if event.type == QUIT or(event.type == KEYUP and event.key == K_ESCAPE):    # On arrête pygame avec la touce echap
           running = False

        if event.type == KEYDOWN:                         # On déplace le joueur avec les touches directionnels
            if playerloc is not None:
                if event.key == K_UP:
                    move_up()

                if event.key == K_DOWN:
                    move_down()

                if event.key == K_RIGHT:
                    move_right()

                if event.key == K_LEFT:
                    move_left()

            if event.key == K_b:
                play, replay, chooseDifficult, finish = [False] * 4
                update_size_screen(25,25)


        if event.type == pygame.MOUSEBUTTONDOWN:                                    # On gère les actions avec la souris

            mouse_pos = pygame.mouse.get_pos()                                      # On récupère la position de la souris

            if chooseDifficult == True:
                if buttonEasy.collidepoint(mouse_pos):
                    update_size_screen(10,10)
                    play = True

                if buttonNormal.collidepoint(mouse_pos):
                    update_size_screen(25,25)
                    play = True

                if buttonHard.collidepoint(mouse_pos):
                    update_size_screen(60,30)
                    play = True

            elif replay == True:                                                    # Si on est dans le menu replay on vérifie sur quel bouton se situe la souris pour génerer le labyrinthe correspondant
                for i in range(1,len(listreplay)):
                    button = listreplay[i][2]
                    if button.collidepoint(mouse_pos):
                        size = listreplay[i][1]
                        size = size.split(',')
                        x, y = int(float(size[0].replace('(',''))), int(float(size[1].replace(')','')))
                        update_size_screen(x, y)
                        mazebase = listreplay[i][0]
                        liste = string_to_maze(mazebase)
                        play = True
                        replay = False
                        blockR = True

            if buttonPlay is not None:

                if buttonPlay.collidepoint(mouse_pos) and chooseDifficult == False:              # Si on est dans le menu et qu'on clique sur le bouton play on met la variable play à Vrai
                    chooseDifficult = True
                    blockR = False

                if buttonReplay.collidepoint(mouse_pos) and replay == False:            # Si on est dans le menu et qu'on clique sur le bouton replay on met la variable replay à Vrai
                    replay = True


# Quand on quitte la boucle on éteint pygame

pygame.quit()

