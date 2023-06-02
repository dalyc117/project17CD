import pygame
import time
import Player
import Ball
import Brick

from pygame.locals import (
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

# define window size
Screen_Width = 1000
Screen_Height = 1000
# Score is +1000 whenever a new wall is generated, including the first one
score = -2000
lives = 5
level = 0
speed = [8, -8]
D_grey = (50, 50, 50)
L_grey = (75, 75, 75)

pygame.init()
pygame.font.init()

# create the screen object
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
font = pygame.font.Font('freesansbold.ttf', 32)
all_sprites = pygame.sprite.Group()

# Instantiate Player and ball
player = Player.Player()
ball = Ball.Ball()
# Create some groups and a clock
all_sprites.add(player)
all_sprites.add(ball)
bricks = pygame.sprite.Group()
clock = pygame.time.Clock()

game_running = True
game_over = False

# Game loop
while game_running:
    screen.fill(L_grey)

    # Loop generates new brick wall when no bricks left
    if len(bricks.sprites()) == 0:
        for j in range(0, 8):
            for i in range(0, 9):
                # *100 is for pixel placement, 100+ is a fixed integer to make sure the blocks are not directly pressed against the top of the screen
                if j == 1:
                    newbrick = Brick.Brick((i + 1) * 100, (100 + (j + 1) * 25), (Brick.Row_colour.get(j)), 2)
                else:
                    newbrick = Brick.Brick((i + 1) * 100, (100 + (j + 1) * 25), (Brick.Row_colour.get(j)), 1)
                all_sprites.add(newbrick)
                bricks.add(newbrick)
        # Resets other aspects of the game
        ball.rect = ball.surf.get_rect(
            center=(500, 850))
        speed[0] = abs(speed[0]) + 2
        speed[1] = -(abs(speed[1]) + 2)
        score = score + 2000
        level = level + 1
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        pygame.display.flip()
        time.sleep(1)

    # look at every event in the queue
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Escape key
            if event.key == K_ESCAPE:
                game_running = False

        elif event.type == QUIT:
            game_running = False

    # Check for player and ball collision
    if pygame.Rect.colliderect(ball.rect, player):
        speed[1] = -speed[1]

    # Check for ball and brick collision
    if pygame.sprite.spritecollideany(ball, bricks):
        collided_brick = pygame.sprite.spritecollideany(ball, bricks)
        if collided_brick != None:
            collided_brick.brick_lives = collided_brick.brick_lives - 1
            if collided_brick.brick_lives == 0:
                collided_brick.kill()
        speed[1] = -speed[1]
        score = score + 20

    # Check for game over and show game over screen
    if game_over == True:
        if event.type == KEYDOWN:
            # Check for restart request, and execute
            if event.key == K_RETURN:
                for entity in bricks:  # remove all bricks from the previous game
                    entity.kill()
                pygame.display.flip()
                # Restore these to their original values
                game_over = False
                score = -2000
                lives = 5
                level = 0
                speed = [8, -8]

        # Display Game Over text
        G_over1 = font.render("GAME OVER", True, D_grey)
        textRect = G_over1.get_rect()
        textRect.center = (Screen_Width / 2, (Screen_Height / 2) - 50)
        screen.blit(G_over1, textRect)
        G_over2 = font.render("PRESS ENTER TO", True, D_grey)
        textRect = G_over2.get_rect()
        textRect.center = (Screen_Width / 2, Screen_Height / 2)
        screen.blit(G_over2, textRect)
        G_over3 = font.render("PLAY AGAIN", True, D_grey)
        textRect = G_over3.get_rect()
        textRect.center = (Screen_Width / 2, (Screen_Height / 2) + 50)
        screen.blit(G_over3, textRect)
        Score = font.render(f'SCORE: {score}', True, D_grey)
        textRect = Score.get_rect()
        textRect.center = (200, 50)
        screen.blit(Score, textRect)
        pygame.display.flip()

    # get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # update player position based on key presses
    player.update(pressed_keys, Screen_Width)

    # Text displayed during gameplay
    if game_over == False:
        Score = font.render(f'SCORE: {score}', True, D_grey)
        textRect = Score.get_rect()
        textRect.center = (200, 50)
        screen.blit(Score, textRect)

        Level = font.render(f'LEVEL: {level}', True, D_grey)
        textRect = Level.get_rect()
        textRect.center = (500, 50)
        screen.blit(Level, textRect)

        Lives = font.render(f'LIVES: {lives}', True, D_grey)
        textRect = Lives.get_rect()
        textRect.center = (800, 50)
        screen.blit(Lives, textRect)

    # Update ball position and check remaining lives
    lives = ball.update(lives, Screen_Width, Screen_Height, speed)
    if lives == 0:
        game_over = True
        speed = [0, 0]

    # Draw all sprites on screen
    if game_over == False:
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    clock.tick(60)
