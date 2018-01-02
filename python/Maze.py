# On importe les librairies

import pygame
import csv
from pygame.locals import *
import mazeGen
import mazeGen2
import time

# On initialise pygame et la police d'écriture

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 24)
font1 = pygame.font.SysFont('Comic Sans MS', 18)

# On initialise les listes

mazes, listreplay, mazes, texts = [[]] * 4

# On initialise les variables booléennes

finish, play, replay, settings, blockR, tracer = [False] * 6
t0once, t1once, saveonce, regenonce, running = [True] * 5

# Autres variables

playerloc = None
delay = 0
nametxt = ''
genTexts = ['Fusion aléatoire','Exploration exhaustive']
genText = 'Exploration exhaustive'
gen = 1
difficultTexts = ['Easy','Normal','Hard']
difficultText = 'Normal'
difficult = 1
sizeDiff = [(10,10),(25,25),(60,30)]
xDiff, yDiff = 25,25
colorTrB = (255, 0, 0)

# Fonction qui transforme un labyrinthe en une chaine de caractère pour le sauvegarder

def maze_to_string(maze):
    stringfin = []
    for i in maze:
        string = ''.join([str(x) for x in i])
        stringfin.append(string)
    return stringfin


# On définit la taille de l'écran

def update_size_screen(x, y, maze = None):
    global liste, xWindow, yWindow, window, mazebase
    if gen == 0:
        liste = mazeGen2.generate_labyrinthe(x,y)
    elif gen == 1:
        liste = mazeGen.generate_labyrinthe(x,y)
    xWindow = x*20+10
    yWindow = y*20+10
    window = pygame.display.set_mode( (xWindow, yWindow) )
    if maze is not None:
        mazebase = maze
    else:
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
    array = []
    date = time.asctime()
    with open('save.csv') as csvfile:
        fieldnames = ['maze','date','highscore','size','nickname','essais']
        reader = csv.DictReader(csvfile, delimiter=';')
        newrow = {'maze':str(maze), 'date':str(date), 'highscore':str(score)+'s', 'size':str(((xWindow-10)/20,(yWindow-10)/20)),'nickname':str(nametxt),'essais':'1'}
        for row in reader:
            if row['maze'] == 'maze':
                continue
            if row['maze'] == str(maze):
                row['date'] = str(date)
                row['highscore'] = str(score)+'s'
                row['essais'] = str(int(row['essais']) + 1)
                newrow = None
            array.append(row)
        if newrow is not None:
            array.append(newrow)
    with open('save.csv','w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in array:
            writer.writerow(row)
    csvfile.close()


# Fonction qui affiche les sauvegardes précédentes sous formes de boutons (pour rejouer)

def draw_csv():
    global listreplay, buttonPlay, buttonReplay
    listreplay.clear()
    with open('save.csv') as save:
        saveread = csv.reader(save, delimiter=';')
        r = []
        i=0

        for row in saveread:
            if row != [] and row[0] != 'maze':
                r.append(row)

        r.append(['maze', 'date', 'highscore', 'size', 'nickname', 'essais'])
        reader = r.reverse()

        for row in r:
            rect = pygame.Rect(25, (60 * i), 460, 50)
            pygame.draw.rect(window, [128, 128, 0], rect)

            textdate = font1.render( str(row[1]), 1, (255,255,255) )
            textscore = font1.render( str(row[2]), 1, (255,255,255) )
            textname = font1.render( str(row[4]), 1, (255,255,255) )
            textessais = font1.render( str(row[5]), 1, (255,255,255) )

            window.blit(textdate, (35, (60 * i)))
            window.blit(textscore, (260, (60 * i)))
            window.blit(textname, (350, (60 * i)))
            window.blit(textessais, (430, (60 * i)+20))

            listreplay.append([row[0],row[3],rect])
            i+=1

    buttonPlay, buttonReplay = [None] * 2

# Fonction qui définit la difficulté du jeu

def set_difficult(i):
    global difficultText, difficult, xDiff, yDiff
    if difficult == len(difficultTexts)-1 and i == 1:
        difficult = 0
        difficultText = difficultTexts[difficult]

    elif difficult == 0 and i == -1:
        difficult = len(difficultTexts)-1
        difficultText = difficultTexts[difficult]

    else:
        difficult += i
        difficultText = difficultTexts[difficult]

    (xDiff, yDiff) = sizeDiff[difficult]

# Fonction qui définit le type de génération du labyrinthe

def set_gen(i):
    global genText, gen
    if gen == len(genTexts)-1 and i == 1:
        gen = 0
        genText = genTexts[gen]

    elif gen == 0 and i == -1:
        gen = len(genTexts)-1
        genText = genTexts[gen]

    else:
        gen += i
        genText = genTexts[gen]


# Fonction pour se déplacer en haut

def move_up():
    global liste
    global finish
    if y-1 >= 0:
        if liste[y-1][x] in [1,4]:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 4
            liste[y-1][x] = 2
        elif liste[y-1][x] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True

# Fonction pour se déplacer en bas

def move_down():
    global liste
    global finish
    if y+1 < yWindow / 10:
        if liste[y+1][x] in [1,4]:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 4
            liste[y+1][x] = 2
        elif liste[y+1][x] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True

# Fonction pour se déplacer à droite

def move_right():
    global liste
    global finish
    if x+1 < xWindow / 10:
        if liste[y][x+1] in [1,4]:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 4
            liste[y][x+1] = 2
        elif liste[y][x+1] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True

# Fonction pour se déplacer à gauche

def move_left():
    global liste
    global finish
    if x-1 >= 0:
        if liste[y][x-1] in [1,4]:          #On vérifie si la futur position est vide (au quel cas on pourra se déplacer)
            liste[y][x] = 4
            liste[y][x-1] = 2
        elif liste[y][x-1] == 3:        #Si la futur position est l'arrivée on déclare le jeu comme finis
            finish = True

# On lance une boucle qui modifiera l'affichage pygame

while running:

    # On définit le taux de rafraichissement de l'affichage sur 60 Hz et on remplit le fond d'une couleur blanche
    clock.tick(60)
    window.fill((255,255,255))

    # De base, on se trouve sur le menu avec deux choix : Jouer un nouveau niveau ou rejouer un ancien pour battre son score

    if play == False and replay == False and settings == False:
        buttonPlay = pygame.Rect((xWindow/2-125), (yWindow/2-125), 250, 50)
        buttonReplay = pygame.Rect((xWindow/2-125), (yWindow/2-25), 250, 50)

        buttonEasy, buttonNormal, buttonNormal = [None] * 3

        pygame.draw.rect(window, [255, 0, 0], buttonPlay)
        playtxt = font.render('Play',1,(255,255,255))
        window.blit(playtxt, (230,130) )

        pygame.draw.rect(window, [255, 0, 0], buttonReplay)
        replaytxt = font.render('Replay',1,(255,255,255))
        window.blit(replaytxt, (215,230) )

    # Menu pour choisir un surnom, choisir la difficulté, choisir le type de génération et si on laisse une trace derriere le joueur

    if settings == True:
        buttonPlay, buttonReplay = [None] * 2
        infotxt = font.render('Entrer votre nom:',1,(0,0,0))
        window.blit(infotxt, (160,50))
        nickname = font.render(nametxt,1,(0,0,0))
        window.blit(nickname, (200,80))

        buttonSwitchL = pygame.Rect((xWindow/2-200), (yWindow/2-125), 50, 50)
        buttonNormal = pygame.Rect((xWindow/2-125), (yWindow/2-125), 250, 50)
        buttonSwitchR = pygame.Rect((xWindow/2+150), (yWindow/2-125), 50, 50)

        pygame.draw.rect(window, [255, 0, 0], buttonSwitchL)
        easytxt = font.render('<',1,(255,255,255))
        window.blit(easytxt, (75,135) )

        pygame.draw.rect(window, [255, 0, 0], buttonNormal)
        normaltxt = font.render(difficultText,1,(255,255,255))
        window.blit(normaltxt, (215,135) )

        pygame.draw.rect(window, [255, 0, 0], buttonSwitchR)
        hardtxt = font.render('>',1,(255,255,255))
        window.blit(hardtxt, (425,135) )


        buttonL = pygame.Rect((xWindow/2-200), (yWindow/2-50), 50, 50)
        buttonGeneration = pygame.Rect((xWindow/2-130), (yWindow/2-50), 260, 50)
        buttonR = pygame.Rect((xWindow/2+150), (yWindow/2-50), 50, 50)

        pygame.draw.rect(window, [255, 0, 0], buttonL)
        ltxt = font.render('<',1,(255,255,255))
        window.blit(ltxt, (75,210) )

        pygame.draw.rect(window, [255, 0, 0], buttonGeneration)
        gentxt = font.render(genText,1,(255,255,255))
        window.blit(gentxt, (130,210) )

        pygame.draw.rect(window, [255, 0, 0], buttonR)
        rtxt = font.render('>',1,(255,255,255))
        window.blit(rtxt, (425,210) )

        buttonTrace = pygame.Rect((xWindow/2-110), (yWindow/2+25), 160, 50)
        buttonTraceB = pygame.Rect((xWindow/2+60), (yWindow/2+25), 50, 50)

        pygame.draw.rect(window, [255, 0, 0], buttonTrace)
        tracetxt = font.render('Tracer ?',1,(255,255,255))
        window.blit(tracetxt, (170,285) )

        pygame.draw.rect(window, colorTrB, buttonTraceB)

        buttonStart = pygame.Rect((xWindow/2-75), (yWindow/2+100), 150, 50)
        pygame.draw.rect(window, [255, 0, 0], buttonStart)
        starttxt = font.render('Start',1,(255,255,255))
        window.blit(starttxt, (225,360) )


    # Si on choisit de jouer

    if play == True:                            # On lance le timer
        if t0once == True:
            t0 = time.monotonic()
            t0once = False

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

                elif liste[y][x] == 1 or (liste[y][x] == 4 and tracer == False):
                    rect = pygame.Rect(x*10, y*10, 10, 10)
                    pygame.draw.rect(window, (255,255,255), rect)

                elif liste[y][x] == 4 and tracer == True:
                    rect = pygame.Rect(x*10, y*10, 10, 10)
                    pygame.draw.rect(window, (128,0,128), rect)


    # Fonction pour génerer un nouveau labyrinthe en maintenant la touche R

    if blockR == False:
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            delay += 1/60
            if delay > 1.5:
                if regenonce == True:
                    update_size_screen( int((xWindow-10)/20), int((yWindow-10)/20) )
                    t0 = time.monotonic()
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
        play, replay, finish, settings = [False] * 4                     # On remet les variables à faux
        update_size_screen(25,25,mazebase)                                      # On remet la taille de l'écran à la normale


    pygame.display.flip()                       # On affiche les textures mis en mémoire
    pygame.display.update()

    # Ici, on gère les touches pressées

    for event in pygame.event.get():
        if playerloc is not None:
            (x, y) = playerloc

        if event.type == QUIT or(event.type == KEYUP and event.key == K_ESCAPE):    # On arrête pygame avec la touce echap
           running = False

        if event.type == KEYDOWN:
            if settings == True:                                                       # Ecrire le nom du joueur
                if event.key == 8 and nametxt != '':
                    nametxt = nametxt[:-1]
                elif len(nametxt) < 9:
                    nametxt = nametxt + event.dict['unicode']

            if playerloc is not None:                                               # On déplace le joueur avec les touches directionnels
                if event.key == K_UP:
                    move_up()

                if event.key == K_DOWN:
                    move_down()

                if event.key == K_RIGHT:
                    move_right()

                if event.key == K_LEFT:
                    move_left()

            if event.key == K_b:                                                    # Touche B -> Touche Retour
                play, replay, settings, finish, tracer = [False] * 5
                update_size_screen(25,25)


        if event.type == pygame.MOUSEBUTTONDOWN:                                    # On gère les actions avec la souris

            mouse_pos = pygame.mouse.get_pos()                                      # On récupère la position de la souris

            if settings == True:
                if buttonSwitchL.collidepoint(mouse_pos):
                    set_difficult(-1)

                if buttonStart.collidepoint(mouse_pos):
                    update_size_screen(xDiff,yDiff)
                    play = True
                    settings = False
                    nametxt = ''

                if buttonSwitchR.collidepoint(mouse_pos):
                    set_difficult(1)

                if buttonL.collidepoint(mouse_pos):
                    set_gen(-1)

                if buttonR.collidepoint(mouse_pos):
                    set_gen(1)

                if buttonTraceB.collidepoint(mouse_pos):
                    if colorTrB == (255,0,0):
                        colorTrB = (0,255,0)
                        tracer = True
                    else:
                        colorTrB = (255,0,0)
                        tracer = False

            elif replay == True:                                                    # Si on est dans le menu replay on vérifie sur quel bouton se situe la souris pour génerer le labyrinthe correspondant
                for i in range(1,len(listreplay)):
                    button = listreplay[i][2]
                    if button.collidepoint(mouse_pos):
                        size = listreplay[i][1]
                        size = size.split(',')
                        x, y = int( float( size[0].replace('(','') ) ), int( float( size[1].replace(')','') ) )
                        mazebase = listreplay[i][0]
                        update_size_screen(x, y, mazebase)
                        liste = string_to_maze(mazebase)
                        play, blockR, saveonce, t0once, t1once = [True] * 5
                        replay = False

            if buttonPlay is not None:

                if buttonPlay.collidepoint(mouse_pos) and settings == False:              # Si on est dans le menu et qu'on clique sur le bouton play on met la variable play à Vrai
                    settings, saveonce, t0once, t1once = [True] * 4
                    blockR = False

                if buttonReplay.collidepoint(mouse_pos) and replay == False:            # Si on est dans le menu et qu'on clique sur le bouton replay on met la variable replay à Vrai
                    replay = True

# Quand on quitte la boucle on éteint pygame

pygame.quit()

