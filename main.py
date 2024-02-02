import sys
import math
from Classes.Enums import State, Directions
from Classes.Field import Field
from Classes.Tile import Tile
from Classes.Monster import Monster
from Classes.Player import Player
import pygame

pygame.init()
#=== IMPORTS ===#


#================ VARIABLES ================#
screenWidth: int = 960
screenHeight: int = 720
screen: pygame.Surface = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Dungeon Sweeper")

BLACK: list[int] = [0, 0, 0]
WHITE: list[int] = [255, 255, 255]
RED: list[int] = [255, 0, 0]
GREEN: list[int] = [0, 255, 0]
BLUE: list[int] = [0, 0, 255]
FONT = pygame.font.Font(None, 56)
FONT_SM = pygame.font.Font(None, 48)
FONT_XSM = pygame.font.Font(None, 24)
CELL_CLOSED = pygame.image.load("./Graphics/cell_closed.png").convert_alpha()
CELL_MARKED = pygame.image.load("./Graphics/cell_marked.png").convert_alpha()
Tile.FONT = FONT
Tile.FONT_SM = FONT_SM
Tile.FONT_XSM = FONT_XSM

clock = pygame.time.Clock()
borderLeft: int = 100
borderTop: int = 220
menuState = "main"
debugMode: bool = False
gameStarted: bool = False
field = Field(CELL_CLOSED, borderTop, borderLeft)
player: Player = Player(field)
#===========================================#


#================ FUNCTIONS ================#
def getScore():
    score = 0
    for tile in Field.tiles:
        if tile.state == State.Open:
            score += (tile.adjacentMonsters + 1) * 5
    return score

def ClearScreen():
    screen.fill([0, 0, 0])

def resetDraws():
    for tile in Field.tiles:
        tile.drawed = False

def drawNextFrame():
    match menuState:
        case "main":
            pass
        case "field":
            if debugMode:
                pygame.draw.rect(screen, RED, pygame.Rect(0, 0, screenWidth, screenHeight), 1)

            screen.blit(FONT.render("Dungeon Sweeper", False, WHITE), [50, 50])
            screen.blit(FONT_SM.render("Monsters: " + str(Field.GetMonsters()), False, WHITE), [650, 54])
            screen.blit(FONT_SM.render("Life: " + str(player.hp) + " Level: " + str(player.level) + " XP: " + str(player.xp) + " Attack: " + str(player.attack), False, WHITE), [50, 100])
            
            for tile in Field.tiles:
                tile.drawSelf(screen)
#===========================================#


#======================================== GAME LOOP ========================================#
run = True
while run:
    #=-------------------- EVENT HANDLER --------------------=#
    if debugMode:
        for tile in Field.tiles:
            if tile.isLeftClicked():
                if tile.hasMonster:
                    print("X: ", tile.rect.x, ", Y: ", tile.rect.y, ", State: ", tile.state, ", AdjacentMonsters: ", tile.adjacentMonsters, ", Level: ", tile.monster.level, ", Life: ", tile.monster.hp, ", Attack: ", tile.monster.attack)
                else:
                    print("X: ", tile.rect.x, ", Y: ", tile.rect.y, ", StartingTile: ", tile.startingTile, ", State: ", tile.state, ", AdjacentMonsters: ", tile.adjacentMonsters, ", Hovered: ", tile.hovered)
            
    else:
        for tile in Field.tiles:
            tile.isHovered()

            if tile.isLeftClicked():
                if gameStarted:
                    player.LeftClick(tile)
                else:
                    gameStarted = True
                    field.PrepareField(tile)
                    player.LeftClick(tile)

            if tile.isRightClicked():
                player.RightClick(tile, CELL_CLOSED, CELL_MARKED)
                
        if field.reseted:
            player.Death()
            field.reseted = False
            gameStarted = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_r:
                player.Death()
                gameStarted = False
            if event.key == pygame.K_d:
                debugMode = not debugMode
            if event.key == pygame.K_t:
                if menuState == "main":
                    menuState = "field"
                elif menuState == "field":
                    menuState = "main"
    #---------------------------------------------------------#

    #=--------------------- GAME DRAWING --------------------=#
    resetDraws()
    drawNextFrame()
    #---------------------------------------------------------#

    #=---- FUNCTIONAL ----=#
    pygame.display.update()
    clock.tick(60)
    ClearScreen()
    #----------------------#

pygame.quit()
#===========================================================================================#
