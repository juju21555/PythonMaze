import random

# Exploration exhaustive

def breakWall(x1,y1,x2,y2):
    milieu = [ x1+x2+1, y1+y2+1 ]
    murs[milieu[1]][milieu[0]] = 1

def perpendicular(x1,y1,x2,y2):
    if x1-x2 == 0:
        return ['E','O']
    elif y1-y2 == 0:
        return ['N','S']

def weaveWall(x1,y1,x2,y2):
    milieu = [ x1+x2+1, y1+y2+1 ]
    if x1-x2 == 0:
        if y1-y2>0:
            y3 = 2*y2+2
            y4 = 2*y2+4

        elif y2-y1>0:
            y3 = 2*y1+2
            y4 = 2*y1+4

        x3,x4 = [2*x1+1] * 2
        murs[y3][x3] = 5
        murs[y4][x4] = 6

    elif y1-y2 == 0:
        if x1-x2>0:
            x3 = 2*x2+2
            x4 = 2*x2+4

        elif x2-x1>0:
            x3 = 2*x1+2
            x4 = 2*x1+4

        y3,y4 = [2*y1+1] * 2
        murs[y3][x3] = 7
        murs[y4][x4] = 8

    murs[milieu[1]][milieu[0]] = 1

def generate_labyrinthe(xMax, yMax):

    global murs

    directionX = {'N':0,'S':0,'E':1,'O':-1}
    directionY = {'N':1,'S':-1,'E':0,'O':0}

    labyrinthe = [[0 for x in range(xMax)] for y in range(yMax)]

    murs = [[0 for x in range(2*xMax+1)] for y in range(2*yMax+1)]
    for y in range(len(murs)-1):
        for x in range(len(murs[y])-1):
            if x % 2 != 0 and y % 2 != 0:
                murs[y][x] = 1


    randCell = ((random.randrange(xMax)), (random.randrange(yMax)))
    lastCell = [randCell]


    while lastCell != []:
        (rx, ry) = lastCell[-1]
        labyrinthe[ry][rx] = 1
        lVoisins = []
        for direction in ['N','S','O','E']:
            nx = rx + directionX[direction]
            ny = ry + directionY[direction]
            if nx >= 0 and nx < xMax and ny >= 0 and ny < yMax and labyrinthe[ny][nx] == 0:

                lVoisins.append(direction)

        if len(lVoisins) > 0:
            var = random.choice(lVoisins)
            breakWall(rx, ry, (rx+directionX[var]), (ry+directionY[var]))
            rx, ry = rx + directionX[var], ry + directionY[var]
            lastCell.append((rx, ry))

        else:
            (rx, ry) = lastCell[-1]
            if len(lastCell) > 1:
                (ax, ay) = lastCell[-2]
                wVoisins = []
                for direction in perpendicular(rx,ry,ax,ay):
                    nx = rx + 2 * directionX[direction]
                    ny = ry + 2 * directionY[direction]
                    if nx >= 1 and nx < xMax-1 and ny >= 1 and ny < yMax-1 and labyrinthe[ny][nx] == 0:

                        wVoisins.append(direction)

                if len(wVoisins) > 0:
                    var = random.choice(wVoisins)
                    weaveWall(rx, ry, (rx+2*directionX[var]), (ry+2*directionY[var]))
                    rx, ry = rx + 2*directionX[var], ry + 2*directionY[var]
                    lastCell.append((rx, ry))
                else:
                    lastCell.pop()
            else:
                lastCell.pop()

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

