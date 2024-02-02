import pygame

class Button():
    def __init__(self, x: int, y: int, image: pygame.Surface, scale: float):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def drawSelf(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def isClicked(self) -> bool:
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not(self.clicked):
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
