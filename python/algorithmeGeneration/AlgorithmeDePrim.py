import random

# Algorithme de Prim

def breakWall(x1,y1,x2,y2):
    milieu = [ int((x1+x2) /2), int((y1+y2) /2) ]
    murs[milieu[1]][milieu[0]] = 1

def generate_labyrinthe(xMax, yMax):

    global murs

    dx = {'N':0,'S':0,'E':2,'O':-2}
    dy = {'N':2,'S':-2,'E':0,'O':0}

    murs = [[0 for x in range(2*xMax+1)] for y in range(2*yMax+1)]

    listCell = []

    (rx, ry) = ((2*random.randrange(xMax)+1), (2*random.randrange(yMax)+1))
    murs[ry][rx] = 1

    for d in ['N','S','O','E']:
        nx = rx + dx[d]
        ny = ry + dy[d]
        if nx >= 0 and nx < 2*xMax+1 and ny >= 0 and ny < 2*yMax+1:
            murs[ny][nx] = 2
            listCell.append((nx, ny))

    while listCell != []:
                (rx, ry) = random.choice(listCell)
                listCell.remove((rx, ry))
                murs[ry][rx] = 1
                voisinsVisite = []
                for d in ['N','S','O','E']:
                    nx, ny = rx + dx[d], ry + dy[d]
                    if nx >= 0 and nx < 2*xMax+1 and ny >= 0 and ny < 2*yMax+1 and murs[ny][nx] == 1:
                        voisinsVisite.append((nx, ny))

                for d in ['N','S','O','E']:
                    nx, ny = rx + dx[d], ry + dy[d]
                    if nx >= 0 and nx < 2*xMax+1 and ny >= 0 and ny < 2*yMax+1 and murs[ny][nx] == 0:
                        murs[ny][nx] = 2
                        listCell.append((nx, ny))

                if len(voisinsVisite) > 0:
                    (nx, ny) = random.choice(voisinsVisite)
                    breakWall(nx,ny,rx,ry)
                    murs[ny][nx] = 1

    dirStart = random.randrange(4)
    if dirStart == 0:
        start = [0, 2 * random.randrange(yMax) +1 ]
        end = [(2 * xMax), 2 * random.randrange(yMax) + 1 ]
    elif dirStart == 1:
        start = [2 * random.randrange(xMax) + 1, (2 * yMax) ]
        end = [2 * random.randrange(xMax) + 1, 0 ]
    elif dirStart == 2:
        start = [(2 * xMax), 2 * random.randrange(yMax) + 1 ]
        end = [0, 2 * random.randrange(yMax) + 1 ]
    elif dirStart == 3:
        start = [2 * random.randrange(xMax) + 1, 0  ]
        end = [2 * random.randrange(xMax) + 1, (2 * yMax) ]

    murs[start[1]][start[0]] = 2
    murs[end[1]][end[0]] = 3

    return murs