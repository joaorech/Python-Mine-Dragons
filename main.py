import sys
import pygame
import random
pygame.init()
#=== IMPORTS ===#


#================ VARIABLES ================#
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
FONT = pygame.font.Font(None, 56)
FONT_SM = pygame.font.Font(None, 48)
FONT_XSM = pygame.font.Font(None, 24)
CELL_CLOSED = pygame.image.load("./Graphics/cell_closed.png")
CELL_MARKED = pygame.image.load("./Graphics/cell_marked.png")
border_left = 100
border_top = 180
num_bombs = 120
cellsize = 20
rows = 36
cols = 24
field = []
temp = []
# field[x][y][0]: 0 se não estiver bomba, 1 se estiver bomba
# field[x][y][1]: 0 se estiver fechado, 1 se estiver aberto, 2 se estiver marcado
# field[x][y][2]: Número de bombas adjacentes
# field[x][y][3]: 1 se for uma das células iniciais, 0 senão
# field[x][y][4]: 1 se for uma das células da borda invisível, 0 senão
# field[x][y][5]: 1 se já foi verificada, 0 senão
for i in range(rows+2):
    for j in range(cols+2):
        temp.append(list([0]*6))
    field.append(temp[:])
    temp.clear()
for x in range(rows+2):
    for y in range(cols+2):
        if (x == 0 or y == 0) or (x == rows+1 or y == cols+1):
            field[x][y][1] = 1
            field[x][y][3] = 1
            field[x][y][4] = 1
            field[x][y][5] = 1
game_started = 0
celx = 0
cely = 0
#===========================================#


#================ FUNCTIONS ================#
def placeBombs(number):
    cont = 0
    for i in range(number):
        x = random.randint(1, rows)
        y = random.randint(1, cols)
        if field[x][y][0] == 0 and field[x][y][3] != 1:
            field[x][y][0] = 1
            field[x][y][5] = 1
        else:
            cont += 1
    if cont > 0:
        placeBombs(cont)


def resetField():
    global game_started
    game_started = 0
    clearScreen()
    for x in range(rows+2):
        for y in range(cols+2):
            field[x][y][0] = 0
            field[x][y][1] = 0
            field[x][y][2] = 0
            field[x][y][3] = 0
            field[x][y][5] = 0


def clearScreen():
    screen.fill(BLACK)


def onLeftClick():
    global game_started
    if game_started == 1:
        if field[celx][cely][1] == 0 or field[celx][cely][1] == 2:
            field[celx][cely][1] = 1
            if field[celx][cely][0] == 1:
                resetField()
            else:
                if field[celx][cely][2] == 0:
                    verifyNeighbors([celx, cely])
        else:
            bombs = 0
            open_cells = 0
            for n in getNeighbors([celx, cely], 0, 1):
                if n[3] == 1:
                    open_cells += 1
                if n[2] == 1 and n[3] == 2:
                    bombs += 1
            if field[celx][cely][2] == (8-open_cells):
                for n in getNeighbors([celx, cely], 0):
                    if n[2] == 1:
                        field[n[0]][n[1]][1] = 2
            if field[celx][cely][2] == bombs:
                for n in getNeighbors([celx, cely], 0, 2):
                    if n[2] != 1:
                        field[n[0]][n[1]][1] = 1
                    if n[3] == 0:
                        verifyNeighbors([n[0], n[1]])
    else:
        game_started = 1
        field[celx][cely][3] = 1
        setNeighbors([celx, cely], 3, 1)
        placeBombs(num_bombs)
        verifyAllBombs()

        field[celx][cely][1] = 1
        if field[celx][cely][0] == 1:
            resetField()
        else:
            if field[celx][cely][2] == 0:
                verifyNeighbors([celx, cely])


def onRightClick():
    if game_started == 1:
        if field[celx][cely][1] == 0:
            field[celx][cely][1] = 2
        elif field[celx][cely][1] == 2:
            field[celx][cely][1] = 0
        screen.fill(BLACK)


def getNeighbors(cel, *args):
    x = cel[0]
    y = cel[1]
    top_left = [x-1, y-1]
    top = [x, y-1]
    top_right = [x+1, y-1]
    right = [x+1, y]
    bottom_right = [x+1, y+1]
    bottom = [x, y+1]
    bottom_left = [x-1, y+1]
    left = [x-1, y]
    for i in args:
        top_left.append(field[x-1][y-1][i])
        top.append(field[x][y-1][i])
        top_right.append(field[x+1][y-1][i])
        right.append(field[x+1][y][i])
        bottom_right.append(field[x+1][y+1][i])
        bottom.append(field[x][y+1][i])
        bottom_left.append(field[x-1][y+1][i])
        left.append(field[x-1][y][i])

    neighbors = [top_left, top, top_right, right,
                 bottom_right, bottom, bottom_left, left]
    return neighbors
    # Return Indexes: [0] [1] [2]
    #                 [7][cel][3]
    #                 [6] [5] [4]


def setNeighbors(cel, type, value):
    x = cel[0]
    y = cel[1]
    field[x-1][y-1][type] = (value if field[x-1][y-1]
                             [5] != 1 else field[x-1][y-1][type])
    field[x][y-1][type] = (value if field[x][y-1][5] !=
                           1 else field[x][y-1][type])
    field[x+1][y-1][type] = (value if field[x+1][y-1]
                             [5] != 1 else field[x+1][y-1][type])
    field[x+1][y][type] = (value if field[x+1][y][5] !=
                           1 else field[x+1][y][type])
    field[x+1][y+1][type] = (value if field[x+1][y+1]
                             [5] != 1 else field[x+1][y+1][type])
    field[x][y+1][type] = (value if field[x][y+1][5] !=
                           1 else field[x][y+1][type])
    field[x-1][y+1][type] = (value if field[x-1][y+1]
                             [5] != 1 else field[x-1][y+1][type])
    field[x-1][y][type] = (value if field[x-1][y][5] !=
                           1 else field[x-1][y][type])


def verifyAllBombs():
    for x in range(rows+2):
        for y in range(cols+2):
            if (x == 0 or y == 0) or (x == rows+1 or y == cols+1):
                field[x][y][2] = 8
            else:
                bombs = 0
                for neighbor in getNeighbors([x, y], 0):
                    if neighbor[2] == 1:
                        field[neighbor[0]][neighbor[1]][2] = 8
                        bombs += 1
                field[x][y][2] = bombs


def verifyNeighbors(cel):
    field[cel[0]][cel[1]][5] = 1
    setNeighbors([cel[0], cel[1]], 1, 1)
    for neighbor in getNeighbors([cel[0], cel[1]], 2, 0, 4, 5):
        if neighbor[2] == 0 and neighbor[3] != 1 and neighbor[4] != 1 and neighbor[5] != 1:
            verifyNeighbors([neighbor[0], neighbor[1]])


def getScore():
    score = 0
    for x in range(rows):
        for y in range(cols):
            if field[x+1][y+1][1] == 1:
                score += (field[x+1][y+1][2]+1)*5
    return score


def getBombs():
    count = 0
    for x in range(rows):
        for y in range(cols):
            if field[x+1][y+1][1] == 2:
                count += 1
    return (num_bombs-count)
#===========================================#


#====================== SETUP ======================#
screen = pygame.display.set_mode((960, 720))
#===================================================#


#======================================== GAME LOOP ========================================#
while True:
    #=-------------------- EVENT HANDLER --------------------=#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_r:
                resetField()
        if event.type == pygame.MOUSEBUTTONUP:
            celx = int((int(pygame.mouse.get_pos()[0])-border_left)/cellsize)+1
            cely = int((int(pygame.mouse.get_pos()[1])-border_top)/cellsize)+1
            if not((celx < 0 or celx > 36) or (cely < 0 or cely > 24)):
                if event.button == 1:
                    # print("row: "+str(celx)+"  col: "+str(cely))
                    onLeftClick()
                if event.button == 3:
                    onRightClick()
    #---------------------------------------------------------#

    #=--------------------- GAME DRAWING --------------------=#
    screen.blit(FONT.render("Mine Field", False, WHITE), [50, 50])
    screen.blit(FONT_SM.render(
        "Score: " + str(getScore()), False, WHITE), [650, 58])
    screen.blit(FONT_SM.render(
        "Bombs: " + str(getBombs()), False, WHITE), [450, 58])
    for row in range(len(field)-1):
        for col in range(len(field[0])-1):
            if row != 0 and col != 0:
                if field[row][col][2] != 0:
                    screen.blit(FONT_XSM.render(str(field[row][col][2]), False, WHITE), [
                        border_left+((row-1)*cellsize)+5, border_top+((col-1)*cellsize)+3])
                if field[row][col][1] == 0:
                    screen.blit(CELL_CLOSED, [
                        border_left+((row-1)*cellsize), border_top+((col-1)*cellsize), cellsize, cellsize])
                elif field[row][col][1] == 2:
                    screen.blit(CELL_MARKED, [
                        border_left+((row-1)*cellsize), border_top+((col-1)*cellsize), cellsize, cellsize])
                pygame.draw.rect(screen, WHITE, [
                    border_left+((row-1)*cellsize), border_top+((col-1)*cellsize), cellsize, cellsize], 1)
    #---------------------------------------------------------#

    #=---- FUNCTIONAL ----=#
    pygame.display.update()
    pygame.time.delay(100)
    clearScreen()
    #----------------------#
#===========================================================================================#
