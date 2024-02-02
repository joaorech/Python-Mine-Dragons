import pygame

BLACK: list[int] = [0, 0, 0]
WHITE: list[int] = [255, 255, 255]
RED: list[int] = [255, 0, 0]
GREEN: list[int] = [0, 255, 0]
BLUE: list[int] = [0, 0, 255]
FONT = pygame.font.Font(None, 56)
FONT_SM = pygame.font.Font(None, 48)
FONT_XSM = pygame.font.Font(None, 24)
CELL_CLOSED: pygame.Surface = pygame.image.load("./Graphics/cell_closed.png")
CELL_MARKED: pygame.Surface = pygame.image.load("./Graphics/cell_marked.png")