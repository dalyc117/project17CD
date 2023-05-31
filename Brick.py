import pygame

Row_colour = {0: (0, 0, 0),
              1: (93, 0, 255),
              2: (0, 47, 255),
              3: (0, 255, 221),
              4: (55, 255, 0),
              5: (246, 255, 0),
              6: (255, 140, 0),
              7: (255, 0, 0)}  # Red


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, colour):
        super(Brick, self).__init__()
        self.surf = pygame.Surface((95, 10))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(x, y))
