import pygame
from .Enums import State
from .Monster import Monster

#=-------------- Tile ---------------=#
class Tile:
    WHITE: list[int] = [255, 255, 255]
    RED: list[int] = [255, 0, 0]
    FONT: pygame.font.Font
    FONT_SM: pygame.font.Font
    FONT_XSM: pygame.font.Font
    cellSize: int = 20

    def __init__(self, x: int, y: int, image: pygame.Surface, state: State, isStartingTile: bool, isVerified: bool):
        width = image.get_width()
        height = image.get_height()
        self._scale = 1
        self._image = pygame.transform.scale(image, (int(width * self.scale), int(height * self.scale)))
        self._rect = image.get_rect()
        self.rect.topleft = (x, y)
        self._state: State = state
        self._startingTile: bool = isStartingTile
        self._isVerified: bool = isVerified
        self._adjacentMonsters: bool = 0
        self._hasMonster: bool = False
        self._hasCorpse: bool = False
        self._monster: Monster = Monster(0)
        self._drawed: bool = False
        self._highlighted: bool = False
        self._hovered: bool = False
        self._leftClicked: bool = False
        self._rightClicked: bool = False

    #---- Properties ----#
    @property
    def hasMonster(self):
        return self._hasMonster
    @hasMonster.setter
    def hasMonster(self, value: bool):
        self._hasMonster = value

    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self, value: int):
        self._scale = value
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, value: pygame.Surface):
        self._image = pygame.transform.scale(value, (int(value.get_width() * self.scale), int(value.get_height() * self.scale)))

    @property
    def rect(self):
        return self._rect
    @rect.setter
    def rect(self, value: pygame.Rect):
        self._rect = value

    @property
    def hasCorpse(self):
        return self._hasCorpse
    @hasCorpse.setter
    def hasCorpse(self, value: bool):
        self._hasCorpse = value

    @property
    def monster(self):
        return self._monster
    @monster.setter
    def monster(self, value: Monster):
        self._monster = value

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value: State):
        self._state = value

    @property
    def drawed(self):
        return self._drawed
    @drawed.setter
    def drawed(self, value: bool):
        self._drawed = value

    @property
    def highlighted(self):
        return self._highlighted
    @highlighted.setter
    def highlighted(self, value: bool):
        self._highlighted = value

    @property
    def hovered(self):
        return self._hovered
    @hovered.setter
    def hovered(self, value: bool):
        self._hovered = value

    @property
    def leftClicked(self):
        return self._leftClicked
    @leftClicked.setter
    def leftClicked(self, value: bool):
        self._leftClicked = value

    @property
    def rightClicked(self):
        return self._rightClicked
    @rightClicked.setter
    def rightClicked(self, value: bool):
        self._rightClicked = value

    @property
    def adjacentMonsters(self):
        return self._adjacentMonsters
    @adjacentMonsters.setter
    def adjacentMonsters(self, value: int):
        self._adjacentMonsters = value

    @property
    def startingTile(self):
        return self._startingTile
    @startingTile.setter
    def startingTile(self, value: bool):
        self._startingTile = value

    @property
    def isVerified(self):
        return self._isVerified
    @isVerified.setter
    def isVerified(self, value: bool):
        self._isVerified = value
    #--------------------#

    #------ Methods -----#
    def drawSelf(self, surface: pygame.Surface):
        self.drawed = True
        if self.state == State.Closed or self.state == State.Marked:
            surface.blit(self.image, [self.rect.x - ((self.hovered or self.highlighted) * 2), self.rect.y - ((self.hovered or self.highlighted) * 2)])
            
        elif self.state == State.Open:
            if self.adjacentMonsters != 0:
                surface.blit(Tile.FONT_XSM.render(str(self.adjacentMonsters), False, Tile.WHITE), [self.rect.x + 5, self.rect.y + 3])
                
            elif self.hasMonster:
                surface.blit(Tile.FONT_XSM.render(str(self.monster.level), False, Tile.RED), [self.rect.x + 5, self.rect.y + 3])
                
            elif self.hasCorpse:
                surface.blit(Tile.FONT_XSM.render("X", False, Tile.RED), [self.rect.x + 5, self.rect.y + 3])

    
    def isHovered(self) -> bool:
        action = False

        pos = pygame.mouse.get_pos()

        if self.drawed and self.rect.collidepoint(pos):
            self.hovered = True
            action = True
        
        else:
            self.hovered = False

        return action
    
    def isLeftClicked(self) -> bool:
        action = False

        pos = pygame.mouse.get_pos()

        if self.drawed and self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not(self.leftClicked):
                self.leftClicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.leftClicked = False

        return action
    
    def isRightClicked(self) -> bool:
        action = False

        pos = pygame.mouse.get_pos()

        if self.drawed and self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[2] == 1 and not(self.rightClicked):
                self.rightClicked = True
                action = True
        
        if pygame.mouse.get_pressed()[2] == 0:
            self.rightClicked = False

        return action
    #--------------------#
#=-----------------------------------=#