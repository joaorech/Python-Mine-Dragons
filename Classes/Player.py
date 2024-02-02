from .Enums import State, Directions
import pygame

from .Field import Field
from .Tile import Tile
from .Monster import Monster

#=-------------- Player -------------=#
class Player:
    currentLevel: int = 1
    xpToNextLevel: int = 3

    def __init__(self, field: Field):
        self._field = field
        self._level: int = 1
        self._maxHp: int = 3
        self._hp: int = 3
        self._attack: int = 1
        self._xp: int = 0
    
    #---- Properties ----#
    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, value: int):
        if value > self._level:
            self.LevelUp()
        self._level = value
        Player.currentLevel = value

    @property
    def maxHp(self):
        return self._maxHp
    @maxHp.setter
    def maxHp(self, value: int):
        self._maxHp = value

    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value: int):
        self._hp = value
        if self._hp <= 0:
            self.Death()

    @property
    def attack(self):
        return self._attack
    @attack.setter
    def attack(self, value: int):
        self._attack = value

    @property
    def xp(self):
        return self._xp
    @xp.setter
    def xp(self, value: int):
        self._xp = value
        if self._xp >= Player.xpToNextLevel:
            overflowXp = self._xp - Player.xpToNextLevel
            self.level += 1
            self.xp += overflowXp
    #--------------------#

    #------ Methods -----#
    def LeftClick(self, tile: Tile):
        if tile.state == State.Closed or tile.state == State.Marked:
            tile.state = State.Open
            if tile.hasMonster:
                self.Combat(tile, tile.monster)
            else:
                if tile.adjacentMonsters == 0:
                    self._field.VerifyNeighbors(tile)
        else:
            if tile.hasMonster:
                self.Combat(tile, tile.monster)
            else:
                open_tiles: int = 0

                for neighborTile in self._field.GetNeighbors(tile):
                    if neighborTile is not None:
                        if neighborTile.state == State.Open:
                            open_tiles += 1

                if tile.adjacentMonsters == (8-open_tiles):
                    for neighborTile in self._field.GetNeighbors(tile):
                        if neighborTile is not None:
                            if neighborTile.hasMonster:
                                neighborTile.state = State.Marked


    def RightClick(self, tile: Tile, imageClosed: pygame.Surface, imageMarked: pygame.Surface):
        if tile.state == State.Closed:
            tile.state = State.Marked
            tile.image = imageMarked
        elif tile.state == State.Marked:
            tile.state = State.Closed
            tile.image = imageClosed


    def Death(self):
        self._field.ResetField()
        self.ResetSelf()

    def ResetSelf(self):
        self._level = 1
        self._maxHp = 3
        self._hp = 3
        self._attack = 1
        self._xp = 0
    
    def Combat(self, tile: Tile, monster: Monster):
        attackBack = monster.Attack(self.attack)

        if attackBack > 0:
            self.hp -= attackBack
        else:
            self.OnKill(tile, monster)

    def OnKill(self, tile: Tile, monster: Monster):
        xpGain = monster.level - self.currentLevel + 2
        if xpGain > 0:
            self.xp += xpGain

        monster.level = 0
        tile.hasMonster = False
        tile.hasCorpse = True

    def LevelUp(self):
        self.hp = self.maxHp
        self.xp = 0
    #--------------------#
#=-----------------------------------=#