import pygame 
from pygame.locals import *
import math
import sys
import pygame.mixer



SCREEN = Rect(0, 0, 400, 400) 

class Paddle(pygame.sprite.Sprite): 
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN.bottom - 20          

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]  
        self.rect.clamp_ip(SCREEN)                   

class Block(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN.left + x * self.rect.width
        self.rect.top = SCREEN.top + y * self.rect.height

class Score():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont(None, 20)
        self.score = 0
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        img = self.sysfont.render("SCORE:"+str(self.score), True, (255,255,250))
        screen.blit(img, (self.x, self.y))
    def add_score(self, x):
        self.score += x

class Ball(pygame.sprite.Sprite):
    def __init__(self, filename, paddle, blocks, score, speed, angle_left, angle_right):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.dx = self.dy = 0 
        self.paddle = paddle  
        self.blocks = blocks 
        self.update = self.start 
        self.score = score
        self.hit = 0  
        self.speed = speed 
        self.angle_left = angle_left 
        self.angle_right = angle_right 

    def start(self):
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top
        if pygame.mouse.get_pressed()[0] == 1:
            self.dx = 0
            self.dy = -self.speed
            self.update = self.move

    def move(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

        if self.rect.left < SCREEN.left:   
            self.rect.left = SCREEN.left
            self.dx = -self.dx             
        if self.rect.right > SCREEN.right: 
            self.rect.right = SCREEN.right
            self.dx = -self.dx
        if self.rect.top < SCREEN.top:     
            self.rect.top = SCREEN.top
            self.dy = -self.dy

        if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
            self.hit = 0                                
            (x1, y1) = (self.paddle.rect.left - self.rect.width, self.angle_left)
            (x2, y2) = (self.paddle.rect.right, self.angle_right)
            x = self.rect.left                          
            y = (float(y2-y1)/(x2-x1)) * (x - x1) + y1  
            angle = math.radians(y)                     
            self.dx = self.speed * math.cos(angle)
            self.dy = -self.speed * math.sin(angle)
            self.paddle_sound.play()                    

        if self.rect.top > SCREEN.bottom:
            self.update = self.start                    
            self.gameover_sound.play()
            self.hit = 0
            self.score.add_score(-100)                  

        blocks_collided = pygame.sprite.spritecollide(self, self.blocks, True)
        if blocks_collided:  
            oldrect = self.rect
            for block in blocks_collided:
                if oldrect.left < block.rect.left and oldrect.right < block.rect.right:
                    self.rect.right = block.rect.left
                    self.dx = -self.dx
                    
                if block.rect.left < oldrect.left and block.rect.right < oldrect.right:
                    self.rect.left = block.rect.right
                    self.dx = -self.dx

                if oldrect.top < block.rect.top and oldrect.bottom < block.rect.bottom:
                    self.rect.bottom = block.rect.top
                    self.dy = -self.dy

                if block.rect.top < oldrect.top and block.rect.bottom < oldrect.bottom:
                    self.rect.top = block.rect.bottom
                    self.dy = -self.dy
                self.block_sound.play()     
                self.hit += 1               
                self.score.add_score(self.hit * 10)   
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    
    Ball.paddle_sound = pygame.mixer.Sound(
        "assets/sound/######.mp3")    
    Ball.block_sound = pygame.mixer.Sound(
        "assets/sound/#######.mp3")    
    Ball.gameover_sound = pygame.mixer.Sound(
        "assets/sound/#######.mp3") 
    group = pygame.sprite.RenderUpdates()  
    blocks = pygame.sprite.Group()   

    Paddle.containers = group
    Ball.containers = group
    Block.containers = group, blocks
    paddle = Paddle("assets/img/breath_0.png")

    for x in range(1, 19):
        for y in range(1, 11):
            Block("assets/img/brown_rock.png", x, y)

    score = Score(10, 10)    

    Ball("assets/img/ball.png",
         paddle, blocks, score, 5, 135, 45)
    clock = pygame.time.Clock()

    while (1):
        clock.tick(60)      
        screen.fill((255,255,255))
        group.update()
        group.draw(screen)
        score.draw(screen) 
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
