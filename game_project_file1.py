import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import player_sprite

 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
#print(pygame.get_init())
HEIGHT = 350
WIDTH = 700
ACC = 2
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Background(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            bg_url = "backgrounds/nightsky_2.png"
            self.bgimage = pygame.image.load(bg_url)        
            self.bgY = 0
            self.bgX = 0
 
      def render(self):
            displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
 
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ground_url = "platforms/water_1.png"
        self.image = pygame.image.load(ground_url)
        self.rect = self.image.get_rect(center = (350, 350))
 
    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))  
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()


class Player(pygame.sprite.Sprite):
    

    def __init__(self):
        super().__init__()
        BG = (0,0,0)
        self.image = player_sprite.get_image(128,128,BG)
        self.rect = self.image.get_rect()
 
        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"
        self.jumping = False
        self.dt = FPS_CLOCK.tick(60)

    def move(self):
        self.acc = vec(0,0.5)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        #returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        #player acceleration
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        #velocity calculations
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #player warping
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
 
    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top +1 
                    self.vel.y = 0
                    self.jumping = False

    def jump(self):
        self.rect.x +=1 

        #check to see if player contacts ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def update(self):
        pass
    
    def attack(self):
        pass


                        
background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()


while True:
    
    FPS_CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
     
        #if event.type == pygame.MOUSEBUTTONDOWN:
            #pass
    
            # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
    player.gravity_check()
        # Render Functions ------
    background.render() 
    ground.render()

    player.move()

    displaysurface.blit(player.image, player.rect)

    pygame.display.update() 
        
    



