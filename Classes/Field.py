import random
import math
import pygame

from .Enums import State
from .Tile import Tile

class Field:
    tiles: list[Tile] = []
    rows: int = 36
    cols: int = 24
    numberMonsters: int = 120

    def __init__(self, image: pygame.Surface, borderLeft: int, borderTop: int):
        self.reseted = False
        for x in range(Field.rows):
            for y in range(Field.cols):
                Field.tiles.append(Tile(borderTop + x * Tile.cellSize, borderLeft + y * Tile.cellSize, image, State.Closed, False, False))


    def PrepareField(self, tile: Tile):
        tile.startingTile = True
        self.SetNeighbors(tile, "startingTile", True)
        self.PlaceMonsters(self.numberMonsters)
        self.VerifyAllMonsters()
        self.SetMonsterlevel()

        tile.state = State.Open
        if tile.hasMonster:
            self.ResetField()
        else:
            if tile.adjacentMonsters == 0:
                self.VerifyNeighbors(tile)


    def PlaceMonsters(self, number: int):
        cont: int = 0
        for i in range(number):
            x = random.randint(0, Field.rows * Field.cols - 1)
            tile: Tile = Field.tiles[x]
            if not tile.hasMonster and not tile.startingTile:
                tile.hasMonster = True
                tile.isVerified = True
            else:
                cont += 1
        if cont > 0:
            self.PlaceMonsters(cont)


    def VerifyAllMonsters(self):
        for tile in Field.tiles:
            monsters: int = 0
            for neighborTile in self.GetNeighbors(tile):
                if neighborTile is not None:
                    if neighborTile.hasMonster:
                        neighborTile.adjacentMonsters = 0
                        monsters += 1
            tile.adjacentMonsters = monsters


    def SetMonsterlevel(self):
        for tile in Field.tiles:
            if tile.hasMonster:
                total: int = 0
                for neighbor in self.GetNeighbors(tile):
                    if neighbor is not None:
                        total += neighbor.adjacentMonsters
                level = math.floor(total/6)
                tile.monster.level = level

    
    def GetNeighbors(self, tile: Tile) -> list[Tile]:
        x = tile.rect.x
        y = tile.rect.y
        topLeft = Field.Tile(x - 1 * Tile.cellSize, y - 1 * Tile.cellSize)
        top = Field.Tile(x, y - 1 * Tile.cellSize)
        topRight = Field.Tile(x + 1 * Tile.cellSize, y - 1 * Tile.cellSize)
        right = Field.Tile(x + 1 * Tile.cellSize, y)
        bottomRight = Field.Tile(x + 1 * Tile.cellSize, y + 1 * Tile.cellSize)
        bottom = Field.Tile(x, y + 1 * Tile.cellSize)
        bottomLeft = Field.Tile(x - 1 * Tile.cellSize, y + 1 * Tile.cellSize)
        left = Field.Tile(x - 1 * Tile.cellSize, y)

        neighbors: list[Tile] = [topLeft, top, topRight, right,
                    bottomRight, bottom, bottomLeft, left]

        return neighbors


    def SetNeighbors(self, tile: Tile, type: str, value):
        for neighborTile in self.GetNeighbors(tile):
            if neighborTile is not None:
                setattr(neighborTile, type, value)
    

    def VerifyNeighbors(self, tile: Tile):
        tile.isVerified = True
        self.SetNeighbors(tile, "state", State.Open)
        for neighborTile in self.GetNeighbors(tile):
            if neighborTile is not None:
                if neighborTile.adjacentMonsters == 0 and not neighborTile.hasMonster and not neighborTile.isVerified:
                    self.VerifyNeighbors(neighborTile)


    def ResetField(self):
        for tile in Field.tiles:
            tile.hasMonster = False
            tile.state = State.Closed
            tile.adjacentMonsters = 0
            tile.startingTile = False
            tile.isVerified = False
        self.reseted = True


    @staticmethod
    def Tile(x: int, y: int) -> Tile:
        for tile in Field.tiles:
            if (tile.rect.x == x and tile.rect.y == y):
                return tile


    @staticmethod
    def GetMonsters() -> int:
        count: int = 0
        for tile in Field.tiles:
            if tile.state == State.Marked:
                count += 1
        return (Field.numberMonsters - count)
    