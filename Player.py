import pygame

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((150, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(500, 900)
        )
        # Move the sprite based on user key presses

    def update(self, pressed_keys, Screen_Width):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-30, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(30, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Screen_Width:
            self.rect.right = Screen_Width
