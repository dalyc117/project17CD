import pygame
import time


from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

#define window size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
score = -1000
lives = 5
level = 0
speed = [8,-8]
D_grey = (50, 50, 50)
L_grey = (75, 75, 75)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((150, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center= (500, 900)
        )

# Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
          self.rect.move_ip(-30, 0)
        if pressed_keys[K_RIGHT]:
           self.rect.move_ip(30, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center= (600, 850)
        )

    def update(self,lives):
        self.rect.move_ip(speed)

        #keep ball on screen
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            speed[0] = -speed[0]
            return(lives)
        elif self.rect.top <= 0:
            speed[1] = -speed[1]
            return(lives)
        #return ball to centre if it hits the bottom
        elif self.rect.bottom >= SCREEN_HEIGHT:
            lives = lives - 1
            self.rect = self.surf.get_rect(
                center=(500, 850))
            speed[0] = abs(speed[0])
            speed[1] = -abs(speed[1])
            time.sleep(1)
            return(lives)
        return (lives)
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, colour):
        super(Brick,self).__init__()
        self.surf = pygame.Surface((95,10))
        self.surf.fill((colour))
        self.rect = self.surf.get_rect(center=(x,y))

Row_colour = {  0 : (0,0,0),
                1 : (93,0,255),
                2 : (0,47,255),
                3 : (0,255,221),
                4 : (55,255,0),
                5 : (246,255,0),
                6 : (255,140,0),
                7 : (255,0,0)}

pygame.init()
pygame.font.init()

# create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
font = pygame.font.Font('freesansbold.ttf', 32)
all_sprites = pygame.sprite.Group()


#Instantiate Player and ball
player = Player()
ball = Ball()
all_sprites.add(player)
all_sprites.add(ball)
#Instantiate brick wall
bricks = pygame.sprite.Group()
clock = pygame.time.Clock()

game_running = True
game_over = False

    #Game loop
while game_running == True:
    screen.fill((L_grey))
    #Loop generates new brick wall when none left
    if len(bricks.sprites()) == 0:
        for j in range (0,8):
            for i in range(0,9):
                # *100 is for pixel placement, 100+ is a fixed integer to make sure the blocks are not directly pressed against the top of the screen
                newbrick = Brick((i+1)*100, (100+(j+1)*25),(Row_colour.get(j)))
                all_sprites.add(newbrick)
                bricks.add(newbrick)
        ball.rect = ball.surf.get_rect(
            center=(500, 850))
        speed[0] = abs(speed[0]) +2
        speed[1] = -(abs(speed[1]) +2)
        score = score + 1000
        level = level + 1
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        pygame.display.flip()
        time.sleep(1)
    #look at every event in the queue
    for event in pygame.event.get():
        #Did the user hit a key?
        if event.type == KEYDOWN:
            #Escape key
            if event.key == K_ESCAPE:
                game_running = False

        elif event.type == QUIT:
            game_running = False

    if pygame.Rect.colliderect(ball.rect,player):
        speed[1] = -speed[1]

    if pygame.sprite.spritecollideany(ball,bricks):
        collided_brick = pygame.sprite.spritecollideany(ball,bricks)
        if collided_brick != None:
            collided_brick.kill()
        speed[1] = -speed[1]
        score = score + 20

    if game_over == True:
        if event.type == KEYDOWN:
            # Enter key
            if event.key == K_RETURN:
                for entity in bricks:
                    entity.kill()
                pygame.display.flip()
                game_over = False
                score = -1000
                lives = 5
                level = 0
                speed = [8, -8]

        G_over1 = font.render("GAME OVER", True, D_grey)
        textRect = G_over1.get_rect()
        textRect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) -50)
        screen.blit(G_over1, textRect)
        G_over2 = font.render("PRESS ENTER TO", True, D_grey)
        textRect = G_over2.get_rect()
        textRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(G_over2, textRect)
        G_over3 = font.render("PLAY AGAIN", True, D_grey)
        textRect = G_over3.get_rect()
        textRect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) +50)
        screen.blit(G_over3, textRect)
        Score = font.render(f'SCORE: {score}', True, D_grey)
        textRect = Score.get_rect()
        textRect.center = (200, 50)
        screen.blit(Score, textRect)
        pygame.display.flip()

    # get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # update player position based on keypresses
    player.update(pressed_keys)

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

    lives = ball.update(lives)
    if lives == 0:
        game_over = True
        speed = [0,0]

    if game_over == False:
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    clock.tick(60)

