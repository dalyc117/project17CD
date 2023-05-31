import pygame
import time


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(600, 850)
        )

    def update(self, lives, Screen_Width, Screen_Height, speed):
        self.rect.move_ip(speed)

        # keep ball on screen
        if self.rect.left <= 0 or self.rect.right >= Screen_Width:
            speed[0] = -speed[0]
            return lives
        elif self.rect.top <= 0:
            speed[1] = -speed[1]
            return lives
        # return ball to centre if it hits the bottom
        elif self.rect.bottom >= Screen_Height:
            lives = lives - 1
            self.rect = self.surf.get_rect(
                center=(500, 850))
            speed[0] = abs(speed[0])
            speed[1] = -abs(speed[1])
            time.sleep(1)
            return lives
        return lives
